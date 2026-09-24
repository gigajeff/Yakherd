"""Read-only structural checks. Never import or execute a target repository."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


OWNERS = {"instructions": "AGENTS.md", "mission": "SSOT.md", "baseline": "BASELINE.md",
          "current": "NOW.md", "usage": "README.md"}
MAX_DOCUMENT_BYTES = 2 * 1024 * 1024
LEGACY_RECEIPT = "JEFF_STRICT_SSOT_INSTALL.json"


def inspect(target: Path, engine: object, *, overrides: dict[str, bytes] | None = None) -> dict:
    """Inspect bounded local files using the installer's containment checks."""
    errors: list[str] = []
    warnings: list[str] = []
    root = target.absolute()
    overlay = overrides or {}
    report = {"schema_version": 3, "target": str(root), "status": "not_ready",
              "errors": errors, "warnings": warnings,
              "claim": "repository structure only; no product correctness or authority claim"}
    try:
        engine.validate_existing_chain(root)
        if not root.is_dir():
            raise ValueError("target is not a directory")
        if any(p.name.startswith(engine.RETROFIT_TXN_PREFIX) for p in root.iterdir()):
            errors.append("unresolved migration journal; inspect recovery before another migration")
        if os.path.lexists(root / engine.RETROFIT_LOCK_NAME):
            errors.append("migration lock present; inspect its owner before changing files")

        def read(relative: str) -> str:
            path = engine.safe_destination(root, relative)
            if relative in overlay:
                if len(overlay[relative]) > MAX_DOCUMENT_BYTES:
                    raise ValueError(f"document exceeds inspection bound: {relative}")
                return overlay[relative].decode("utf-8")
            if not path.is_file():
                raise ValueError(f"missing regular file: {relative}")
            if path.stat().st_size > MAX_DOCUMENT_BYTES:
                raise ValueError(f"document exceeds inspection bound: {relative}")
            return path.read_bytes().decode("utf-8")

        if ".yakherd/profile.json" not in overlay and not os.path.lexists(root / ".yakherd/profile.json"):
            if os.path.lexists(root / LEGACY_RECEIPT):
                raise ValueError("legacy Yakherd installation; use a reviewed v3 migration, not setup")
            raise ValueError("no Yakherd 3 profile; use setup for new paths or a reviewed migration")
        profile = json.loads(read(".yakherd/profile.json"))
        if (not isinstance(profile, dict) or profile.get("schema_version") != 3
                or profile.get("profile") != "yakherd-ssot" or profile.get("owners") != OWNERS):
            raise ValueError("unsupported profile or owner map")
        receipt = json.loads(read(engine.INSTALL_MANIFEST_NAME))
        if (not isinstance(receipt, dict) or receipt.get("schema_version") != 1
                or receipt.get("package_name") != "yakherd_ssot"
                or receipt.get("package_version") != "3.0.0"):
            raise ValueError("missing or unsupported v3 installation receipt")
        texts = {}
        for name in [*OWNERS.values(), "START_HERE.md", ".yakherd/policies/Y-PROC-1.md"]:
            try:
                text = read(name)
                texts[name] = text
                if not text.strip():
                    errors.append(f"empty owner: {name}")
                if re.search(r"\{\{[A-Z][A-Z0-9_]*\}\}", text):
                    errors.append(f"unresolved template placeholder: {name}")
                # Code examples and external citations are not local ownership links.
                prose = re.sub(r"```.*?```", "", text, flags=re.S)
                for link in re.findall(r"!?\[[^\]\n]*\]\(([^)\n]+)\)", prose):
                    link = link.strip("<>")
                    parsed = urlsplit(link)
                    if parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    decoded = unquote(parsed.path)
                    candidate = Path(name).parent / decoded
                    # Resolve '..' only after proving the final location is within root.
                    absolute = Path(os.path.abspath(root / candidate))
                    try:
                        relative = absolute.relative_to(root).as_posix()
                        linked = engine.safe_destination(root, relative)
                        if relative not in overlay and not linked.exists():
                            errors.append(f"broken local link: {name} -> {link}")
                    except (ValueError, engine.BootstrapError):
                        errors.append(f"unsafe local link: {name} -> {link}")
            except (OSError, ValueError, UnicodeError, engine.BootstrapError) as exc:
                errors.append(str(exc))
        now = texts.get("NOW.md", "")
        headings = re.findall(r"^## (.+)$", now, flags=re.M)
        for heading in ("Objective", "Scope", "Definition of Done", "Current state and blockers", "Next executable action"):
            if headings.count(heading) != 1:
                errors.append(f"NOW.md needs exactly one '{heading}' section")
        if now.startswith("# INITIAL:"):
            warnings.append("initial scaffold: adopt the user's product objective in NOW.md; no product readiness claimed")
        if ("CLAUDE.md" in overlay or os.path.lexists(root / "CLAUDE.md")) and read("CLAUDE.md").strip() != "@AGENTS.md":
            warnings.append("CLAUDE.md contains additional instructions; inspect for competing authority")
        for name in ("AGENTS.md", "START_HERE.md", "SSOT.md", "docs/task_protocol.md",
                     "docs/prompts/codex_team_launcher.md"):
            if name not in overlay and not os.path.lexists(root / name):
                continue
            text = read(name)
            if text.startswith("<!-- YAKHERD-LEGACY-ARCHIVE -->"):
                continue
            if any(phrase in text for phrase in ("Create exactly five direct role agents",
                                                "Creation of all five roles is a startup invariant",
                                                "must not capture or extract the product prompt before bootstrap")):
                errors.append(f"active legacy startup instructions remain: {name}")
        report["status"] = "not_ready" if errors else "ready"
    except (OSError, ValueError, UnicodeError, engine.BootstrapError) as exc:
        errors.append(str(exc))
    return report
