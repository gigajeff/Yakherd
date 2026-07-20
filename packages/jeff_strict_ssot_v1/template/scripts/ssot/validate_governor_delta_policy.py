"""Read-only validation for the Jeff Strict SSOT Governor delta policy."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


EXPECTED = {
    "quiet": {"max_lines": 2, "max_utf8_bytes": 512, "writes_allowed": False},
    "delta": {"max_lines": 120, "max_utf8_bytes": 16384, "writes_allowed": True},
    "rebaseline": {
        "max_lines": 240,
        "max_utf8_bytes": 32768,
        "writes_allowed": True,
    },
}


def validate(root: Path) -> list[str]:
    path = root / "docs/governance/GOVERNOR_DELTA_POLICY.json"
    errors: list[str] = []
    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"governor policy unreadable: {exc}"]
    if data.get("schema_version") != 1:
        errors.append("governor schema_version must be 1")
    if data.get("authority_effect") != "none":
        errors.append("Governor authority_effect must be none")
    if data.get("automation_created") is not False:
        errors.append("bootstrap must not create Governor automation")
    if data.get("cadence") is not None:
        errors.append("bootstrap Governor cadence must be null")
    modes = data.get("modes")
    if not isinstance(modes, dict):
        return errors + ["Governor modes must be an object"]
    for name, expected in EXPECTED.items():
        actual = modes.get(name)
        if not isinstance(actual, dict):
            errors.append(f"missing Governor mode: {name}")
            continue
        for key, value in expected.items():
            if actual.get(key) != value:
                errors.append(f"Governor {name}.{key} must equal {value!r}")
    requirements = modes.get("rebaseline", {}).get("requires", [])
    if set(requirements) != {
        "broken_history_continuity",
        "explicit_human_authorization",
    }:
        errors.append("rebaseline requires exact continuity/authorization gates")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    errors = validate(args.root.resolve())
    for error in errors:
        print(f"error: {error}")
    print(f"governor_policy status={'passed' if not errors else 'failed'} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
