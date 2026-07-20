"""Run durable Jeff Strict SSOT V1 package acceptance in an explicit output root."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def environment_identity() -> dict[str, str]:
    return {
        "machine": platform.node() or "unknown_machine",
        "os": platform.platform(),
        "runtime": sys.version.replace("\n", " "),
    }


def relative_to(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def run_command(
    command: list[str],
    cwd: Path,
    output: Path,
    sequence: int,
    claim: str,
    artifacts: list[Path] | None = None,
) -> tuple[dict[str, Any], Path]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    prefix = f"{sequence:02d}"
    stdout_path = output / f"{prefix}_stdout.txt"
    stderr_path = output / f"{prefix}_stderr.txt"
    stdout_path.write_text(result.stdout, encoding="utf-8")
    stderr_path.write_text(result.stderr, encoding="utf-8")
    artifact_records = []
    for path in artifacts or []:
        if path.is_file():
            artifact_records.append({"path": relative_to(output, path), "sha256": sha256(path)})
    record = {
        "schema_version": 1,
        "evidence_class": "protocol",
        "timestamp_utc": utc_now(),
        "working_directory": str(cwd.resolve()),
        "command": command,
        "exit_code": result.returncode,
        "environment": environment_identity(),
        "supported_claim": claim,
        "stdout": {"inline": None, "path": relative_to(output, stdout_path), "sha256": sha256(stdout_path)},
        "stderr": {"inline": None, "path": relative_to(output, stderr_path), "sha256": sha256(stderr_path)},
        "artifacts": artifact_records,
        "authority_effect": "none",
        "limitations": ["protocol evidence only", "does not validate product behavior"],
    }
    record_path = output / f"{prefix}_run_record.json"
    record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record, record_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args(argv)

    package = args.package_root.resolve()
    output = args.output_root.resolve()
    if output.exists() and any(output.iterdir()):
        print("acceptance_error: output root must be nonexistent or empty", file=sys.stderr)
        return 2
    output.mkdir(parents=True, exist_ok=True)
    release_errors: list[str] = []
    release_path = package / "RELEASE.json"
    try:
        release = json.loads(release_path.read_text(encoding="utf-8"))
        expected_release_fields = {
            "schema_version",
            "package_name",
            "package_version",
            "bootstrap_sha256",
            "manifest_sha256",
            "authentication_boundary",
        }
        if set(release) != expected_release_fields or release.get("schema_version") != 1:
            release_errors.append("RELEASE.json schema/fields mismatch")
        if release.get("bootstrap_sha256") != sha256(package / "bootstrap.py"):
            release_errors.append("bootstrap.py does not match RELEASE.json")
        if release.get("manifest_sha256") != sha256(package / "MANIFEST.json"):
            release_errors.append("MANIFEST.json does not match RELEASE.json")
        manifest_identity = json.loads(
            (package / "MANIFEST.json").read_text(encoding="utf-8")
        )
        for field in ("package_name", "package_version"):
            if release.get(field) != manifest_identity.get(field):
                release_errors.append(f"RELEASE.json/MANIFEST.json {field} mismatch")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        release_errors.append(f"RELEASE.json unreadable: {exc}")
    install = output / "installed_repository"
    dry_target = output / "dry_run_target"
    python = sys.executable
    command_records: list[dict[str, Any]] = []
    record_paths: list[Path] = []

    def execute(command: list[str], cwd: Path, claim: str, artifacts: list[Path] | None = None) -> None:
        record, path = run_command(command, cwd, output, len(command_records) + 1, claim, artifacts)
        command_records.append(record)
        record_paths.append(path)

    dry_command = [python, "-B", str(package / "bootstrap.py"), "--target", str(dry_target), "--project-name", "Acceptance Fixture", "--date", args.date, "--dry-run"]
    execute(dry_command, package, "first dry-run succeeds without writing target")
    execute(dry_command, package, "repeated dry-run is byte-deterministic and writes no target")
    dry_run_wrote_target = dry_target.exists()
    dry_run_outputs_identical = (
        (output / "01_stdout.txt").read_bytes() == (output / "02_stdout.txt").read_bytes()
        and (output / "01_stderr.txt").read_bytes() == (output / "02_stderr.txt").read_bytes()
    )

    install_command = [python, "-B", str(package / "bootstrap.py"), "--target", str(install), "--project-name", "Acceptance Fixture", "--date", args.date]
    execute(install_command, package, "fresh install succeeds", [install / "JEFF_STRICT_SSOT_INSTALL.json"])
    install_manifest_path = install / "JEFF_STRICT_SSOT_INSTALL.json"
    package_manifest = json.loads((package / "MANIFEST.json").read_text(encoding="utf-8"))
    expected_installed = set(package_manifest["template_files"]) | {"JEFF_STRICT_SSOT_INSTALL.json"}
    actual_installed = {
        path.relative_to(install).as_posix()
        for path in install.rglob("*")
        if path.is_file()
    }
    installed_missing = sorted(expected_installed - actual_installed)
    installed_unexpected = sorted(actual_installed - expected_installed)

    execute(
        [python, "-B", str(install / "scripts/ssot/validate_protocol.py"), "--root", str(install), "--strict"],
        install,
        "generated protocol validator passes clean fixture",
    )
    execute(
        [python, "-B", str(install / "scripts/ssot/validate_governor_delta_policy.py"), "--root", str(install), "--strict"],
        install,
        "generated Governor policy validator passes clean fixture",
    )
    execute(
        [python, "-B", "-m", "unittest", "discover", "-s", str(install / "tests/ssot"), "-v"],
        install,
        "generated repository tests pass",
    )
    execute(
        [python, "-B", "-m", "unittest", "discover", "-s", str(package / "tests"), "-p", "test_*.py", "-v"],
        package,
        "package tests pass",
    )
    execute(install_command, package, "second fresh install is refused without changing installed state")

    evidence_command = [
        python,
        "-B",
        str(install / "scripts/ssot/validate_protocol.py"),
        "--root",
        str(output),
        "--strict",
        "--evidence-only",
    ]
    for path in record_paths:
        evidence_command.extend(["--evidence", str(path)])
    execute(evidence_command, output, "generated command run records conform to bounded evidence schema")

    validator_path = install / "scripts/ssot/validate_protocol.py"
    spec = importlib.util.spec_from_file_location("acceptance_validator", validator_path)
    if not spec or not spec.loader:
        raise RuntimeError("cannot load generated validator for final record check")
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    in_process_record_errors: dict[str, list[str]] = {}
    for path in record_paths:
        errors = validator.validate_evidence(path, output)
        if errors:
            in_process_record_errors[path.name] = errors

    install_manifest = json.loads(install_manifest_path.read_text(encoding="utf-8")) if install_manifest_path.is_file() else {}
    hash_mismatches: list[str] = []
    installed_files: list[dict[str, Any]] = []
    for item in install_manifest.get("files", []):
        path = install / item["path"]
        actual = sha256(path) if path.is_file() else None
        installed_files.append({"path": item["path"], "expected": item["rendered_sha256"], "actual": actual})
        if actual != item["rendered_sha256"]:
            hash_mismatches.append(item["path"])

    expected_codes = [0, 0, 0, 0, 0, 0, 0, 2, 0]
    actual_codes = [item["exit_code"] for item in command_records]
    package_files = sorted(path for path in package.rglob("*") if path.is_file())
    unexpected_package_cache = sorted(
        path.relative_to(package).as_posix()
        for path in package_files
        if "__pycache__" in path.parts or path.suffix.lower() == ".pyc"
    )
    passed = (
        actual_codes == expected_codes
        and not dry_run_wrote_target
        and dry_run_outputs_identical
        and not hash_mismatches
        and not installed_missing
        and not installed_unexpected
        and not in_process_record_errors
        and not release_errors
        and not unexpected_package_cache
    )
    aggregate = {
        "schema": "jeff_strict_ssot_acceptance_aggregate_v1",
        "timestamp_utc": utc_now(),
        "package_root": str(package),
        "output_root": str(output),
        "supported_claim": "Jeff Strict SSOT V1 dry-run/install/hash/validator/test/evidence/overwrite acceptance",
        "command_records": [
            {"path": relative_to(output, path), "sha256": sha256(path), "exit_code": record["exit_code"]}
            for path, record in zip(record_paths, command_records)
        ],
        "expected_exit_codes": expected_codes,
        "actual_exit_codes": actual_codes,
        "dry_run_wrote_target": dry_run_wrote_target,
        "dry_run_outputs_identical": dry_run_outputs_identical,
        "installed_missing": installed_missing,
        "installed_unexpected": installed_unexpected,
        "installed_hash_mismatches": hash_mismatches,
        "installed_files": installed_files,
        "installed_expected_paths": sorted(expected_installed),
        "installed_actual_paths": sorted(actual_installed),
        "record_validation_errors": in_process_record_errors,
        "release_validation_errors": release_errors,
        "package_files": [
            {"path": path.relative_to(package).as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in package_files
        ],
        "unexpected_package_cache": unexpected_package_cache,
        "status": "passed" if passed else "failed",
        "authority_effect": "package_candidate_evidence_only",
        "limitations": [
            "aggregate is an index, not a command run record",
            "does not validate a product",
            "does not activate the Governor",
            "does not modify CROCHET or SPLATOMATIC",
            "independent Red Team review remains required",
        ],
    }
    aggregate_path = output / "acceptance_aggregate.json"
    aggregate_path.write_text(json.dumps(aggregate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = (
        "# Jeff Strict SSOT V1 Acceptance\n\n"
        f"- Status: `{aggregate['status']}`\n"
        f"- Commands: `{len(command_records)}`\n"
        f"- Command records validated: `{len(record_paths) - len(in_process_record_errors)}/{len(record_paths)}`\n"
        f"- Installed payload hashes verified: `{len(installed_files)}`\n"
        f"- Exact installed regular-file tree: `{len(actual_installed)}/{len(expected_installed)}`\n"
        f"- Missing/unexpected/hash mismatch: `{len(installed_missing)}/{len(installed_unexpected)}/{len(hash_mismatches)}`\n"
        f"- Repeated dry-run identical: `{str(dry_run_outputs_identical).lower()}`\n"
        f"- Dry-run wrote target: `{str(dry_run_wrote_target).lower()}`\n"
        "- Authority effect: `package_candidate_evidence_only`\n"
    )
    (output / "acceptance_summary.md").write_text(summary, encoding="utf-8")
    print(json.dumps({"status": aggregate["status"], "aggregate": str(aggregate_path)}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
