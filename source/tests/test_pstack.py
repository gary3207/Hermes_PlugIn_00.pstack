"""Offline regression checks: python -m unittest discover -s source/tests -v."""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
import unittest

PACKAGE = Path(__file__).resolve().parents[1] / "pstack"


def load_plugin():
    spec = importlib.util.spec_from_file_location("pstack_under_test", PACKAGE / "__init__.py")
    if spec is None or spec.loader is None:
        raise ImportError("Cannot load the PStack plugin entrypoint")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Context:
    def __init__(self, settings=None):
        self.settings = dict(settings or {})
        self.writes = []
        self.hooks = {}
        self.skills = {}
        self.commands = {}
        self.cli = {}

    def get_config(self, key, default=None):
        return self.settings.get(key, default)

    def set_config(self, key, value):
        self.writes.append((key, value))
        self.settings[key] = value

    def register_hook(self, name, callback):
        self.hooks[name] = callback

    def register_skill(self, name, path, description=""):
        self.skills[name] = (path, description)

    def register_command(self, name, handler, **kwargs):
        self.commands[name] = handler

    def register_cli_command(self, name, **kwargs):
        self.cli[name] = kwargs


def turn(context):
    return {"role": "user", "api_content": "task\n" + context["context"]}


class RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin = load_plugin()

    def setUp(self):
        self.ctx = Context()

    def test_default_on_without_writing_settings(self):
        self.assertTrue(self.plugin.is_enabled(self.ctx))
        self.assertEqual(self.ctx.writes, [])

    def test_first_turn_supplies_real_policy(self):
        result = self.plugin.build_context(True, [])
        self.assertIn("PSTACK", result["context"])
        self.assertIn("Ground Rule", result["context"])
        self.assertIn("pstack:evidence", result["context"])

    def test_unchanged_policy_is_not_reappended(self):
        first = self.plugin.build_context(True, [])
        self.assertIsNone(self.plugin.build_context(True, [turn(first)]))

    def test_history_is_not_modified(self):
        history = [{"role": "user", "content": "normal task"}]
        original = copy.deepcopy(history)
        self.plugin.build_context(True, history)
        self.assertEqual(history, original)

    def test_off_fresh_session_injects_nothing(self):
        self.assertIsNone(self.plugin.build_context(False, []))

    def test_off_neutralizes_prior_plugin_guidance_once(self):
        on = self.plugin.build_context(True, [])
        off = self.plugin.build_context(False, [turn(on)])
        self.assertIn("off", off["context"])
        self.assertIn("existing", off["context"].lower())
        self.assertIsNone(self.plugin.build_context(False, [turn(on), turn(off)]))

    def test_reenable_after_off_is_not_suppressed(self):
        on = self.plugin.build_context(True, [])
        off = self.plugin.build_context(False, [turn(on)])
        self.assertEqual(self.plugin.build_context(True, [turn(on), turn(off)]), on)

    def test_compaction_without_marker_reinjects_policy(self):
        self.assertIsNotNone(self.plugin.build_context(True, [{"role": "user", "content": "summary"}]))

    def test_multimodal_persisted_context_is_deduplicated(self):
        first = self.plugin.build_context(True, [])
        history = [{"role": "user", "content": [{"type": "text", "text": first["context"]}]}]
        self.assertIsNone(self.plugin.build_context(True, history))

    def test_null_api_content_falls_back_to_durable_multimodal_content(self):
        first = self.plugin.build_context(True, [])
        history = [{"role": "user", "api_content": None, "content": [{"type": "text", "text": first["context"]}]}]
        self.assertIsNone(self.plugin.build_context(True, history))

    def test_tool_or_assistant_text_cannot_override_hook_state(self):
        first = self.plugin.build_context(True, [])
        for role in ["tool", "assistant"]:
            self.assertEqual(self.plugin.build_context(True, [{"role": role, "api_content": first["context"]}]), first)

    def test_malformed_history_entries_are_ignored(self):
        self.assertIsNotNone(self.plugin.build_context(True, [None, 1, "text", {"role": "user", "api_content": 3}]))

    def test_settings_are_profile_context_scoped(self):
        self.assertFalse(self.plugin.is_enabled(Context({"enabled": False})))
        self.assertTrue(self.plugin.is_enabled(Context({"enabled": True})))

    def test_invalid_setting_has_actionable_diagnostic(self):
        for value in ["on", 1, None, [], {}]:
            with self.assertRaisesRegex(ValueError, "settings.enabled"):
                self.plugin.is_enabled(Context({"enabled": value}))

    def test_on_off_persist_only_own_boolean_setting(self):
        self.plugin.command(self.ctx, "off")
        self.plugin.command(self.ctx, "on")
        self.assertEqual(self.ctx.writes, [("enabled", False), ("enabled", True)])

    def test_invalid_command_does_not_write_or_run_task(self):
        self.assertIn("Usage", self.plugin.command(self.ctx, "review; delete files"))
        self.assertEqual(self.ctx.writes, [])

    def test_status_is_read_only_and_discloses_guidance_not_enforcement(self):
        data = self.plugin.status(self.ctx)
        self.assertTrue(data["enabled"])
        self.assertEqual(data["policy_kind"], "guidance-not-permission-enforcement")
        self.assertEqual(self.ctx.writes, [])

    def test_cli_parser_limits_actions(self):
        parser = argparse.ArgumentParser()
        self.plugin.setup_cli(parser)
        self.assertEqual(parser.parse_args([]).action, "status")
        self.assertEqual(parser.parse_args(["off"]).action, "off")


class BundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin = load_plugin()

    def test_catalog_exact_families_and_metadata(self):
        catalog = self.plugin.catalog()
        expected = {"evidence", "diagnose", "impact", "design", "reliability", "review", "verify", "measure", "evaluate", "handoff", "learn", "explain", "formal", "work", "compare", "git"}
        self.assertEqual(set(catalog), expected)
        for name, description in catalog.items():
            self.assertLessEqual(len(description), 60)
            self.assertTrue(description.endswith("."))
            text = (PACKAGE / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn("name: " + name, text.split("\n---\n", 1)[0])
            self.assertIn(description, text.split("\n---\n", 1)[0])
            for section in ["When to Use", "Procedure", "Pitfalls", "Verification"]:
                self.assertIn(section, text, (name, section))

    def test_native_registration_is_inert_and_described(self):
        ctx = Context()
        self.plugin.register(ctx)
        self.assertEqual(set(ctx.hooks), {"pre_llm_call"})
        self.assertEqual(set(ctx.commands), {"pstack"})
        self.assertEqual(set(ctx.cli), {"pstack"})
        self.assertEqual(len(ctx.skills), 16)
        self.assertTrue(all(path.is_file() and description for path, description in ctx.skills.values()))
        self.assertEqual(ctx.writes, [])
        on = ctx.hooks["pre_llm_call"](conversation_history=[])
        self.assertIn("PSTACK", on["context"])
        ctx.commands["pstack"]("off")
        self.assertIsNone(ctx.hooks["pre_llm_call"](conversation_history=[]))

    def test_shared_replacement_rules_preserve_user_authority(self):
        text = (PACKAGE / "policy.md").read_text(encoding="utf-8")
        for phrase in ["Ground Rule", "Core", "source/", "Ponytail", "scope", "evidence", "approval", "profile"]:
            self.assertIn(phrase, text)
        self.assertLess(len(text), 6500)

    def test_catalog_identifiers_cannot_escape_package(self):
        for name in self.plugin.catalog():
            self.assertRegex(name, r"^[a-z][a-z0-9-]*$")
            self.assertEqual((PACKAGE / "skills" / name / "SKILL.md").resolve().parents[2], PACKAGE.resolve())


if __name__ == "__main__":
    unittest.main()
