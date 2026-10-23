# PStack for Hermes

This native Hermes package provides automatic scope-preserving engineering guidance and 16 on-demand adapted skills. It does not enforce permissions, change Core, install dependencies, execute business tasks, or alter other profiles.

Installation:

```text
hermes plugins install gary3207/Hermes_PlugIn_pstack/source/pstack --enable
hermes pstack status
```

Start a new Hermes process/conversation after installation. Use `hermes pstack on|off|skills|status` or `/pstack` in a loaded session. The only user setting is the profile-local boolean `plugins.entries.pstack.settings.enabled` (default `true`). An off setting is preserved until explicitly changed; it does not disable explicitly requested skills.

See the repository README and `source/docs/SELECTION.md` for Korean setup, restoration scope, verification, and all upstream-to-adaptation mappings. Read `policy.md` for the actual shared guidance and `NOTICE.md`/`LICENSE` for attribution. Existing user Ground Rules, security controls, and Ponytail take precedence.
