"""Windows acceptance and portable policy tests for Y-PROC-1."""

from __future__ import annotations

import ctypes
import json
import os
import signal
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yakherd import process_hygiene as hygiene  # noqa: E402


class FiniteCommandPolicyTests(unittest.TestCase):
    def test_finite_forms_are_allowed(self) -> None:
        allowed = [
            ["python", "-c", "print('finite')"],
            ["python", "script.py"],
            ["node", "-e", "console.log('finite')"],
            ["cmd", "/c", "echo", "finite"],
            ["powershell", "-Command", "Write-Output finite"],
            ["npm", "test"],
            ["tsc", "--noEmit"],
        ]
        for command in allowed:
            with self.subTest(command=command):
                hygiene.validate_finite_command(command)

    def test_interactive_detached_and_watch_forms_are_rejected(self) -> None:
        rejected = [
            ["node"],
            ["node_repl.exe"],
            ["python"],
            ["py", "-3"],
            ["cmd", "/K"],
            ["powershell", "-NoExit", "-Command", "echo x"],
            ["powershell", "-Command", "Start-Job { echo x }"],
            ["powershell", "-Command", "Start-Process tool.exe"],
            ["cmd", "/c", "start", "tool.exe"],
            ["cmd", "/c", "start tool.exe"],
            ["powershell", "-Command", "npm run dev"],
            ["powershell", "-Command", "& npm run dev"],
            ["cmd", "/c", "npm run dev"],
            ["bash", "-c", "npm run dev"],
            ["npm", "run", "dev"],
            ["vite"],
            ["nodemon", "app.js"],
            ["webpack", "serve"],
            ["tsc", "-w"],
            ["dotnet", "watch"],
            ["tool", "--daemon"],
        ]
        for command in rejected:
            with self.subTest(command=command):
                with self.assertRaises(hygiene.ProcessPolicyError):
                    hygiene.validate_finite_command(command)

    def test_exec_fails_closed_off_windows(self) -> None:
        if os.name == "nt":
            self.skipTest("non-Windows fail-closed check")
        with self.assertRaises(hygiene.ProcessPolicyError):
            hygiene.run_broker(
                [sys.executable, "-c", "print('x')"],
                cwd=ROOT,
                classification="light",
                timeout_seconds=1,
                queue_timeout_seconds=1,
                owner=None,
            )


