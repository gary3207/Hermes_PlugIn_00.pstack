"""Read-only native discovery probe; run with an importable Hermes runtime.

Example: python source/tests/native_probe.py --home <isolated-home> --package source/pstack
This never installs a plugin, changes settings, starts a job, or calls an LLM.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", type=Path, required=True)
    parser.add_argument("--package", type=Path, required=True)
    args = parser.parse_args()
    home = args.home.resolve()
    configured_home = os.environ.get("HERMES_HOME")
    if not configured_home or Path(configured_home).resolve() != home:
        raise RuntimeError("Set HERMES_HOME to the explicit probe --home before starting Python")

    from hermes_constants import get_hermes_home
    from hermes_cli.plugins import PluginManager

    if Path(get_hermes_home()).resolve() != home:
        raise RuntimeError("Hermes resolved a different home; refusing to probe")
    expected = args.package.resolve()
    catalog = json.loads((expected / "skills.json").read_text(encoding="utf-8"))
    manager = PluginManager()
    manager.discover_and_load()
    entries = [p for p in manager.list_plugins() if p["name"] == "pstack"]
    if len(entries) != 1 or not entries[0]["enabled"] or entries[0]["error"]:
        raise RuntimeError("PStack was not independently discovered and enabled: " + repr(entries))
    actual = set(manager.list_plugin_skills("pstack"))
    if actual != set(catalog):
        raise RuntimeError("Native skill identifiers do not match the publication catalog")
    metadata = {x["name"]: x for x in manager.list_plugin_skill_metadata()}
    installed = None
    for name, description in catalog.items():
        qualified = "pstack:" + name
        path = manager.find_plugin_skill(qualified)
        if not path or not path.is_file() or path.read_bytes() != (expected / "skills" / name / "SKILL.md").read_bytes():
            raise RuntimeError("Native skill payload mismatch: " + qualified)
        if metadata[qualified]["description"] != description:
            raise RuntimeError("Native skill trigger metadata mismatch: " + qualified)
        installed = path.parents[2]
    if installed is None:
        raise RuntimeError("The native skill catalog is empty")
    matched = 0
    for source in sorted(expected.rglob("*")):
        if not source.is_file() or "__pycache__" in source.parts or source.suffix == ".pyc":
            continue
        target = installed / source.relative_to(expected)
        if not target.is_file() or hashlib.sha256(source.read_bytes()).digest() != hashlib.sha256(target.read_bytes()).digest():
            raise RuntimeError("Installed payload mismatch: " + str(source.relative_to(expected)))
        matched += 1
    hook_results = manager.invoke_hook("pre_llm_call", conversation_history=[], session_id="pstack-offline-probe")
    ours = [r for r in hook_results if isinstance(r, dict) and "HERMES PSTACK" in str(r.get("context", ""))]
    if len(ours) != 1 or "pstack:reliability" not in ours[0]["context"]:
        raise RuntimeError("Expected one real enabled PStack hook result; check the profile setting")
    repeat = manager.invoke_hook("pre_llm_call", conversation_history=[{"role": "user", "api_content": ours[0]["context"]}], session_id="pstack-offline-probe")
    if any(isinstance(r, dict) and "HERMES PSTACK" in str(r.get("context", "")) for r in repeat):
        raise RuntimeError("Unchanged policy was appended twice")
    print(json.dumps({"ok": True, "home": str(home), "native_discovery": True, "native_skills": len(actual), "matching_payload_files": matched, "hook_executed": True, "repeat_context_suppressed": True, "model_call": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
