"""Native Hermes guidance plugin; no tools, network, or task execution."""
from __future__ import annotations

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
VERSION = "1.0.0"
OFF_CONTEXT = (
    "HERMES PSTACK v1.0.0: off\n"
    "PStack automatic guidance is off. Do not keep applying earlier PStack-only "
    "routing instructions automatically. Existing user Ground Rules, safety "
    "requirements, and other enabled plugins remain in effect. Explicitly "
    "requested PStack skills remain available."
)


def catalog() -> dict[str, str]:
    data = json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("pstack skills.json must be an object")
    for name, description in data.items():
        if not re.fullmatch(r"[a-z][a-z0-9-]*", name) or not isinstance(description, str) or not description:
            raise ValueError("pstack skills.json contains an invalid skill entry")
    return data


def is_enabled(ctx) -> bool:
    value = ctx.get_config("enabled", True)
    if type(value) is not bool:
        raise ValueError("plugins.entries.pstack.settings.enabled must be a boolean")
    return value


def _user_text(message) -> str:
    if not isinstance(message, dict) or message.get("role") != "user":
        return ""
    value = message.get("api_content")
    if value is None:
        value = message.get("content", "")
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(
            part["text"] for part in value
            if isinstance(part, dict) and isinstance(part.get("text"), str)
        )
    return ""


def build_context(enabled: bool, conversation_history=None):
    on_context = "HERMES PSTACK v1.0.0: on\n" + (ROOT / "policy.md").read_text(encoding="utf-8")
    desired = on_context if enabled else OFF_CONTEXT
    for message in reversed(conversation_history or []):
        text = _user_text(message)
        on_position, off_position = text.rfind(on_context), text.rfind(OFF_CONTEXT)
        if on_position >= 0 or off_position >= 0:
            previous_enabled = on_position > off_position
            return None if previous_enabled == enabled else {"context": desired}
    return {"context": desired} if enabled else None


def status(ctx) -> dict:
    return {
        "plugin": "pstack",
        "version": VERSION,
        "enabled": is_enabled(ctx),
        "policy_kind": "guidance-not-permission-enforcement",
        "scope": "active Hermes profile only",
        "settings_key": "plugins.entries.pstack.settings.enabled",
        "activation": "new processes discover newly installed plugins",
    }


def command(ctx, raw_args: str = "") -> str:
    action = (raw_args or "").strip().lower() or "status"
    if action in {"on", "off"}:
        ctx.set_config("enabled", action == "on")
        return json.dumps(status(ctx), ensure_ascii=False, indent=2)
    if action == "status":
        return json.dumps(status(ctx), ensure_ascii=False, indent=2)
    if action == "skills":
        return json.dumps({"pstack:" + key: value for key, value in catalog().items()}, ensure_ascii=False, indent=2)
    return "Usage: /pstack [status|on|off|skills]. Task skills: skill_view('pstack:<name>')."


def setup_cli(parser) -> None:
    parser.add_argument("action", nargs="?", default="status", choices=["status", "on", "off", "skills"])


def register(ctx) -> None:
    for name, description in catalog().items():
        ctx.register_skill(name, ROOT / "skills" / name / "SKILL.md", description=description)

    def pre_llm_call(conversation_history=None, **kwargs):
        return build_context(is_enabled(ctx), conversation_history)

    def handle_command(raw_args="", **kwargs):
        return command(ctx, raw_args)

    def handle_cli(args):
        print(command(ctx, args.action))

    ctx.register_hook("pre_llm_call", pre_llm_call)
    ctx.register_command("pstack", handle_command, description="Inspect or toggle PStack guidance.", args_hint="[status|on|off|skills]", argument_mode="options")
    ctx.register_cli_command("pstack", help="Inspect or toggle PStack guidance.", setup_fn=setup_cli, handler_fn=handle_cli)