@unittest.skipUnless(os.name == "nt", "Y-PROC-1 Job Object acceptance requires Windows")
class WindowsProcessHygieneTests(unittest.TestCase):
    def setUp(self) -> None:
        (ROOT / ".tmp").mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=ROOT / ".tmp")
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def broker(
        self,
        command: list[str],
        *,
        classification: str = "light",
        timeout: float = 10,
    ) -> int:
        return hygiene.run_broker(
            command,
            cwd=ROOT,
            classification=classification,
            timeout_seconds=timeout,
            queue_timeout_seconds=10,
            owner="test-suite",
            root=self.root,
        )

    def records(self) -> list[dict[str, object]]:
        records, errors = hygiene.load_tasks(self.root)
        self.assertEqual(errors, [])
        return records

    def wait_for(self, predicate: object, timeout: float = 10) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():  # type: ignore[operator]
                return
            time.sleep(0.05)
        self.fail("condition did not become true before timeout")

    def cli_process(
        self, args: list[str], *, stdin: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ)
        environment["YAKHERD_PROCESS_STATE"] = str(self.root)
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "yakherd.py"), *args],
            cwd=ROOT,
            env=environment,
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
            timeout=20,
        )

    def test_finite_command_records_identity_and_cleans_job(self) -> None:
        code = self.broker([sys.executable, "-B", "-c", "print('finite')"])
        self.assertEqual(code, 0)
        record = self.records()[0]
        self.assertEqual(record["state"], "completed")
        self.assertTrue(record["cleanup"]["verified_zero"])  # type: ignore[index]
        top = record["top_process"]
        self.assertIsInstance(top, dict)
        self.assertIsInstance(top["creation_time_100ns"], int)  # type: ignore[index]
        self.assertTrue(top["executable"])  # type: ignore[index]
        self.assertEqual(record["lifecycle"], "finite")

    def test_atomic_containment_verification_failure_terminates_child(self) -> None:
        with mock.patch.object(
            hygiene.WindowsJob,
            "contains",
            return_value=False,
        ):
            code = self.broker(
                [sys.executable, "-B", "-c", "import time; time.sleep(30)"]
            )
        record = self.records()[0]
        self.assertEqual(code, 1, record)
        self.assertEqual(record["state"], "failed")
        self.assertTrue(record["cleanup"]["verified_zero"])  # type: ignore[index]
        self.assertIn(
            "outside the required Job Object", str(record["execution_error"])
        )

    def test_first_child_instruction_observes_job_membership(self) -> None:
        result_path = self.root / "atomic-membership.txt"
        script = (
            "import ctypes,pathlib; "
            "k=ctypes.WinDLL('kernel32',use_last_error=True); "
            "k.GetCurrentProcess.restype=ctypes.c_void_p; "
            "k.IsProcessInJob.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)]; "
            "k.IsProcessInJob.restype=ctypes.c_int; "
            "v=ctypes.c_int(); "
            "ok=k.IsProcessInJob(k.GetCurrentProcess(),None,ctypes.byref(v)); "
            f"pathlib.Path({str(result_path)!r}).write_text(str(int(bool(ok) and bool(v.value))),encoding='utf-8')"
        )
        self.assertEqual(self.broker([sys.executable, "-B", "-c", script]), 0)
        self.assertEqual(result_path.read_text(encoding="utf-8"), "1")

    def test_finite_batch_file_runs_inside_atomic_job(self) -> None:
        script = self.root / "finite command.cmd"
        output = self.root / "batch-output.txt"
        script.write_text(f"@echo finite>\"{output}\"\n", encoding="utf-8")
        self.assertEqual(self.broker([str(script)]), 0)
        self.assertEqual(output.read_text(encoding="utf-8").strip(), "finite")

    def test_nonfinite_timeouts_fail_closed(self) -> None:
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(hygiene.ProcessPolicyError):
                    hygiene.run_broker(
                        [sys.executable, "-B", "-c", "pass"],
                        cwd=ROOT,
                        classification="light",
                        timeout_seconds=value,
                        queue_timeout_seconds=10,
                        owner="test-suite",
                        root=self.root,
                    )

    def test_internal_parallel_children_are_allowed_and_cleaned(self) -> None:
        script = (
            "import subprocess,sys; "
            "ps=[subprocess.Popen([sys.executable,'-B','-c','pass']) for _ in range(8)]; "
            "[p.wait() for p in ps]"
        )
        self.assertEqual(self.broker([sys.executable, "-B", "-c", script]), 0)
        self.assertTrue(self.records()[0]["cleanup"]["verified_zero"])  # type: ignore[index]

    def test_parent_exit_before_child_still_kills_child(self) -> None:
        child_pid_path = self.root / "child.pid"
        child_script = "import time; time.sleep(30)"
        parent_script = (
            "import pathlib,subprocess,sys; "
            f"p=subprocess.Popen([sys.executable,'-B','-c',{child_script!r}]); "
            f"pathlib.Path({str(child_pid_path)!r}).write_text(str(p.pid),encoding='utf-8')"
        )
        self.assertEqual(self.broker([sys.executable, "-B", "-c", parent_script]), 0)
        child_pid = int(child_pid_path.read_text(encoding="utf-8"))
        self.assertIsNone(hygiene.process_identity(child_pid))

    def test_timeout_terminates_entire_nested_tree(self) -> None:
        child_pid_path = self.root / "timeout-child.pid"
        child_script = "import time; time.sleep(30)"
        parent_script = (
            "import pathlib,subprocess,sys,time; "
            f"p=subprocess.Popen([sys.executable,'-B','-c',{child_script!r}]); "
            f"pathlib.Path({str(child_pid_path)!r}).write_text(str(p.pid),encoding='utf-8'); "
            "time.sleep(30)"
        )
        code = self.broker([sys.executable, "-B", "-c", parent_script], timeout=0.5)
        self.assertEqual(code, 124)
        child_pid = int(child_pid_path.read_text(encoding="utf-8"))
        self.assertIsNone(hygiene.process_identity(child_pid))
        record = self.records()[0]
        self.assertEqual(record["state"], "timed_out")
        self.assertTrue(record["cleanup"]["verified_zero"])  # type: ignore[index]

    def test_heavy_process_uses_below_normal_priority(self) -> None:
        self.assertEqual(
            self.broker(
                [sys.executable, "-B", "-c", "import time; time.sleep(0.2)"],
                classification="heavy",
            ),
            0,
        )
        top = self.records()[0]["top_process"]
        self.assertEqual(top["priority_class"], hygiene.BELOW_NORMAL_PRIORITY_CLASS)  # type: ignore[index]

    def test_simultaneous_heavy_requests_queue_instead_of_overlap(self) -> None:
        first_start = self.root / "first-start"
        first_end = self.root / "first-end"
        second_start = self.root / "second-start"
        second_end = self.root / "second-end"

        def command(start: Path, end: Path) -> list[str]:
            script = (
                "import pathlib,time; "
                f"pathlib.Path({str(start)!r}).write_text(str(time.time()),encoding='utf-8'); "
                "time.sleep(0.7); "
                f"pathlib.Path({str(end)!r}).write_text(str(time.time()),encoding='utf-8')"
            )
            return [
                sys.executable,
                "-B",
                str(ROOT / "yakherd.py"),
                "exec",
                "--heavy",
                "--timeout",
                "10",
                "--queue-timeout",
                "10",
                "--",
                sys.executable,
                "-B",
                "-c",
                script,
            ]

        environment = dict(os.environ)
        environment["YAKHERD_PROCESS_STATE"] = str(self.root)
        first = subprocess.Popen(command(first_start, first_end), cwd=ROOT, env=environment)
        try:
            self.wait_for(first_start.exists)
            second = subprocess.Popen(command(second_start, second_end), cwd=ROOT, env=environment)
            try:
                self.assertEqual(first.wait(timeout=15), 0)
                self.assertEqual(second.wait(timeout=15), 0)
            finally:
                if second.poll() is None:
                    second.terminate()
                    second.wait(timeout=5)
        finally:
            if first.poll() is None:
                first.terminate()
                first.wait(timeout=5)
        first_finished = float(first_end.read_text(encoding="utf-8"))
        second_started = float(second_start.read_text(encoding="utf-8"))
        self.assertGreaterEqual(second_started, first_finished - 0.05)

    def test_broker_abnormal_exit_triggers_job_kill_and_reconciliation(self) -> None:
        environment = dict(os.environ)
        environment["YAKHERD_PROCESS_STATE"] = str(self.root)
        broker = subprocess.Popen(
            [
                sys.executable,
                "-B",
                str(ROOT / "yakherd.py"),
                "exec",
                "--light",
                "--timeout",
                "30",
                "--",
                sys.executable,
                "-B",
                "-c",
                "import time; time.sleep(30)",
            ],
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            def running_record() -> bool:
                records, _ = hygiene.load_tasks(self.root)
                if broker.poll() is not None:
                    stdout, stderr = broker.communicate()
                    self.fail(
                        f"broker exited before running state code={broker.returncode} "
                        f"stdout={stdout!r} stderr={stderr!r} records={records!r}"
                    )
                return bool(records and records[0].get("state") == "running")

            self.wait_for(running_record)
            record = self.records()[0]
            child_pid = int(record["top_process"]["pid"])  # type: ignore[index]
            broker.terminate()
            broker.wait(timeout=5)
            self.wait_for(lambda: hygiene.process_identity(child_pid) is None)
            report = hygiene.reconcile(self.root, dry_run=False)
            self.assertFalse(report["ambiguous"])
            self.assertEqual(self.records()[0]["state"], "reconciled")
        finally:
            if broker.poll() is None:
                broker.terminate()
                broker.wait(timeout=5)
            broker.communicate(timeout=5)

    def test_direct_ctrl_break_cancellation_cleans_entire_job(self) -> None:
        environment = dict(os.environ)
        environment["YAKHERD_PROCESS_STATE"] = str(self.root)
        broker = subprocess.Popen(
            [
                sys.executable,
                "-B",
                str(ROOT / "yakherd.py"),
                "exec",
                "--light",
                "--timeout",
                "30",
                "--",
                sys.executable,
                "-B",
                "-c",
                "import time; time.sleep(30)",
            ],
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
        try:
            self.wait_for(
                lambda: bool(
                    self.records()
                    and self.records()[0].get("state") == "running"
                )
            )
            record = self.records()[0]
            child_pid = int(record["top_process"]["pid"])  # type: ignore[index]
            os.kill(broker.pid, signal.CTRL_BREAK_EVENT)
            stdout, stderr = broker.communicate(timeout=10)
            self.assertEqual(
                broker.returncode,
                130,
                f"stdout={stdout!r} stderr={stderr!r} record={self.records()[0]!r}",
            )
            self.assertIsNone(hygiene.process_identity(child_pid))
            final = self.records()[0]
            self.assertEqual(final["state"], "cancelled")
            self.assertTrue(final["cleanup"]["verified_zero"])  # type: ignore[index]
        finally:
            if broker.poll() is None:
                broker.terminate()
                broker.wait(timeout=5)
            broker.communicate(timeout=5)

    def test_stop_hook_cancels_only_matching_session_tasks(self) -> None:
        environment = dict(os.environ)
        environment["YAKHERD_PROCESS_STATE"] = str(self.root)
        environment["CODEX_THREAD_ID"] = "hook-session"
        broker = subprocess.Popen(
            [
                sys.executable,
                "-B",
                str(ROOT / "yakherd.py"),
                "exec",
                "--light",
                "--timeout",
                "30",
                "--",
                sys.executable,
                "-B",
                "-c",
                "import time; time.sleep(30)",
            ],
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            self.wait_for(
                lambda: bool(
                    self.records()
                    and self.records()[0].get("state") == "running"
                )
            )
            record = self.records()[0]
            self.assertEqual(record["owner"], "codex:hook-session")
            child_pid = int(record["top_process"]["pid"])  # type: ignore[index]
            hook = self.cli_process(
                ["process", "hook"],
                stdin=json.dumps(
                    {
                        "hook_event_name": "Stop",
                        "session_id": "hook-session",
                        "turn_id": "hook-turn",
                        "cwd": str(ROOT),
                    }
                ),
            )
            self.assertEqual(hook.returncode, 0, hook.stderr)
            self.assertTrue(json.loads(hook.stdout)["continue"], hook.stdout)
            stdout, stderr = broker.communicate(timeout=10)
            self.assertEqual(
                broker.returncode,
                130,
                f"stdout={stdout!r} stderr={stderr!r}",
            )
            self.assertIsNone(hygiene.process_identity(child_pid))
            self.assertNotIn(self.records()[0]["state"], hygiene.ACTIVE_STATES)
        finally:
            if broker.poll() is None:
                broker.terminate()
                broker.wait(timeout=5)
            broker.communicate(timeout=5)

    def test_stop_hook_warns_without_killing_different_owner(self) -> None:
        environment = dict(os.environ)
        environment["YAKHERD_PROCESS_STATE"] = str(self.root)
        environment["CODEX_THREAD_ID"] = "other-session"
        broker = subprocess.Popen(
            [
                sys.executable,
                "-B",
                str(ROOT / "yakherd.py"),
                "exec",
                "--light",
                "--timeout",
                "30",
                "--",
                sys.executable,
                "-B",
                "-c",
                "import time; time.sleep(30)",
            ],
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            self.wait_for(
                lambda: bool(
                    self.records()
                    and self.records()[0].get("state") == "running"
                )
            )
            child_pid = int(self.records()[0]["top_process"]["pid"])  # type: ignore[index]
            hook = self.cli_process(
                ["process", "hook"],
                stdin=json.dumps(
                    {
                        "hook_event_name": "SubagentStop",
                        "session_id": "hook-session",
                        "turn_id": "hook-turn",
                        "cwd": str(ROOT),
                    }
                ),
            )
            self.assertEqual(hook.returncode, 0, hook.stderr)
            payload = json.loads(hook.stdout)
            self.assertTrue(payload["continue"], hook.stdout)
            self.assertIn("different owner", payload["systemMessage"])
            self.assertIsNone(broker.poll())
            self.assertIsNotNone(hygiene.process_identity(child_pid))
        finally:
            if broker.poll() is None:
                broker.terminate()
                broker.wait(timeout=5)
            broker.communicate(timeout=5)

    def test_legacy_pid_identity_mismatch_is_unverified_and_never_terminated(self) -> None:
        sleeper = subprocess.Popen(
            [sys.executable, "-B", "-c", "import time; time.sleep(30)"]
        )
        try:
            identity = hygiene.process_identity(sleeper.pid)
            self.assertIsNotNone(identity)
            expected = dict(identity)
            expected["creation_time_100ns"] += 1
            record = hygiene._new_record(
                command=[sys.executable, "-c", "pass"],
                cwd=ROOT,
                classification="light",
                timeout_seconds=10,
                queue_timeout_seconds=10,
                owner="pid-reuse-test",
            )
            record["state"] = "running"
            record["broker"] = {"pid": 0, "creation_time_100ns": 0, "executable": None}
            record["top_process"] = expected
            record["processes_observed"] = [expected]
            hygiene.write_task(self.root, record)
            report = hygiene.reconcile(self.root, dry_run=False)
            self.assertEqual(report["cleanup_blockers"], [])
            self.assertIsNone(sleeper.poll())
            self.assertEqual(self.records()[0]["state"], "retired_warning")
        finally:
            sleeper.terminate()
            sleeper.wait(timeout=5)

    def test_stale_identity_warning_does_not_block_new_execution_or_hook(self) -> None:
        sleeper = subprocess.Popen(
            [sys.executable, "-B", "-c", "import time; time.sleep(30)"]
        )
        try:
            identity = hygiene.process_identity(sleeper.pid)
            self.assertIsNotNone(identity)
            expected = dict(identity)
            expected["creation_time_100ns"] += 1
            record = hygiene._new_record(
                command=[sys.executable, "-c", "pass"],
                cwd=ROOT,
                classification="light",
                timeout_seconds=10,
                queue_timeout_seconds=10,
                owner="fail-closed-test",
            )
            record["state"] = "running"
            record["broker"] = {"pid": 0, "creation_time_100ns": 0, "executable": None}
            record["top_process"] = expected
            record["processes_observed"] = [expected]
            hygiene.write_task(self.root, record)
            self.assertEqual(self.broker([sys.executable, "-B", "-c", "pass"]), 0)
            self.assertIsNone(sleeper.poll())

            hook = self.cli_process(
                ["process", "hook"],
                stdin=json.dumps(
                    {
                        "hook_event_name": "Stop",
                        "session_id": "test",
                        "turn_id": "test",
                        "cwd": str(ROOT),
                    }
                ),
            )
            self.assertEqual(hook.returncode, 0, hook.stderr)
            self.assertTrue(json.loads(hook.stdout)["continue"])
        finally:
            sleeper.terminate()
            sleeper.wait(timeout=5)

    def test_pid_reuse_is_normal_warning_and_replacement_is_untouched(self) -> None:
        sleeper = subprocess.Popen([sys.executable, "-B", "-c", "import time; time.sleep(30)"])
        try:
            record = hygiene._new_record(
                command=[sys.executable, "-B", "-c", "pass"], cwd=ROOT,
                classification="light", timeout_seconds=10, queue_timeout_seconds=10, owner="reuse-test",
            )
            identity = hygiene.process_identity(sleeper.pid)
            self.assertIsNotNone(identity)
            expected = hygiene._bind_task_identity(identity, record, job_member=True, lifecycle="finite")
            expected["creation_time_100ns"] += 1
            event = hygiene._classify_record_process(record, expected)
            self.assertEqual(event["state"], hygiene.PID_REUSED_UNRELATED)
            self.assertIsNone(sleeper.poll())
        finally:
            sleeper.terminate()
            sleeper.wait(timeout=5)

    def test_contradictory_identity_is_inconsistent_not_terminated(self) -> None:
        record = hygiene._new_record(
            command=[sys.executable, "-B", "-c", "pass"], cwd=ROOT,
            classification="light", timeout_seconds=10, queue_timeout_seconds=10, owner="conflict-test",
        )
        identity = {
            "pid": 123, "creation_time_100ns": 1, "executable": r"C:\\Python\\python.exe",
            "image_name": "vctip.exe", "command_line": '"C:\\Python\\python.exe" -c pass',
            "task_id": record["task_id"], "execution_id": record["execution_id"],
            "job_name": record["job"]["name"], "observed_at": hygiene.utc_now(), "lifecycle": "finite",
        }
        event = hygiene._classify_record_process(record, identity)
        self.assertEqual(event["state"], hygiene.OWNERSHIP_RECORD_INCONSISTENT)

    def test_explicit_resume_allows_warning_once_but_not_blocker(self) -> None:
        record = hygiene._new_record(
            command=[sys.executable, "-B", "-c", "pass"], cwd=ROOT,
            classification="light", timeout_seconds=10, queue_timeout_seconds=10, owner="resume-test",
        )
        record["state"] = "cleanup_requested"
        record["cleanup"]["error"] = "unverified telemetry"
        hygiene.write_task(self.root, record)
        first = hygiene.resume_warning(self.root, str(record["task_id"]))
        second = hygiene.resume_warning(self.root, str(record["task_id"]))
        self.assertTrue(first["allowed"])
        self.assertTrue(second["allowed"])
        self.assertTrue(second["already_authorized"])
        record["state"] = "cleanup_failed"
        record["cleanup"]["severity"] = hygiene.CLEANUP_BLOCKER
        record["cleanup"]["error"] = "cleanup failure"
        record["concrete_hazards"] = []
        hygiene.write_task(self.root, record)
        # A historical cleanup_failed record with no remaining verified hazard is
        # a warning, not a permanent embargo.
        self.assertTrue(hygiene.resume_warning(self.root, str(record["task_id"]))["allowed"])
        with mock.patch.object(
            hygiene, "_classify_record_processes",
            return_value=[{"state": hygiene.VERIFIED_LIVE_OWNED, "pid": 7, "current": {}}],
        ), mock.patch.object(
            hygiene, "_cleanup_severity",
            return_value=(hygiene.CLEANUP_BLOCKER, [{"pid": 7, "kind": "cpu_activity"}]),
        ):
            self.assertFalse(hygiene.resume_warning(self.root, str(record["task_id"]))["allowed"])

    def test_hot_verified_process_after_failed_cleanup_is_a_blocker(self) -> None:
        record = hygiene._new_record(
            command=[sys.executable, "-B", "-c", "pass"], cwd=ROOT,
            classification="light", timeout_seconds=10, queue_timeout_seconds=10, owner="hazard-test",
        )
        current = {
            "pid": 321, "creation_time_100ns": 1, "executable": r"C:\\Python\\python.exe",
            "cpu_time_seconds": 1.0, "working_set_bytes": 0,
        }
        live = [{"state": hygiene.VERIFIED_LIVE_OWNED, "pid": 321, "current": current}]
        with mock.patch.object(
            hygiene, "process_identity", side_effect=[dict(current), {**current, "cpu_time_seconds": 1.3}]
        ), mock.patch.object(hygiene.time, "sleep"):
            severity, hazards = hygiene._cleanup_severity(record, live, "TerminateJobObject failed")
        self.assertEqual(severity, hygiene.CLEANUP_BLOCKER)
        self.assertEqual(hazards[0]["kind"], "cpu_activity")

    def test_reconcile_never_opens_a_mismatched_recorded_job(self) -> None:
        record = hygiene._new_record(
            command=[sys.executable, "-B", "-c", "pass"], cwd=ROOT,
            classification="light", timeout_seconds=10, queue_timeout_seconds=10, owner="job-conflict-test",
        )
        record["state"] = "running"
        record["broker"] = {"pid": 0, "creation_time_100ns": 0, "executable": None}
        record["job"]["name"] = hygiene.expected_job_name(str(__import__("uuid").uuid4()))
        hygiene.write_task(self.root, record)
        with mock.patch.object(hygiene, "_open_existing_job", side_effect=AssertionError("must not open corrupt Job")):
            report = hygiene.reconcile(self.root, dry_run=False)
        self.assertEqual(report["cleanup_blockers"], [])
        self.assertEqual(self.records()[0]["state"], "retired_warning")

    def test_wait_empty_failure_with_hot_verified_member_is_cleanup_blocker(self) -> None:
        class FakeJob:
            def __init__(self, replies: list[list[int]]) -> None:
                self.replies = iter(replies)
                self.terminated = False

            def pids(self) -> list[int]:
                return next(self.replies)

            def terminate(self, _code: int) -> None:
                self.terminated = True

            def wait_empty(self, _timeout: float) -> bool:
                return False

            def close(self) -> None:
                pass

        record = hygiene._new_record(
            command=[sys.executable, "-B", "-c", "pass"], cwd=ROOT,
            classification="light", timeout_seconds=10, queue_timeout_seconds=10, owner="wait-failure-test",
        )
        record["state"] = "running"
        hygiene.write_task(self.root, record)
        current = {"pid": 99, "creation_time_100ns": 1, "executable": r"C:\\Python\\python.exe", "cpu_time_seconds": 1.0, "working_set_bytes": 0}
        live = [{"state": hygiene.VERIFIED_LIVE_OWNED, "pid": 99, "current": current}]
        jobs = [FakeJob([[99]]), FakeJob([[99], []]), FakeJob([[99]])]
        with mock.patch.object(hygiene, "_open_existing_job", side_effect=jobs), mock.patch.object(
            hygiene, "_classify_record_processes", return_value=live
        ), mock.patch.object(
            hygiene, "process_identity", side_effect=[dict(current), {**current, "cpu_time_seconds": 1.3}]
        ), mock.patch.object(hygiene.time, "sleep"):
            report = hygiene.cleanup_owned(root=self.root, task_id=str(record["task_id"]), all_owned=False, dry_run=False, verify=True)
        self.assertEqual(report["tasks"][0]["status"], "cleanup_blocker")
        self.assertEqual(self.records()[0]["state"], "cleanup_failed")

    def test_destructive_cleanup_requires_verify(self) -> None:
        with self.assertRaises(hygiene.ProcessPolicyError):
            hygiene.cleanup_owned(
                root=self.root,
                task_id=None,
                all_owned=True,
                dry_run=False,
                verify=False,
            )

    @unittest.skipUnless(shutil.which("node"), "Node is unavailable")
    def test_unrelated_node_process_is_untouched(self) -> None:
        node = subprocess.Popen(["node", "-e", "setTimeout(()=>{},30000)"])
        try:
            self.assertEqual(
                self.broker(
                    [sys.executable, "-B", "-c", "import time; time.sleep(30)"],
                    timeout=0.3,
                ),
                124,
            )
            self.assertIsNone(node.poll())
        finally:
            node.terminate()
            node.wait(timeout=5)

    def test_status_dry_run_cleanup_and_hook_are_observable(self) -> None:
        self.assertEqual(self.broker([sys.executable, "-B", "-c", "pass"]), 0)
        status = hygiene.status_report(self.root)
        self.assertEqual(status["active_finite_tasks"], [])
        report = hygiene.cleanup_owned(
            root=self.root,
            task_id=None,
            all_owned=True,
            dry_run=True,
            verify=True,
        )
        self.assertEqual(report["tasks"], [])
        hook = self.cli_process(
            ["process", "hook"],
            stdin=json.dumps(
                {
                    "hook_event_name": "Stop",
                    "session_id": "test",
                    "turn_id": "test",
                    "cwd": str(ROOT),
                }
            ),
        )
        self.assertEqual(hook.returncode, 0, hook.stderr)
        self.assertTrue(json.loads(hook.stdout)["continue"])

    def test_two_hundred_mixed_lifecycles_leave_no_processes_or_handles(self) -> None:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.GetCurrentProcess.restype = ctypes.c_void_p
        kernel32.GetProcessHandleCount.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        kernel32.GetProcessHandleCount.restype = ctypes.c_int

        def handle_count() -> int:
            value = ctypes.c_ulong()
            self.assertTrue(
                kernel32.GetProcessHandleCount(kernel32.GetCurrentProcess(), ctypes.byref(value))
            )
            return int(value.value)

        def marker_cancel() -> None:
            existing = {str(record["task_id"]) for record in self.records()}
            result: list[int] = []
            worker = threading.Thread(
                target=lambda: result.append(
                    self.broker(
                        [sys.executable, "-B", "-c", "import time; time.sleep(30)"]
                    )
                )
            )
            worker.start()
            selected: list[str] = []

            def find_running() -> bool:
                selected[:] = [
                    str(record["task_id"])
                    for record in self.records()
                    if str(record["task_id"]) not in existing
                    and record.get("state") == "running"
                ]
                return bool(selected)

            self.wait_for(find_running)
            hygiene.request_cancellation(self.root, selected[0])
            worker.join(timeout=10)
            self.assertFalse(worker.is_alive())
            self.assertEqual(result, [130])

        def broker_crash() -> None:
            existing = {str(record["task_id"]) for record in self.records()}
            environment = dict(os.environ)
            environment["YAKHERD_PROCESS_STATE"] = str(self.root)
            broker = subprocess.Popen(
                [
                    sys.executable,
                    "-B",
                    str(ROOT / "yakherd.py"),
                    "exec",
                    "--light",
                    "--timeout",
                    "30",
                    "--",
                    sys.executable,
                    "-B",
                    "-c",
                    "import time; time.sleep(30)",
                ],
                cwd=ROOT,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            selected: list[dict[str, object]] = []
            try:
                def find_running() -> bool:
                    selected[:] = [
                        record
                        for record in self.records()
                        if str(record["task_id"]) not in existing
                        and record.get("state") == "running"
                    ]
                    return bool(selected)

                self.wait_for(find_running)
                child_pid = int(selected[0]["top_process"]["pid"])  # type: ignore[index]
                broker.terminate()
                broker.wait(timeout=5)
                self.wait_for(lambda: hygiene.process_identity(child_pid) is None)
                report = hygiene.reconcile(self.root, dry_run=False)
                self.assertFalse(report["ambiguous"])
            finally:
                if broker.poll() is None:
                    broker.terminate()
                    broker.wait(timeout=5)
                broker.communicate(timeout=5)

        baseline = handle_count()
        nested_script = (
            "import subprocess,sys; "
            "p=subprocess.Popen([sys.executable,'-B','-c','pass']); p.wait()"
        )
        for index in range(200):
            case = index % 40
            if case in {0, 20}:
                self.assertEqual(
                    self.broker(
                        [sys.executable, "-B", "-c", "import time; time.sleep(1)"],
                        timeout=0.05,
                    ),
                    124,
                )
            elif case in {1, 21}:
                self.assertEqual(
                    self.broker([sys.executable, "-B", "-c", nested_script]), 0
                )
            elif case == 2:
                marker_cancel()
            elif case == 3:
                broker_crash()
            else:
                self.assertEqual(
                    self.broker([sys.executable, "-B", "-c", "pass"]), 0
                )
        after = handle_count()
        self.assertLessEqual(after, baseline + 12)
        self.assertEqual(len(self.records()), 200)
        for record in self.records():
            self.assertTrue(record["cleanup"]["verified_zero"])  # type: ignore[index]
        status = hygiene.status_report(self.root)
        self.assertEqual(status["active_finite_tasks"], [])
        self.assertEqual(status["queued_heavy_tasks"], [])
        self.assertEqual(status["cleanup_failures"], [])


if __name__ == "__main__":
    unittest.main()
