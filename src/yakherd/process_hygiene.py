"""Y-PROC-1 Windows process containment and local execution governance."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import math
import os
import re
import signal
import shutil
import subprocess
import sys
import time
import uuid
from contextlib import contextmanager
from ctypes import wintypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


POLICY_ID = "Y-PROC-1.1"
SCHEMA = "yakherd.process-task.v1.1"
LEGACY_SCHEMAS = {"yakherd.process-task.v1"}
DEFAULT_TIMEOUT_SECONDS = 900.0
DEFAULT_QUEUE_TIMEOUT_SECONDS = 900.0
POLL_SECONDS = 0.1
ACTIVE_STATES = {"queued", "running", "cleanup_requested", "cleanup_failed"}
TERMINAL_STATES = {
    "cancelled",
    "cleaned",
    "completed",
    "failed",
    "queue_timeout",
    "reconciled",
    "retired_warning",
    "timed_out",
}

VERIFIED_LIVE_OWNED = "VERIFIED_LIVE_OWNED"
VERIFIED_EXITED = "VERIFIED_EXITED"
PID_REUSED_UNRELATED = "PID_REUSED_UNRELATED"
OWNERSHIP_UNVERIFIED = "OWNERSHIP_UNVERIFIED"
OWNERSHIP_RECORD_INCONSISTENT = "OWNERSHIP_RECORD_INCONSISTENT"
APPROVED_PERSISTENT = "APPROVED_PERSISTENT"
CLEANUP_WARNING = "CLEANUP_WARNING"
CLEANUP_BLOCKER = "CLEANUP_BLOCKER"
PROCESS_STATES = {
    VERIFIED_LIVE_OWNED,
    VERIFIED_EXITED,
    PID_REUSED_UNRELATED,
    OWNERSHIP_UNVERIFIED,
    OWNERSHIP_RECORD_INCONSISTENT,
    APPROVED_PERSISTENT,
}


class ProcessPolicyError(RuntimeError):
    """A command or operation violates Y-PROC-1."""


class ProcessCancelled(RuntimeError):
    """A task-scoped cancellation marker was observed by the broker."""


class WindowsProcessError(OSError):
    """A required Windows process operation failed."""


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def state_root() -> Path:
    override = os.environ.get("YAKHERD_PROCESS_STATE")
    if override:
        return Path(override).expanduser().absolute()
    base = os.environ.get("LOCALAPPDATA")
    if not base:
        base = str(Path.home() / ".local" / "state")
    return Path(base) / "Yakherd" / "process-v1"


def task_path(root: Path, task_id: str) -> Path:
    _validate_task_id(task_id)
    return root / "tasks" / f"{task_id}.json"


def history_path(root: Path, task_id: str) -> Path:
    _validate_task_id(task_id)
    return root / "history" / f"{task_id}.json"


def cancel_path(root: Path, task_id: str) -> Path:
    _validate_task_id(task_id)
    return root / "cancellations" / f"{task_id}.cancel"


def _validate_task_id(task_id: str) -> None:
    try:
        parsed = uuid.UUID(task_id)
    except (ValueError, AttributeError) as exc:
        raise ProcessPolicyError(f"invalid Y-PROC-1 task id: {task_id!r}") from exc
    if str(parsed) != task_id:
        raise ProcessPolicyError(f"non-canonical Y-PROC-1 task id: {task_id!r}")


def expected_job_name(task_id: str) -> str:
    _validate_task_id(task_id)
    return f"Local\\Yakherd-{task_id}"


def request_cancellation(root: Path, task_id: str) -> None:
    path = cancel_path(root, task_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write("Y-PROC-1 cancellation requested\n")
    except FileExistsError:
        pass


def cancellation_requested(root: Path, task_id: str) -> bool:
    return cancel_path(root, task_id).is_file()


def _write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    deadline = time.monotonic() + 2.0
    while True:
        try:
            os.replace(temporary, path)
            return
        except PermissionError:
            if time.monotonic() >= deadline:
                raise
            time.sleep(0.01)


@contextmanager
def _file_lock(path: Path, *, blocking: bool) -> Iterator[bool]:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+b")
    acquired = False
    try:
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            mode = msvcrt.LK_LOCK if blocking else msvcrt.LK_NBLCK
            try:
                msvcrt.locking(handle.fileno(), mode, 1)
                acquired = True
            except OSError:
                acquired = False
        else:
            import fcntl

            operation = fcntl.LOCK_EX
            if not blocking:
                operation |= fcntl.LOCK_NB
            try:
                fcntl.flock(handle.fileno(), operation)
                acquired = True
            except OSError:
                acquired = False
        yield acquired
    finally:
        if acquired:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def write_task(root: Path, record: dict[str, Any]) -> None:
    with _file_lock(root / "registry.lock", blocking=True) as acquired:
        if not acquired:  # pragma: no cover - blocking locks either acquire or raise
            raise ProcessPolicyError("could not acquire process registry lock")
        _write_json_atomic(task_path(root, str(record["task_id"])), record)


def retire_task(root: Path, record: dict[str, Any]) -> None:
    """Move a terminal record out of the actionable task registry."""
    task_id = str(record["task_id"])
    record["retired_at"] = record.get("retired_at") or utc_now()
    with _file_lock(root / "registry.lock", blocking=True) as acquired:
        if not acquired:  # pragma: no cover
            raise ProcessPolicyError("could not acquire process registry lock")
        _write_json_atomic(history_path(root, task_id), record)
        active = task_path(root, task_id)
        try:
            active.unlink()
        except FileNotFoundError:
            pass


def _load_task_directory(
    directory: Path, *, accepted_schemas: set[str]
) -> tuple[list[dict[str, Any]], list[str]]:
    if not directory.is_dir():
        return [], []
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in sorted(directory.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict) or value.get("schema") not in accepted_schemas:
                raise ValueError("schema mismatch")
            task_id = value.get("task_id")
            if not isinstance(task_id, str):
                raise ValueError("task_id is missing or not a string")
            _validate_task_id(task_id)
            if path.stem != task_id:
                raise ValueError("task_id does not match registry filename")
            records.append(value)
        except (
            OSError,
            UnicodeDecodeError,
            json.JSONDecodeError,
            ValueError,
            ProcessPolicyError,
        ) as exc:
            errors.append(f"{path.name}: {exc}")
    return records, errors


def load_tasks(
    root: Path, *, include_history: bool = True
) -> tuple[list[dict[str, Any]], list[str]]:
    accepted = {SCHEMA, *LEGACY_SCHEMAS}
    active, active_errors = _load_task_directory(
        root / "tasks", accepted_schemas=accepted
    )
    if not include_history:
        return active, active_errors
    history, history_errors = _load_task_directory(
        root / "history", accepted_schemas=accepted
    )
    by_id = {str(record["task_id"]): record for record in history}
    by_id.update({str(record["task_id"]): record for record in active})
    return [by_id[key] for key in sorted(by_id)], active_errors + history_errors


if os.name == "nt":
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    ntdll = ctypes.WinDLL("ntdll", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    shell32 = ctypes.WinDLL("shell32", use_last_error=True)

    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
    PROCESS_TERMINATE = 0x0001
    PROCESS_VM_READ = 0x0010
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    SYNCHRONIZE = 0x00100000
    TH32CS_SNAPPROCESS = 0x00000002
    BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
    EXTENDED_STARTUPINFO_PRESENT = 0x00080000
    STARTF_USESTDHANDLES = 0x00000100
    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    DUPLICATE_SAME_ACCESS = 0x00000002
    PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002
    PROC_THREAD_ATTRIBUTE_JOB_LIST = 0x0002000D
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    JobObjectBasicProcessIdList = 3
    JobObjectExtendedLimitInformation = 9
    JOB_OBJECT_QUERY = 0x0004
    JOB_OBJECT_TERMINATE = 0x0008
    WAIT_OBJECT_0 = 0
    WAIT_TIMEOUT = 258
    STILL_ACTIVE = 259
    ERROR_NO_MORE_FILES = 18
    ERROR_ALREADY_EXISTS = 183
    ERROR_MORE_DATA = 234
    ERROR_INSUFFICIENT_BUFFER = 122
    ProcessCommandLineInformation = 60

    ULONG_PTR = wintypes.WPARAM
    SIZE_T = ctypes.c_size_t

    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

    class UNICODE_STRING(ctypes.Structure):
        _fields_ = [
            ("Length", wintypes.USHORT),
            ("MaximumLength", wintypes.USHORT),
            ("Buffer", wintypes.LPWSTR),
        ]

    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ULONG_PTR),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", wintypes.LONG),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", wintypes.WCHAR * 260),
        ]

    class IO_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("ReadOperationCount", ctypes.c_ulonglong),
            ("WriteOperationCount", ctypes.c_ulonglong),
            ("OtherOperationCount", ctypes.c_ulonglong),
            ("ReadTransferCount", ctypes.c_ulonglong),
            ("WriteTransferCount", ctypes.c_ulonglong),
            ("OtherTransferCount", ctypes.c_ulonglong),
        ]

    class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_longlong),
            ("PerJobUserTimeLimit", ctypes.c_longlong),
            ("LimitFlags", wintypes.DWORD),
            ("MinimumWorkingSetSize", SIZE_T),
            ("MaximumWorkingSetSize", SIZE_T),
            ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ULONG_PTR),
            ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
            ("IoInfo", IO_COUNTERS),
            ("ProcessMemoryLimit", SIZE_T),
            ("JobMemoryLimit", SIZE_T),
            ("PeakProcessMemoryUsed", SIZE_T),
            ("PeakJobMemoryUsed", SIZE_T),
        ]

    class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", SIZE_T),
            ("WorkingSetSize", SIZE_T),
            ("QuotaPeakPagedPoolUsage", SIZE_T),
            ("QuotaPagedPoolUsage", SIZE_T),
            ("QuotaPeakNonPagedPoolUsage", SIZE_T),
            ("QuotaNonPagedPoolUsage", SIZE_T),
            ("PagefileUsage", SIZE_T),
            ("PeakPagefileUsage", SIZE_T),
        ]

    class STARTUPINFOW(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("lpReserved", wintypes.LPWSTR),
            ("lpDesktop", wintypes.LPWSTR),
            ("lpTitle", wintypes.LPWSTR),
            ("dwX", wintypes.DWORD),
            ("dwY", wintypes.DWORD),
            ("dwXSize", wintypes.DWORD),
            ("dwYSize", wintypes.DWORD),
            ("dwXCountChars", wintypes.DWORD),
            ("dwYCountChars", wintypes.DWORD),
            ("dwFillAttribute", wintypes.DWORD),
            ("dwFlags", wintypes.DWORD),
            ("wShowWindow", wintypes.WORD),
            ("cbReserved2", wintypes.WORD),
            ("lpReserved2", ctypes.POINTER(wintypes.BYTE)),
            ("hStdInput", wintypes.HANDLE),
            ("hStdOutput", wintypes.HANDLE),
            ("hStdError", wintypes.HANDLE),
        ]

    class STARTUPINFOEXW(ctypes.Structure):
        _fields_ = [
            ("StartupInfo", STARTUPINFOW),
            ("lpAttributeList", ctypes.c_void_p),
        ]

    class PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("hProcess", wintypes.HANDLE),
            ("hThread", wintypes.HANDLE),
            ("dwProcessId", wintypes.DWORD),
            ("dwThreadId", wintypes.DWORD),
        ]

    kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.OpenJobObjectW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
    kernel32.OpenJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    ]
    kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel32.TerminateJobObject.restype = wintypes.BOOL
    kernel32.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
    kernel32.IsProcessInJob.restype = wintypes.BOOL
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    kernel32.TerminateProcess.restype = wintypes.BOOL
    kernel32.GetProcessTimes.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(FILETIME),
        ctypes.POINTER(FILETIME),
        ctypes.POINTER(FILETIME),
        ctypes.POINTER(FILETIME),
    ]
    kernel32.GetProcessTimes.restype = wintypes.BOOL
    kernel32.QueryFullProcessImageNameW.argtypes = [
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPWSTR,
        ctypes.POINTER(wintypes.DWORD),
    ]
    kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
    kernel32.GetPriorityClass.argtypes = [wintypes.HANDLE]
    kernel32.GetPriorityClass.restype = wintypes.DWORD
    kernel32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel32.GetExitCodeProcess.restype = wintypes.BOOL
    kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel32.WaitForSingleObject.restype = wintypes.DWORD
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    kernel32.LocalFree.argtypes = [wintypes.HLOCAL]
    kernel32.LocalFree.restype = wintypes.HLOCAL
    kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel32.Process32FirstW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    kernel32.Process32FirstW.restype = wintypes.BOOL
    kernel32.Process32NextW.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32W)]
    kernel32.Process32NextW.restype = wintypes.BOOL
    kernel32.GetCurrentProcess.argtypes = []
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.GetStdHandle.argtypes = [wintypes.DWORD]
    kernel32.GetStdHandle.restype = wintypes.HANDLE
    kernel32.DuplicateHandle.argtypes = [
        wintypes.HANDLE,
        wintypes.HANDLE,
        wintypes.HANDLE,
        ctypes.POINTER(wintypes.HANDLE),
        wintypes.DWORD,
        wintypes.BOOL,
        wintypes.DWORD,
    ]
    kernel32.DuplicateHandle.restype = wintypes.BOOL
    kernel32.InitializeProcThreadAttributeList.argtypes = [
        ctypes.c_void_p,
        wintypes.DWORD,
        wintypes.DWORD,
        ctypes.POINTER(SIZE_T),
    ]
    kernel32.InitializeProcThreadAttributeList.restype = wintypes.BOOL
    kernel32.UpdateProcThreadAttribute.argtypes = [
        ctypes.c_void_p,
        wintypes.DWORD,
        SIZE_T,
        ctypes.c_void_p,
        SIZE_T,
        ctypes.c_void_p,
        ctypes.c_void_p,
    ]
    kernel32.UpdateProcThreadAttribute.restype = wintypes.BOOL
    kernel32.DeleteProcThreadAttributeList.argtypes = [ctypes.c_void_p]
    kernel32.DeleteProcThreadAttributeList.restype = None
    kernel32.CreateProcessW.argtypes = [
        wintypes.LPCWSTR,
        wintypes.LPWSTR,
        ctypes.c_void_p,
        ctypes.c_void_p,
        wintypes.BOOL,
        wintypes.DWORD,
        ctypes.c_void_p,
        wintypes.LPCWSTR,
        ctypes.POINTER(STARTUPINFOW),
        ctypes.POINTER(PROCESS_INFORMATION),
    ]
    kernel32.CreateProcessW.restype = wintypes.BOOL
    ntdll.NtQueryInformationProcess.argtypes = [
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.ULONG,
        ctypes.POINTER(wintypes.ULONG),
    ]
    ntdll.NtQueryInformationProcess.restype = ctypes.c_long
    psapi.GetProcessMemoryInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(PROCESS_MEMORY_COUNTERS),
        wintypes.DWORD,
    ]
    psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
    shell32.CommandLineToArgvW.argtypes = [
        wintypes.LPCWSTR,
        ctypes.POINTER(ctypes.c_int),
    ]
    shell32.CommandLineToArgvW.restype = ctypes.POINTER(wintypes.LPWSTR)


def _require_windows() -> None:
    if os.name != "nt":
        raise ProcessPolicyError("Y-PROC-1 execution is currently supported only on Windows")


def _win_error(operation: str) -> WindowsProcessError:
    return WindowsProcessError(ctypes.get_last_error(), operation)


def _filetime_value(value: Any) -> int:
    return (int(value.dwHighDateTime) << 32) | int(value.dwLowDateTime)


def _open_process(pid: int, access: int | None = None) -> Any:
    _require_windows()
    requested = access or (PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE)
    handle = kernel32.OpenProcess(requested, False, pid)
    if not handle:
        return None
    return handle


def _parent_pid_map() -> dict[int, int]:
    _require_windows()
    snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if snapshot == INVALID_HANDLE_VALUE:
        raise _win_error("CreateToolhelp32Snapshot(processes)")
    values: dict[int, int] = {}
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
        if not kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
            error = ctypes.get_last_error()
            if error != ERROR_NO_MORE_FILES:
                raise _win_error("Process32FirstW")
            return values
        while True:
            values[int(entry.th32ProcessID)] = int(entry.th32ParentProcessID)
            entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
            if not kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                error = ctypes.get_last_error()
                if error != ERROR_NO_MORE_FILES:
                    raise _win_error("Process32NextW")
                break
    finally:
        kernel32.CloseHandle(snapshot)
    return values


def _process_creation_time(pid: int) -> int | None:
    handle = _open_process(pid, PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE)
    if not handle:
        return None
    try:
        creation = FILETIME()
        exit_time = FILETIME()
        kernel = FILETIME()
        user = FILETIME()
        if not kernel32.GetProcessTimes(
            handle,
            ctypes.byref(creation),
            ctypes.byref(exit_time),
            ctypes.byref(kernel),
            ctypes.byref(user),
        ):
            return None
        return _filetime_value(creation)
    finally:
        kernel32.CloseHandle(handle)


def _query_process_command_line(handle: Any) -> str | None:
    required = wintypes.ULONG()
    ntdll.NtQueryInformationProcess(
        handle,
        ProcessCommandLineInformation,
        None,
        0,
        ctypes.byref(required),
    )
    if not required.value or required.value > 1_048_576:
        return None
    buffer = ctypes.create_string_buffer(required.value)
    status = ntdll.NtQueryInformationProcess(
        handle,
        ProcessCommandLineInformation,
        buffer,
        required.value,
        ctypes.byref(required),
    )
    if status < 0:
        return None
    value = UNICODE_STRING.from_buffer(buffer)
    if not value.Buffer or not value.Length:
        return ""
    return ctypes.wstring_at(value.Buffer, int(value.Length) // 2)


def _command_line_image_name(command_line: str | None) -> str | None:
    if command_line is None or not command_line.strip():
        return None
    count = ctypes.c_int()
    values = shell32.CommandLineToArgvW(command_line, ctypes.byref(count))
    if not values or count.value < 1:
        return None
    try:
        return Path(values[0]).name
    finally:
        kernel32.LocalFree(values)


def _process_identity_from_handle(
    pid: int,
    handle: Any,
    parent_pids: dict[int, int] | None = None,
    *,
    active_only: bool = True,
    telemetry: bool = True,
) -> dict[str, Any] | None:
    exit_code = wintypes.DWORD()
    if not kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
        return None
    if active_only and exit_code.value != STILL_ACTIVE:
        return None
    creation = FILETIME()
    exit_time = FILETIME()
    kernel = FILETIME()
    user = FILETIME()
    if not kernel32.GetProcessTimes(
        handle,
        ctypes.byref(creation),
        ctypes.byref(exit_time),
        ctypes.byref(kernel),
        ctypes.byref(user),
    ):
        return None
    capacity = wintypes.DWORD(32768)
    buffer = ctypes.create_unicode_buffer(capacity.value)
    executable: str | None = None
    if kernel32.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(capacity)):
        executable = buffer.value
    image_name = Path(executable).name if executable else None
    command_line = _query_process_command_line(handle) if telemetry else None
    memory = PROCESS_MEMORY_COUNTERS()
    memory.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
    working_set: int | None = None
    if telemetry and psapi.GetProcessMemoryInfo(handle, ctypes.byref(memory), memory.cb):
        working_set = int(memory.WorkingSetSize)
    priority = (int(kernel32.GetPriorityClass(handle)) or None) if telemetry else None
    if parent_pids is None and telemetry:
        try:
            parent_pids = _parent_pid_map()
        except WindowsProcessError:
            parent_pids = {}
    elif parent_pids is None:
        parent_pids = {}
    parent_pid = parent_pids.get(int(pid))
    return {
        "pid": int(pid),
        "parent_pid": parent_pid,
        "parent_creation_time_100ns": (
            _process_creation_time(parent_pid)
            if telemetry and isinstance(parent_pid, int) and parent_pid > 0
            else None
        ),
        "creation_time_100ns": _filetime_value(creation),
        "executable": executable,
        "image_name": image_name,
        "command_line": command_line,
        "cpu_time_seconds": (
            _filetime_value(kernel) + _filetime_value(user)
        ) / 10_000_000,
        "working_set_bytes": working_set,
        "priority_class": priority,
        "observed_at": utc_now(),
    }


def process_identity(pid: int, parent_pids: dict[int, int] | None = None) -> dict[str, Any] | None:
    """Return PID-reuse-safe active-process identity and lightweight telemetry."""
    _require_windows()
    handle = _open_process(pid, PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_VM_READ | SYNCHRONIZE)
    if not handle:
        return None
    try:
        return _process_identity_from_handle(pid, handle, parent_pids)
    finally:
        kernel32.CloseHandle(handle)


def identity_matches(expected: dict[str, Any], actual: dict[str, Any] | None) -> bool:
    if actual is None:
        return False
    if expected.get("pid") != actual.get("pid"):
        return False
    if expected.get("creation_time_100ns") != actual.get("creation_time_100ns"):
        return False
    expected_executable = expected.get("executable")
    actual_executable = actual.get("executable")
    if expected_executable and actual_executable:
        return os.path.normcase(expected_executable) == os.path.normcase(actual_executable)
    return expected_executable == actual_executable


def identity_coherence(
    identity: dict[str, Any], record: dict[str, Any] | None = None
) -> list[str]:
    """Return contradictions inside one identity observation; missing is separate."""
    errors: list[str] = []
    executable = identity.get("executable")
    image_name = identity.get("image_name")
    if executable and image_name:
        if os.path.normcase(Path(str(executable)).name) != os.path.normcase(
            str(image_name)
        ):
            errors.append("executable_path_image_name_conflict")
    command_image = _command_line_image_name(identity.get("command_line"))
    if command_image and image_name:
        if os.path.normcase(command_image) != os.path.normcase(str(image_name)):
            errors.append("command_line_image_name_conflict")
    task_id = identity.get("task_id")
    job_name = identity.get("job_name")
    if task_id and job_name:
        try:
            if str(job_name) != expected_job_name(str(task_id)):
                errors.append("task_job_identity_conflict")
        except ProcessPolicyError:
            errors.append("invalid_task_identity")
    if record is not None:
        if task_id is not None and task_id != record.get("task_id"):
            errors.append("process_record_task_conflict")
        expected_execution = record.get("execution_id")
        if (
            expected_execution is not None
            and identity.get("execution_id") is not None
            and identity.get("execution_id") != expected_execution
        ):
            errors.append("process_record_execution_conflict")
        recorded_job = record.get("job", {}).get("name")
        if job_name is not None and recorded_job is not None and job_name != recorded_job:
            errors.append("process_record_job_conflict")
    return sorted(set(errors))


def missing_ownership_fields(identity: dict[str, Any]) -> list[str]:
    required = (
        "pid",
        "creation_time_100ns",
        "executable",
        "image_name",
        "task_id",
        "execution_id",
        "job_name",
        "observed_at",
        "lifecycle",
    )
    return [name for name in required if identity.get(name) in {None, ""}]


class WindowsJob:
    """A named kill-on-close Windows Job Object."""

    def __init__(self, name: str, *, open_existing: bool = False) -> None:
        _require_windows()
        self.name = name
        if open_existing:
            self.handle = kernel32.OpenJobObjectW(
                JOB_OBJECT_QUERY | JOB_OBJECT_TERMINATE, False, name
            )
            if not self.handle:
                raise _win_error(f"OpenJobObjectW({name})")
            return
        ctypes.set_last_error(0)
        self.handle = kernel32.CreateJobObjectW(None, name)
        if not self.handle:
            raise _win_error("CreateJobObjectW")
        if ctypes.get_last_error() == ERROR_ALREADY_EXISTS:
            self.close()
            raise WindowsProcessError(f"refusing pre-existing Job Object: {name}")
        information = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        information.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not kernel32.SetInformationJobObject(
            self.handle,
            JobObjectExtendedLimitInformation,
            ctypes.byref(information),
            ctypes.sizeof(information),
        ):
            self.close()
            raise _win_error("SetInformationJobObject(kill-on-close)")

    def contains(self, process_handle: Any) -> bool:
        result = wintypes.BOOL()
        if not kernel32.IsProcessInJob(
            process_handle, self.handle, ctypes.byref(result)
        ):
            raise _win_error("IsProcessInJob")
        return bool(result.value)

    def pids(self) -> list[int]:
        capacity = 16
        while capacity <= 65536:
            size = 8 + ctypes.sizeof(ULONG_PTR) * capacity
            buffer = ctypes.create_string_buffer(size)
            returned = wintypes.DWORD()
            if kernel32.QueryInformationJobObject(
                self.handle,
                JobObjectBasicProcessIdList,
                buffer,
                size,
                ctypes.byref(returned),
            ):
                assigned = ctypes.c_uint32.from_buffer(buffer, 0).value
                listed = ctypes.c_uint32.from_buffer(buffer, 4).value
                count = min(int(assigned), int(listed), capacity)
                array_type = ULONG_PTR * capacity
                values = array_type.from_buffer(buffer, 8)
                return [int(values[index]) for index in range(count)]
            if ctypes.get_last_error() != ERROR_MORE_DATA:
                raise _win_error("QueryInformationJobObject(process list)")
            capacity *= 2
        raise WindowsProcessError("job process list exceeded safety limit")

    def terminate(self, exit_code: int) -> None:
        if not kernel32.TerminateJobObject(self.handle, exit_code):
            raise _win_error("TerminateJobObject")

    def wait_empty(self, timeout_seconds: float) -> bool:
        result = kernel32.WaitForSingleObject(
            self.handle, max(0, int(timeout_seconds * 1000))
        )
        return result == WAIT_OBJECT_0

    def close(self) -> None:
        if getattr(self, "handle", None):
            kernel32.CloseHandle(self.handle)
            self.handle = None

    def __enter__(self) -> "WindowsJob":
        return self

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        self.close()


class NativeProcess:
    """Minimal handle-owning process adapter for atomic Job-list creation."""

    def __init__(self, handle: Any, pid: int, command_line: str) -> None:
        self.handle = handle
        self.pid = int(pid)
        self.command_line = command_line
        self.returncode: int | None = None

    def poll(self) -> int | None:
        if self.returncode is not None:
            return self.returncode
        code = wintypes.DWORD()
        if not kernel32.GetExitCodeProcess(self.handle, ctypes.byref(code)):
            raise _win_error("GetExitCodeProcess")
        if code.value == STILL_ACTIVE:
            return None
        self.returncode = ctypes.c_long(code.value).value
        return self.returncode

    def wait(self, timeout: float) -> int:
        result = kernel32.WaitForSingleObject(
            self.handle, max(0, int(timeout * 1000))
        )
        if result == WAIT_TIMEOUT:
            raise TimeoutError(f"process wait timed out pid={self.pid}")
        if result != WAIT_OBJECT_0:
            raise _win_error("WaitForSingleObject(process)")
        return int(self.poll())

    def identity(self) -> dict[str, Any] | None:
        return _process_identity_from_handle(
            self.pid, self.handle, active_only=False
        )

    def close(self) -> None:
        if self.handle:
            kernel32.CloseHandle(self.handle)
            self.handle = None


def _duplicate_inheritable_handle(source: Any, label: str) -> Any:
    if not source or source == INVALID_HANDLE_VALUE:
        raise WindowsProcessError(f"{label} is unavailable for attached execution")
    current = kernel32.GetCurrentProcess()
    target = wintypes.HANDLE()
    if not kernel32.DuplicateHandle(
        current,
        source,
        current,
        ctypes.byref(target),
        0,
        True,
        DUPLICATE_SAME_ACCESS,
    ):
        raise _win_error(f"DuplicateHandle({label})")
    return target


def _create_process_in_job(
    command: list[str],
    cwd: Path,
    job: WindowsJob,
    *,
    below_normal: bool,
) -> NativeProcess:
    """Create a child atomically assigned to ``job`` before its first instruction."""
    _require_windows()
    launch_command = list(command)
    command_line_text: str | None = None
    if Path(launch_command[0]).suffix.lower() in {".bat", ".cmd"}:
        command_interpreter = os.environ.get("COMSPEC") or shutil.which("cmd.exe")
        if not command_interpreter:
            raise WindowsProcessError("cmd.exe is required to launch a batch command")
        launch_command = [command_interpreter, "/d", "/s", "/c"]
        command_line_text = (
            subprocess.list2cmdline(launch_command)
            + ' "'
            + subprocess.list2cmdline(command)
            + '"'
        )
    attribute_size = SIZE_T()
    kernel32.InitializeProcThreadAttributeList(
        None, 2, 0, ctypes.byref(attribute_size)
    )
    if not attribute_size.value:
        raise _win_error("InitializeProcThreadAttributeList(size)")
    attribute_buffer = ctypes.create_string_buffer(attribute_size.value)
    attribute_list = ctypes.cast(attribute_buffer, ctypes.c_void_p)
    if not kernel32.InitializeProcThreadAttributeList(
        attribute_list, 2, 0, ctypes.byref(attribute_size)
    ):
        raise _win_error("InitializeProcThreadAttributeList")

    duplicated: list[Any] = []
    information = PROCESS_INFORMATION()
    created = False
    try:
        job_handle = wintypes.HANDLE(job.handle)
        if not kernel32.UpdateProcThreadAttribute(
            attribute_list,
            0,
            PROC_THREAD_ATTRIBUTE_JOB_LIST,
            ctypes.byref(job_handle),
            ctypes.sizeof(job_handle),
            None,
            None,
        ):
            raise _win_error("UpdateProcThreadAttribute(job list)")

        for constant, label in (
            (STD_INPUT_HANDLE, "stdin"),
            (STD_OUTPUT_HANDLE, "stdout"),
            (STD_ERROR_HANDLE, "stderr"),
        ):
            duplicated.append(
                _duplicate_inheritable_handle(kernel32.GetStdHandle(constant), label)
            )
        handle_array_type = wintypes.HANDLE * len(duplicated)
        handle_array = handle_array_type(*duplicated)
        if not kernel32.UpdateProcThreadAttribute(
            attribute_list,
            0,
            PROC_THREAD_ATTRIBUTE_HANDLE_LIST,
            handle_array,
            ctypes.sizeof(handle_array),
            None,
            None,
        ):
            raise _win_error("UpdateProcThreadAttribute(handle list)")

        startup = STARTUPINFOEXW()
        startup.StartupInfo.cb = ctypes.sizeof(STARTUPINFOEXW)
        startup.StartupInfo.dwFlags = STARTF_USESTDHANDLES
        startup.StartupInfo.hStdInput = duplicated[0]
        startup.StartupInfo.hStdOutput = duplicated[1]
        startup.StartupInfo.hStdError = duplicated[2]
        startup.lpAttributeList = attribute_list
        command_line = ctypes.create_unicode_buffer(
            command_line_text or subprocess.list2cmdline(launch_command)
        )
        flags = EXTENDED_STARTUPINFO_PRESENT
        if below_normal:
            flags |= BELOW_NORMAL_PRIORITY_CLASS
        if not kernel32.CreateProcessW(
            launch_command[0],
            command_line,
            None,
            None,
            True,
            flags,
            None,
            str(cwd),
            ctypes.byref(startup.StartupInfo),
            ctypes.byref(information),
        ):
            raise _win_error("CreateProcessW(atomic Job list)")
        created = True
        kernel32.CloseHandle(information.hThread)
        information.hThread = None
        process = NativeProcess(
            information.hProcess,
            int(information.dwProcessId),
            command_line.value,
        )
        if not job.contains(process.handle):
            raise WindowsProcessError(
                "CreateProcessW returned a child outside the required Job Object"
            )
        information.hProcess = None
        return process
    finally:
        if created:
            if information.hThread:
                kernel32.CloseHandle(information.hThread)
            if information.hProcess:
                kernel32.TerminateProcess(information.hProcess, 1)
                kernel32.WaitForSingleObject(information.hProcess, 5000)
                kernel32.CloseHandle(information.hProcess)
        for handle in duplicated:
            kernel32.CloseHandle(handle)
        kernel32.DeleteProcThreadAttributeList(attribute_list)


def _terminate_verified_process(
    expected: dict[str, Any],
    exit_code: int,
    *,
    record: dict[str, Any] | None = None,
    job: WindowsJob | None = None,
) -> str:
    if identity_coherence(expected, record):
        return "ownership_record_inconsistent"
    if missing_ownership_fields(expected):
        return "ownership_unverified"
    if job is None:
        return "ownership_unverified"
    handle = _open_process(
        int(expected["pid"]),
        PROCESS_TERMINATE
        | PROCESS_QUERY_LIMITED_INFORMATION
        | PROCESS_VM_READ
        | SYNCHRONIZE,
    )
    if not handle:
        return "already_exited_or_unopenable"
    try:
        actual = _process_identity_from_handle(
            int(expected["pid"]), handle, telemetry=False
        )
        if actual is None:
            return "already_exited"
        if not identity_matches(expected, actual):
            return "pid_reused_unrelated"
        if not job.contains(handle):
            return "ownership_unverified"
        if not kernel32.TerminateProcess(handle, exit_code):
            return "terminate_failed"
        wait_result = kernel32.WaitForSingleObject(handle, 5000)
        return "terminated" if wait_result == WAIT_OBJECT_0 else "terminate_wait_failed"
    finally:
        kernel32.CloseHandle(handle)


def _command_base(command: list[str]) -> str:
    name = Path(command[0]).name.lower()
    for suffix in (".exe", ".cmd", ".bat", ".com"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name


def validate_finite_command(command: list[str]) -> None:
    """Reject known interactive, detached, watch, daemon, and server forms."""
    if not command or not command[0].strip():
        raise ProcessPolicyError("exec requires a command after --")
    if any("\x00" in value for value in command):
        raise ProcessPolicyError("command arguments may not contain NUL")

    base = _command_base(command)
    lowered = [value.lower() for value in command[1:]]
    joined = " ".join(lowered)
    compact = {value.lstrip("-/") for value in lowered}
    wrapper_payload = ""

    if base in {"node", "node_repl"}:
        finite = any(value in {"-e", "--eval", "-p", "--print"} for value in lowered)
        finite = finite or any(not value.startswith("-") for value in lowered)
        if not finite:
            raise ProcessPolicyError("interactive Node/Node REPL commands are forbidden")

    if base in {"python", "python3", "pythonw", "py"}:
        finite = any(value in {"-c", "-m"} for value in lowered)
        finite = finite or any(
            not value.startswith("-") and not (base == "py" and value[:1].isdigit())
            for value in lowered
        )
        if not finite:
            raise ProcessPolicyError("interactive Python commands are forbidden")

    if base in {"powershell", "pwsh"}:
        if "noexit" in compact:
            raise ProcessPolicyError("PowerShell -NoExit is forbidden")
        if not any(value in {"-command", "-c", "-file", "-f"} for value in lowered):
            raise ProcessPolicyError("interactive PowerShell commands are forbidden")
        if "start-job" in joined:
            raise ProcessPolicyError("PowerShell Start-Job is forbidden")
        if "start-process" in joined and "-wait" not in joined:
            raise ProcessPolicyError("Start-Process requires -Wait under Y-PROC-1")
        wrapper_payload = joined

    if base == "cmd":
        if any(value == "/k" for value in lowered):
            raise ProcessPolicyError("cmd /K is forbidden")
        if not any(value in {"/c", "-c"} for value in lowered):
            raise ProcessPolicyError("interactive cmd commands are forbidden")
        try:
            marker = next(index for index, value in enumerate(lowered) if value in {"/c", "-c"})
        except StopIteration:  # pragma: no cover - protected by the check above
            marker = -1
        tail = lowered[marker + 1 :]
        wrapper_payload = " ".join(tail).strip(" \t\"'")
        if (
            re.search(r"(?:^|[&|;])\s*start(?:\s|$)", wrapper_payload)
            and "/wait" not in wrapper_payload
        ):
            raise ProcessPolicyError("cmd start requires /WAIT under Y-PROC-1")

    if base in {"bash", "sh", "wsl"}:
        wrapper_payload = joined

    if wrapper_payload:
        wrapped_persistent = [
            r"\b(?:npm|pnpm|yarn)(?:\.cmd)?\s+(?:run\s+)?dev(?:\s|$)",
            r"(?:^|[;&|]\s*)(?:vite|nodemon)(?:\.cmd)?(?:\s|$)",
            r"\bwebpack(?:\.cmd)?\s+serve(?:\s|$)",
            r"\btsc(?:\.cmd)?\b[^;&|]*(?:--watch|-w)(?:\s|$)",
            r"\bdotnet(?:\.exe)?\s+watch(?:\s|$)",
            r"(?:^|[;&|]\s*)start-job(?:\s|$)",
        ]
        if any(re.search(pattern, wrapper_payload) for pattern in wrapped_persistent):
            raise ProcessPolicyError(
                "wrapped watcher/server/background command requires a future persistent lease"
            )

    if base in {"vite", "nodemon"}:
        raise ProcessPolicyError(f"persistent development command is forbidden: {base}")
    if base in {"npm", "pnpm", "yarn"} and (
        "run dev" in joined or lowered[:1] == ["dev"]
    ):
        raise ProcessPolicyError("development-server scripts require a future persistent lease")
    if base == "webpack" and "serve" in lowered:
        raise ProcessPolicyError("webpack serve requires a future persistent lease")
    if base == "dotnet" and lowered[:1] == ["watch"]:
        raise ProcessPolicyError("dotnet watch requires a future persistent lease")
    if base == "tsc" and any(value in {"-w", "--watch"} for value in lowered):
        raise ProcessPolicyError("TypeScript watch mode requires a future persistent lease")
    if any(value in {"--daemon", "--watch", "--watchall"} for value in lowered):
        raise ProcessPolicyError("watch/daemon mode requires a future persistent lease")


def _resolve_executable(command: list[str], cwd: Path) -> list[str]:
    executable = command[0]
    candidate = Path(executable)
    if candidate.is_absolute():
        if not candidate.is_file():
            raise ProcessPolicyError(f"executable does not exist: {candidate}")
        return [str(candidate), *command[1:]]
    if candidate.parent != Path("."):
        relative = (cwd / candidate).resolve()
        if not relative.is_file():
            raise ProcessPolicyError(f"executable does not exist: {relative}")
        return [str(relative), *command[1:]]
    resolved = shutil.which(executable)
    if not resolved:
        raise ProcessPolicyError(f"executable was not found on PATH: {executable}")
    return [resolved, *command[1:]]


def _bind_task_identity(
    identity: dict[str, Any],
    record: dict[str, Any],
    *,
    job_member: bool,
    lifecycle: str,
    command_line: str | None = None,
    working_directory: str | None = None,
) -> dict[str, Any]:
    value = dict(identity)
    if command_line is not None:
        value["command_line"] = command_line
    value["image_name"] = (
        Path(str(value["executable"])).name if value.get("executable") else None
    )
    value.update(
        {
            "task_id": record["task_id"],
            "execution_id": record["execution_id"],
            "session_id": record["session_id"],
            "job_name": record["job"]["name"],
            "job_member": bool(job_member),
            "job_membership_observed_at": utc_now(),
            "observed_at": value.get("observed_at") or utc_now(),
            "lifecycle": lifecycle,
            "working_directory": working_directory,
        }
    )
    value["coherence_errors"] = identity_coherence(value, record)
    return value


def _merge_observed(
    record: dict[str, Any], existing: list[dict[str, Any]], pids: list[int]
) -> list[dict[str, Any]]:
    known = {
        (item.get("pid"), item.get("creation_time_100ns")): item
        for item in existing
    }
    try:
        parents = _parent_pid_map()
    except WindowsProcessError:
        parents = {}
    for pid in pids:
        identity = process_identity(pid, parents)
        if identity is not None:
            identity = _bind_task_identity(
                identity,
                record,
                job_member=True,
                lifecycle="finite_job_member",
            )
            key = (identity["pid"], identity["creation_time_100ns"])
            previous = known.get(key, {})
            known[key] = {
                **previous,
                **identity,
            }
    return sorted(
        known.values(),
        key=lambda item: (int(item.get("creation_time_100ns") or 0), int(item.get("pid") or 0)),
    )


def _new_record(
    *,
    command: list[str],
    cwd: Path,
    classification: str,
    timeout_seconds: float,
    queue_timeout_seconds: float,
    owner: str | None,
) -> dict[str, Any]:
    task_id = str(uuid.uuid4())
    execution_id = str(uuid.uuid4())
    codex_session = os.environ.get("CODEX_THREAD_ID")
    resolved_owner = (
        owner
        or os.environ.get("YAKHERD_TASK_OWNER")
        or (f"codex:{codex_session}" if codex_session else f"broker:{os.getpid()}")
    )
    broker = process_identity(os.getpid()) if os.name == "nt" else {"pid": os.getpid()}
    return {
        "schema": SCHEMA,
        "policy": POLICY_ID,
        "task_id": task_id,
        "execution_id": execution_id,
        "session_id": codex_session or resolved_owner,
        "owner": resolved_owner,
        "state": "queued" if classification == "heavy" else "starting",
        "classification": classification,
        "lifecycle": "finite",
        "command": command,
        "command_line": subprocess.list2cmdline(command),
        "working_directory": str(cwd),
        "broker": broker,
        "job": {
            "name": expected_job_name(task_id),
            "kill_on_close": True,
        },
        "priority": "below_normal" if classification == "heavy" else "normal",
        "timeout_seconds": timeout_seconds,
        "queue_timeout_seconds": queue_timeout_seconds,
        "created_at": utc_now(),
        "queued_at": utc_now() if classification == "heavy" else None,
        "started_at": None,
        "finished_at": None,
        "top_process": None,
        "processes_observed": [],
        "process_state_events": [],
        "concrete_hazards": [],
        "resume_authorizations": [],
        "exit_code": None,
        "termination_reason": None,
        "cleanup": {
            "attempted": False,
            "method": None,
            "verified_zero": False,
            "remaining_pids": [],
            "error": None,
            "severity": None,
            "warnings": [],
            "blockers": [],
        },
    }


@contextmanager
def _heavy_pipeline_lock(
    root: Path, record: dict[str, Any], timeout_seconds: float
) -> Iterator[None]:
    deadline = time.monotonic() + timeout_seconds
    while True:
        if cancellation_requested(root, str(record["task_id"])):
            raise ProcessCancelled("cancelled while queued")
        with _file_lock(root / "heavy-pipeline.lock", blocking=False) as acquired:
            if acquired:
                record["queue_wait_seconds"] = max(
                    0.0,
                    (datetime.now(timezone.utc) - datetime.fromisoformat(
                        str(record["created_at"]).replace("Z", "+00:00")
                    )).total_seconds(),
                )
                yield
                return
        if time.monotonic() >= deadline:
            raise TimeoutError("heavy pipeline queue timeout")
        time.sleep(POLL_SECONDS)


def run_broker(
    command: list[str],
    *,
    cwd: Path,
    classification: str,
    timeout_seconds: float,
    queue_timeout_seconds: float,
    owner: str | None,
    root: Path | None = None,
) -> int:
    """Run one finite command under the Y-PROC-1 lifecycle boundary."""
    _require_windows()
    if classification not in {"heavy", "light"}:
        raise ProcessPolicyError(f"invalid classification: {classification}")
    if (
        not math.isfinite(timeout_seconds)
        or not math.isfinite(queue_timeout_seconds)
        or timeout_seconds <= 0
        or queue_timeout_seconds <= 0
    ):
        raise ProcessPolicyError("timeouts must be finite positive seconds")
    cwd = cwd.resolve()
    if not cwd.is_dir():
        raise ProcessPolicyError(f"working directory does not exist: {cwd}")
    validate_finite_command(command)
    command = _resolve_executable(command, cwd)
    root = root or state_root()
    reconciliation = reconcile(root, dry_run=False)
    if reconciliation.get("cleanup_blockers"):
        raise ProcessPolicyError(
            "a verified, task-owned hazardous process remains; run `yakherd process status`"
        )
    record = _new_record(
        command=command,
        cwd=cwd,
        classification=classification,
        timeout_seconds=timeout_seconds,
        queue_timeout_seconds=queue_timeout_seconds,
        owner=owner,
    )
    write_task(root, record)

    @contextmanager
    def pipeline() -> Iterator[None]:
        if classification == "heavy":
            with _heavy_pipeline_lock(root, record, queue_timeout_seconds):
                yield
        else:
            yield

    try:
        with pipeline():
            return _run_in_job(root, record, command, cwd, timeout_seconds)
    except TimeoutError as exc:
        record["state"] = "queue_timeout"
        record["termination_reason"] = str(exc)
        record["finished_at"] = utc_now()
        record["cleanup"]["verified_zero"] = True
        retire_task(root, record)
        return 75
    except ProcessCancelled as exc:
        record["state"] = "cancelled"
        record["termination_reason"] = str(exc)
        record["finished_at"] = utc_now()
        record["cleanup"]["attempted"] = True
        record["cleanup"]["method"] = "task_cancellation_marker"
        record["cleanup"]["verified_zero"] = True
        retire_task(root, record)
        return 130
    except KeyboardInterrupt:
        record["state"] = "cancelled"
        record["termination_reason"] = "interrupted while queued"
        record["finished_at"] = utc_now()
        record["cleanup"]["verified_zero"] = True
        retire_task(root, record)
        return 130


def _run_in_job(
    root: Path,
    record: dict[str, Any],
    command: list[str],
    cwd: Path,
    timeout_seconds: float,
) -> int:
    job: WindowsJob | None = None
    process: NativeProcess | None = None
    reason = "exit"
    result = 1
    execution_error: str | None = None
    cleanup_error: str | None = None
    remaining: list[int] = []
    record["state"] = "starting"
    write_task(root, record)
    try:
        if cancellation_requested(root, str(record["task_id"])):
            raise ProcessCancelled("cancelled before launch")
        job = WindowsJob(str(record["job"]["name"]))
        process = _create_process_in_job(
            command,
            cwd,
            job,
            below_normal=record["classification"] == "heavy",
        )
        if cancellation_requested(root, str(record["task_id"])):
            raise ProcessCancelled("cancelled during launch")
        top = process.identity()
        if top is None:
            raise WindowsProcessError(f"could not query child identity pid={process.pid}")
        top = _bind_task_identity(
            top,
            record,
            job_member=True,
            lifecycle="finite",
            command_line=process.command_line,
            working_directory=str(cwd),
        )
        record["top_process"] = top
        record["processes_observed"] = [top]
        record["state"] = "running"
        record["started_at"] = utc_now()
        write_task(root, record)

        deadline = time.monotonic() + timeout_seconds
        last_observation = 0.0
        while True:
            now = time.monotonic()
            if cancellation_requested(root, str(record["task_id"])):
                reason = "cancelled"
                result = 130
                break
            exit_code = process.poll()
            if now - last_observation >= 1.0 or exit_code is not None or now >= deadline:
                pids = job.pids()
                record["processes_observed"] = _merge_observed(
                    record, list(record["processes_observed"]), pids
                )
                write_task(root, record)
                last_observation = now
            if exit_code is not None:
                result = int(exit_code)
                break
            if now >= deadline:
                reason = "timeout"
                result = 124
                break
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        reason = "cancelled"
        result = 130
    except ProcessCancelled as exc:
        reason = "cancelled"
        execution_error = str(exc)
        result = 130
    except (OSError, subprocess.SubprocessError, WindowsProcessError) as exc:
        reason = "broker_error"
        execution_error = str(exc)
        result = 1
    finally:
        record["cleanup"]["attempted"] = True
        if job is not None:
            try:
                active = job.pids()
                record["processes_observed"] = _merge_observed(
                    record, list(record["processes_observed"]), active
                )
                if active:
                    record["cleanup"]["method"] = "TerminateJobObject"
                    job.terminate(124 if reason == "timeout" else 1)
                    if not job.wait_empty(5.0):
                        cleanup_error = "TerminateJobObject did not empty the verified Job within 5 seconds"
                else:
                    record["cleanup"]["method"] = "job_already_empty"
                remaining = job.pids()
                if remaining:
                    cleanup_error = cleanup_error or "verified Job still has members after TerminateJobObject"
            except (OSError, WindowsProcessError) as exc:
                cleanup_error = f"{cleanup_error}; {exc}" if cleanup_error else str(exc)
                try:
                    remaining = job.pids()
                except (OSError, WindowsProcessError):
                    remaining = [-1]
        if process is not None and process.poll() is None:
            expected = record.get("top_process")
            if isinstance(expected, dict) and job is not None:
                outcome = _terminate_verified_process(expected, 1, record=record, job=job)
                if outcome not in {"terminated", "already_exited"}:
                    cleanup_error = f"verified process cleanup: {outcome}"
                try:
                    process.wait(5.0)
                except TimeoutError:
                    if identity_matches(
                        expected, process_identity(int(expected["pid"]))
                    ):
                        cleanup_error = (
                            "top process remained identity-matched after verified cleanup"
                        )
                    else:
                        process.poll()
                if identity_matches(expected, process_identity(int(expected["pid"]))):
                    remaining = sorted(set(remaining + [int(expected["pid"])]))
        if process is not None:
            process.close()
        outcomes = _classify_record_processes(record, job=job)
        live_owned = [event for event in outcomes if event["state"] == VERIFIED_LIVE_OWNED]
        severity, hazards = _cleanup_severity(record, live_owned, cleanup_error)
        record["cleanup"]["remaining_pids"] = [int(event["pid"]) for event in live_owned]
        record["cleanup"]["verified_zero"] = not live_owned
        record["cleanup"]["error"] = cleanup_error
        record["cleanup"]["severity"] = severity
        record["cleanup"]["warnings"] = [event for event in outcomes if event["state"] not in {VERIFIED_EXITED}]
        record["cleanup"]["blockers"] = hazards if severity == CLEANUP_BLOCKER else []
        if job is not None:
            job.close()
        record["exit_code"] = result
        record["termination_reason"] = (
            f"{reason}: {execution_error}" if execution_error else reason
        )
        record["execution_error"] = execution_error
        record["finished_at"] = utc_now()
        if severity == CLEANUP_BLOCKER:
            record["state"] = "cleanup_failed"
            result = 70
        elif severity == CLEANUP_WARNING:
            record["state"] = "retired_warning"
        elif reason == "timeout":
            record["state"] = "timed_out"
        elif reason == "cancelled":
            record["state"] = "cancelled"
        elif reason == "broker_error":
            record["state"] = "failed"
        elif result == 0:
            record["state"] = "completed"
        else:
            record["state"] = "failed"
        if record["state"] == "cleanup_failed":
            write_task(root, record)
        else:
            retire_task(root, record)
    return result


def _record_processes(record: dict[str, Any]) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    top = record.get("top_process")
    if isinstance(top, dict):
        values.append(top)
    for item in record.get("processes_observed", []):
        if isinstance(item, dict):
            values.append(item)
    unique: dict[tuple[Any, Any], dict[str, Any]] = {}
    for value in values:
        unique[(value.get("pid"), value.get("creation_time_100ns"))] = value
    return list(unique.values())


def _append_process_event(record: dict[str, Any], event: dict[str, Any]) -> None:
    """Retain identity decisions without turning ordinary uncertainty into debt."""
    event = {**event, "observed_at": event.get("observed_at") or utc_now()}
    fingerprint = hashlib.sha256(
        json.dumps(
            {
                "pid": event.get("pid"), "creation_time_100ns": event.get("creation_time_100ns"),
                "state": event.get("state"), "reason": event.get("reason"),
            }, sort_keys=True
        ).encode("utf-8")
    ).hexdigest()
    event["fingerprint"] = fingerprint
    prior = record.setdefault("process_state_events", [])
    if not any(value.get("fingerprint") == fingerprint for value in prior if isinstance(value, dict)):
        prior.append(event)


def _classify_record_process(
    record: dict[str, Any], expected: dict[str, Any], job: WindowsJob | None = None
) -> dict[str, Any]:
    """Classify a PID without ever inferring ownership from proximity or ancestry."""
    pid = expected.get("pid")
    base: dict[str, Any] = {"pid": pid, "expected": expected}
    errors = identity_coherence(expected, record)
    if errors:
        return {**base, "state": OWNERSHIP_RECORD_INCONSISTENT, "reason": ";".join(errors)}
    missing = missing_ownership_fields(expected)
    if missing:
        return {**base, "state": OWNERSHIP_UNVERIFIED, "reason": "missing:" + ",".join(missing)}
    if not isinstance(pid, int) or pid <= 0:
        return {**base, "state": OWNERSHIP_UNVERIFIED, "reason": "invalid_pid"}
    try:
        handle = _open_process(pid, PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_VM_READ | SYNCHRONIZE)
    except WindowsProcessError as exc:
        return {**base, "state": OWNERSHIP_UNVERIFIED, "reason": f"open_process:{exc}"}
    if not handle:
        return {**base, "state": VERIFIED_EXITED, "reason": "pid_not_active"}
    try:
        minimal = _process_identity_from_handle(pid, handle, telemetry=False)
        if minimal is None:
            return {**base, "state": VERIFIED_EXITED, "reason": "process_exited"}
        # PID/time/path mismatch is normal reuse. Do not collect more from the replacement.
        if not identity_matches(expected, minimal):
            return {**base, "state": PID_REUSED_UNRELATED, "reason": "pid_time_or_path_mismatch", "current": minimal}
        if job is None:
            job = _open_existing_job(str(record.get("job", {}).get("name", "")))
            opened_here = True
        else:
            opened_here = False
        try:
            if job is None:
                return {**base, "state": OWNERSHIP_UNVERIFIED, "reason": "job_not_open"}
            if job.name != record.get("job", {}).get("name"):
                return {**base, "state": OWNERSHIP_RECORD_INCONSISTENT, "reason": "job_name_conflict"}
            if not job.contains(handle):
                return {**base, "state": OWNERSHIP_UNVERIFIED, "reason": "not_in_recorded_job"}
            full = _process_identity_from_handle(pid, handle)
            if full is None:
                return {**base, "state": VERIFIED_EXITED, "reason": "process_exited"}
            bound = _bind_task_identity(full, record, job_member=True, lifecycle="finite_job_member")
            coherence = identity_coherence(bound, record)
            if coherence:
                return {**base, "state": OWNERSHIP_RECORD_INCONSISTENT, "reason": ";".join(coherence)}
            return {**base, "state": VERIFIED_LIVE_OWNED, "reason": "pid_time_path_and_job_verified", "current": bound,
                    "creation_time_100ns": bound.get("creation_time_100ns")}
        finally:
            if opened_here and job is not None:
                job.close()
    finally:
        kernel32.CloseHandle(handle)


def _classify_record_processes(record: dict[str, Any], job: WindowsJob | None = None) -> list[dict[str, Any]]:
    events = [_classify_record_process(record, item, job) for item in _record_processes(record)]
    for event in events:
        _append_process_event(record, event)
    return events


def _hazards_for_live_owned(record: dict[str, Any], live: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Concrete hazard evidence only; a live but idle process is a warning, not an embargo."""
    hazards: list[dict[str, Any]] = []
    supplied = record.get("concrete_hazards", [])
    for event in live:
        current = event.get("current", {})
        pid = current.get("pid")
        creation = current.get("creation_time_100ns")
        executable = current.get("executable")
        for hazard in supplied if isinstance(supplied, list) else []:
            if not isinstance(hazard, dict) or not hazard.get("verified"):
                continue
            if (hazard.get("pid"), hazard.get("creation_time_100ns"), hazard.get("executable")) == (pid, creation, executable):
                hazards.append({"pid": pid, "kind": hazard.get("kind", "external"), "evidence": hazard.get("evidence", "verified hazard")})
        if isinstance(current.get("working_set_bytes"), int) and current["working_set_bytes"] >= 512 * 1024 * 1024:
            hazards.append({"pid": pid, "kind": "memory_pressure", "evidence": "working set at least 512MiB"})
        # CPU is sampled only after an attempted cleanup still has a verified Job
        # member. It is process-bound evidence, not a generic host-load guess.
        if isinstance(pid, int) and pid > 0:
            first = process_identity(pid)
            time.sleep(0.25)
            second = process_identity(pid)
            if identity_matches(current, first) and identity_matches(current, second):
                first_cpu = first.get("cpu_time_seconds") if first else None
                second_cpu = second.get("cpu_time_seconds") if second else None
                if isinstance(first_cpu, (int, float)) and isinstance(second_cpu, (int, float)) and second_cpu - first_cpu >= 0.02:
                    hazards.append({"pid": pid, "kind": "cpu_activity", "evidence": f"cpu advanced {second_cpu - first_cpu:.3f}s over 0.25s"})
    return hazards


def _cleanup_severity(record: dict[str, Any], live: list[dict[str, Any]], cleanup_error: str | None) -> tuple[str | None, list[dict[str, Any]]]:
    hazards = _hazards_for_live_owned(record, live)
    if live and cleanup_error and hazards:
        return CLEANUP_BLOCKER, hazards
    if cleanup_error or live:
        return CLEANUP_WARNING, hazards
    events = record.get("process_state_events", [])
    if any(isinstance(event, dict) and event.get("state") in {PID_REUSED_UNRELATED, OWNERSHIP_UNVERIFIED, OWNERSHIP_RECORD_INCONSISTENT} for event in events):
        return CLEANUP_WARNING, []
    return None, []


def _broker_alive(record: dict[str, Any]) -> bool:
    broker = record.get("broker")
    return isinstance(broker, dict) and identity_matches(
        broker, process_identity(int(broker.get("pid", -1)))
    )


def _open_existing_job(name: str) -> WindowsJob | None:
    try:
        return WindowsJob(name, open_existing=True)
    except WindowsProcessError as exc:
        code = getattr(exc, "winerror", None) or getattr(exc, "errno", None)
        if code in {2, 6}:
            return None
        raise


def reconcile(root: Path | None = None, *, dry_run: bool) -> dict[str, Any]:
    """Reconcile abandoned Jobs; warning states never block unrelated pipelines."""
    root = root or state_root()
    records, registry_errors = load_tasks(root, include_history=False)
    report: dict[str, Any] = {
        "policy": POLICY_ID,
        "dry_run": dry_run,
        "registry_errors": registry_errors,
        "reconciled": [],
        "ambiguous": [],  # compatibility name; contains warnings only
        "warnings": [],
        "cleanup_blockers": [],
        "active": [],
    }
    if os.name != "nt":
        report["unsupported"] = "Windows only"
        return report
    for record in records:
        if record.get("state") not in ACTIVE_STATES and record.get("state") != "starting":
            continue
        task_id = str(record.get("task_id"))
        if _broker_alive(record):
            report["active"].append(task_id)
            continue
        expected_name = expected_job_name(task_id)
        if record.get("job", {}).get("name") != expected_name:
            event = {"state": OWNERSHIP_RECORD_INCONSISTENT, "reason": "recorded_job_name_mismatch"}
            _append_process_event(record, event)
            record["cleanup"] = {**record.get("cleanup", {}), "attempted": True, "severity": CLEANUP_WARNING, "warnings": [event], "blockers": []}
            record["state"] = "retired_warning"
            record["finished_at"] = utc_now()
            if not dry_run:
                retire_task(root, record)
            report["warnings"].append({"task_id": task_id, "events": [event]})
            continue
        job = _open_existing_job(expected_name)
        events = _classify_record_processes(record, job)
        if job is not None:
            try:
                job_pids = job.pids()
            finally:
                job.close()
        else:
            job_pids = []
        if dry_run:
            report["reconciled"].append({"task_id": task_id, "would_terminate": job_pids, "events": events})
            continue
        cleanup_error: str | None = None
        outcomes: list[dict[str, Any]] = []
        verified_before_cleanup = any(event["state"] == VERIFIED_LIVE_OWNED for event in events)
        if job_pids and verified_before_cleanup:
            try:
                with WindowsJob(str(record["job"]["name"]), open_existing=True) as active_job:
                    active_job.terminate(1)
                    if not active_job.wait_empty(5.0):
                        cleanup_error = "TerminateJobObject did not empty the verified Job within 5 seconds"
                    if active_job.pids():
                        cleanup_error = cleanup_error or "verified Job still has members after TerminateJobObject"
                outcomes.append({"method": "TerminateJobObject", "pids": job_pids})
            except (OSError, WindowsProcessError) as exc:
                cleanup_error = str(exc)
        events = _classify_record_processes(record)
        live = [event for event in events if event["state"] == VERIFIED_LIVE_OWNED]
        severity, hazards = _cleanup_severity(record, live, cleanup_error)
        record["cleanup"] = {
            "attempted": True,
            "method": "startup_reconciliation",
            "verified_zero": not live,
            "remaining_pids": [event["pid"] for event in live],
            "error": cleanup_error,
            "severity": severity,
            "warnings": [event for event in events if event["state"] != VERIFIED_EXITED],
            "blockers": hazards if severity == CLEANUP_BLOCKER else [],
        }
        record["finished_at"] = utc_now()
        record["termination_reason"] = "broker no longer exists"
        record["state"] = "cleanup_failed" if severity == CLEANUP_BLOCKER else ("retired_warning" if severity == CLEANUP_WARNING else "reconciled")
        if record["state"] == "cleanup_failed":
            write_task(root, record)
            report["cleanup_blockers"].append({"task_id": task_id, "hazards": hazards})
        else:
            retire_task(root, record)
        report["reconciled"].append({"task_id": task_id, "outcomes": outcomes, "remaining": [event["pid"] for event in live], "events": events})
        if severity == CLEANUP_WARNING:
            report["warnings"].append({"task_id": task_id, "events": events})
    return report


def cleanup_owned(
    *,
    root: Path | None = None,
    task_id: str | None,
    all_owned: bool,
    dry_run: bool,
    verify: bool,
    owners: set[str] | None = None,
) -> dict[str, Any]:
    """Cancel selected Yakherd tasks and verify their owned Jobs are empty."""
    _require_windows()
    if not all_owned and not task_id and not owners:
        raise ProcessPolicyError("cleanup requires --task TASK_ID or --all-owned")
    if not dry_run and not verify:
        raise ProcessPolicyError("destructive cleanup requires --verify")
    if task_id:
        _validate_task_id(task_id)
    root = root or state_root()
    records, errors = load_tasks(root, include_history=False)
    selected = [
        record
        for record in records
        if all_owned
        or record.get("task_id") == task_id
        or (owners is not None and record.get("owner") in owners)
    ]
    report: dict[str, Any] = {
        "policy": POLICY_ID,
        "dry_run": dry_run,
        "verify": verify,
        "registry_errors": errors,
        "tasks": [],
    }
    for record in selected:
        item: dict[str, Any] = {"task_id": record.get("task_id"), "actions": []}
        if record.get("state") not in ACTIVE_STATES | {"starting"}:
            item["verified_pids"] = []
            item["status"] = "already_clean"
            report["tasks"].append(item)
            continue
        current_task_id = str(record.get("task_id"))
        expected_name = expected_job_name(current_task_id)
        recorded_name = record.get("job", {}).get("name")
        if recorded_name != expected_name:
            event = {"state": OWNERSHIP_RECORD_INCONSISTENT, "reason": "recorded_job_name_mismatch"}
            _append_process_event(record, event)
            item.update({"status": "cleanup_warning", "warnings": [event]})
            if not dry_run:
                record["state"] = "retired_warning"
                record["finished_at"] = utc_now()
                retire_task(root, record)
            report["tasks"].append(item)
            continue
        pre_events = _classify_record_processes(record)
        item["verified_pids"] = [int(event["pid"]) for event in pre_events if event["state"] == VERIFIED_LIVE_OWNED]
        job_pids: list[int] = []
        try:
            job = _open_existing_job(expected_name)
            if job is not None:
                try:
                    job_pids = job.pids()
                finally:
                    job.close()
        except WindowsProcessError as exc:
            item["status"] = "cleanup_warning"
            item["job_error"] = str(exc)
            report["tasks"].append(item)
            continue
        item["job_pids"] = job_pids
        if dry_run:
            item["status"] = "would_cleanup"
            report["tasks"].append(item)
            continue
        request_cancellation(root, current_task_id)
        record["state"] = "cleanup_requested"
        write_task(root, record)

        deadline = time.monotonic() + 5.0
        remaining_job: list[int] = []
        cleanup_error: str | None = None
        while True:
            try:
                job = _open_existing_job(expected_name)
                if job is not None:
                    try:
                        active = job.pids()
                        if active:
                            job.terminate(1)
                            item["actions"].append(
                                {"method": "TerminateJobObject", "pids": active}
                            )
                            if not job.wait_empty(min(1.0, max(0.0, deadline - time.monotonic()))):
                                cleanup_error = "TerminateJobObject did not empty the verified Job within the cleanup deadline"
                        remaining_job = job.pids()
                        if remaining_job:
                            cleanup_error = cleanup_error or "verified Job still has members after TerminateJobObject"
                    finally:
                        job.close()
                else:
                    remaining_job = []
            except (OSError, WindowsProcessError) as exc:
                cleanup_error = str(exc)
                remaining_job = [-1]

            if not remaining_job:
                break
            if time.monotonic() >= deadline:
                break
            time.sleep(POLL_SECONDS)

        verification_job = _open_existing_job(expected_name)
        try:
            events = _classify_record_processes(record, verification_job)
            if verification_job is not None and verification_job.pids():
                cleanup_error = cleanup_error or "verified Job still has members during final identity check"
        finally:
            if verification_job is not None:
                verification_job.close()
        live = [event for event in events if event["state"] == VERIFIED_LIVE_OWNED]
        severity, hazards = _cleanup_severity(record, live, cleanup_error)
        all_remaining = [int(event["pid"]) for event in live]
        item["remaining_pids"] = all_remaining
        item["warnings"] = [event for event in events if event["state"] not in {VERIFIED_EXITED}]
        item["status"] = "cleanup_blocker" if severity == CLEANUP_BLOCKER else ("cleanup_warning" if severity == CLEANUP_WARNING else "clean")
        record["cleanup"] = {
            "attempted": True,
            "method": "owned_cleanup",
            "verified_zero": not all_remaining,
            "remaining_pids": all_remaining,
            "error": cleanup_error,
            "severity": severity,
            "warnings": item["warnings"],
            "blockers": hazards if severity == CLEANUP_BLOCKER else [],
        }
        record["state"] = "cleaned" if item["status"] == "clean" else ("cleanup_failed" if item["status"] == "cleanup_blocker" else "retired_warning")
        record["termination_reason"] = "explicit owned cleanup"
        record["finished_at"] = utc_now()
        if record["state"] == "cleanup_failed":
            write_task(root, record)
        else:
            retire_task(root, record)
        report["tasks"].append(item)
    return report


def status_report(root: Path | None = None) -> dict[str, Any]:
    root = root or state_root()
    reconciliation = reconcile(root, dry_run=False)
    records, errors = load_tasks(root)
    now = datetime.now(timezone.utc)
    tasks = []
    for record in records:
        if record.get("state") not in ACTIVE_STATES and record.get("state") not in {"starting"}:
            continue
        live = []
        if os.name == "nt":
            events = _classify_record_processes(record)
            live = [event.get("current") for event in events if event.get("state") == VERIFIED_LIVE_OWNED]
        else:
            events = []
        started = record.get("started_at") or record.get("created_at")
        elapsed = None
        if started:
            elapsed = max(
                0.0,
                (now - datetime.fromisoformat(str(started).replace("Z", "+00:00"))).total_seconds(),
            )
        tasks.append(
            {
                "task_id": record.get("task_id"),
                "owner": record.get("owner"),
                "state": record.get("state"),
                "classification": record.get("classification"),
                "lifecycle": record.get("lifecycle"),
                "command": record.get("command"),
                "working_directory": record.get("working_directory"),
                "priority": record.get("priority"),
                "elapsed_seconds": elapsed,
                "processes": live,
                "process_states": events,
                "cleanup": record.get("cleanup"),
            }
        )
    return {
        "policy": POLICY_ID,
        "platform": sys.platform,
        "state_root": str(root),
        "active_finite_tasks": [task for task in tasks if task["state"] != "queued"],
        "queued_heavy_tasks": [task for task in tasks if task["state"] == "queued"],
        "approved_persistent_tasks": [],
        "persistent_process_support": "unsupported_fail_closed",
        "verified_live_owned_processes": [process for task in tasks for process in task["processes"]],
        "stale_pid_reuse_events": [event for task in tasks for event in task["process_states"] if event.get("state") == PID_REUSED_UNRELATED],
        "ownership_unverified_records": [event for task in tasks for event in task["process_states"] if event.get("state") == OWNERSHIP_UNVERIFIED],
        "inconsistent_identity_records": [event for task in tasks for event in task["process_states"] if event.get("state") == OWNERSHIP_RECORD_INCONSISTENT],
        "cleanup_warnings": [task for task in tasks if task.get("cleanup", {}).get("severity") == CLEANUP_WARNING],
        "cleanup_blockers": [task for task in tasks if task.get("cleanup", {}).get("severity") == CLEANUP_BLOCKER or task["state"] == "cleanup_failed"],
        "cleanup_failures": [task for task in tasks if task.get("cleanup", {}).get("severity") == CLEANUP_BLOCKER or task["state"] == "cleanup_failed"],
        "registry_errors": sorted(set(errors + reconciliation.get("registry_errors", []))),
        "reconciliation": reconciliation,
    }


def _paths_overlap(first: str, second: str) -> bool:
    try:
        first_path = os.path.normcase(str(Path(first).resolve()))
        second_path = os.path.normcase(str(Path(second).resolve()))
        common = os.path.normcase(os.path.commonpath([first_path, second_path]))
    except (OSError, ValueError):
        return False
    return common in {first_path, second_path}


def run_stop_hook(payload: dict[str, Any], root: Path | None = None) -> dict[str, Any]:
    """Cancel only tasks owned by the Codex session that emitted this stop hook."""
    event = payload.get("hook_event_name")
    if event not in {"Stop", "SubagentStop"}:
        raise ProcessPolicyError("process hook accepts only Stop or SubagentStop input")
    required = {"session_id", "turn_id", "cwd"}
    missing = [
        name
        for name in sorted(required)
        if not isinstance(payload.get(name), str) or not str(payload[name]).strip()
    ]
    if missing:
        raise ProcessPolicyError(
            "process hook requires non-empty string fields: " + ", ".join(missing)
        )

    root = root or state_root()
    session_id = str(payload["session_id"])
    turn_id = str(payload["turn_id"])
    hook_cwd = str(Path(str(payload["cwd"])).resolve())
    owners = {session_id, f"codex:{session_id}"}
    records, registry_errors = load_tasks(root, include_history=False)
    active_records = [
        record
        for record in records
        if record.get("state") in ACTIVE_STATES | {"starting"}
    ]
    scoped = [record for record in active_records if record.get("owner") in owners]
    unscoped_same_workspace = [
        record
        for record in active_records
        if record.get("owner") not in owners
        and isinstance(record.get("working_directory"), str)
        and _paths_overlap(str(record["working_directory"]), hook_cwd)
    ]

    cleanup_report: dict[str, Any] = {"tasks": [], "registry_errors": []}
    if scoped:
        cleanup_report = cleanup_owned(
            root=root,
            task_id=None,
            all_owned=False,
            dry_run=False,
            verify=True,
            owners=owners,
        )
    task_failures = [
        item
        for item in cleanup_report.get("tasks", [])
        if item.get("status") == "cleanup_blocker"
    ]
    failures = bool(task_failures)
    message = None
    if failures or registry_errors or cleanup_report.get("registry_errors") or unscoped_same_workspace:
        details = []
        if registry_errors or cleanup_report.get("registry_errors"):
            details.append("unreadable registry state (warning)")
        if task_failures:
            details.append("verified owned cleanup has a concrete hazard")
        if unscoped_same_workspace:
            details.append("active same-workspace tasks have a different owner (untouched warning)")
        message = (
            f"Y-PROC-1 {event} session={session_id} turn={turn_id} cwd={hook_cwd}: "
            + "; ".join(details)
            + ". Inspect `yakherd process status`."
        )
    return {
        "continue": not failures,
        "stopReason": "Y-PROC-1 scoped cleanup has a verified concrete hazard"
        if failures
        else None,
        "systemMessage": message,
        "suppressOutput": False,
    }


def resume_warning(root: Path | None, task_id: str) -> dict[str, Any]:
    """Explicit user continuation acknowledges warnings once; blockers cannot be waived."""
    _validate_task_id(task_id)
    root = root or state_root()
    active = task_path(root, task_id)
    archive = history_path(root, task_id)
    path = active if active.is_file() else archive
    if not path.is_file():
        raise ProcessPolicyError(f"task is not known: {task_id}")
    records, errors = load_tasks(root)
    if errors:
        # Registry corruption elsewhere remains observable, never an authorization embargo.
        pass
    record = next((item for item in records if item.get("task_id") == task_id), None)
    if record is None:
        raise ProcessPolicyError(f"task is not readable: {task_id}")
    events = _classify_record_processes(record) if os.name == "nt" else []
    live = [event for event in events if event.get("state") == VERIFIED_LIVE_OWNED]
    severity, hazards = _cleanup_severity(record, live, record.get("cleanup", {}).get("error"))
    if severity == CLEANUP_BLOCKER:
        return {"allowed": False, "task_id": task_id, "state": CLEANUP_BLOCKER, "blockers": hazards}
    fingerprint = hashlib.sha256(json.dumps(events, sort_keys=True, default=str).encode("utf-8")).hexdigest()
    authorizations = record.setdefault("resume_authorizations", [])
    already = any(item.get("fingerprint") == fingerprint for item in authorizations if isinstance(item, dict))
    if not already:
        authorizations.append({"fingerprint": fingerprint, "authorized_at": utc_now(), "reason": "explicit_resume_after_warning"})
    record["resume_authorized_at"] = utc_now()
    if record.get("state") in ACTIVE_STATES | {"starting"}:
        record["state"] = "retired_warning" if severity == CLEANUP_WARNING else "reconciled"
        record["finished_at"] = record.get("finished_at") or utc_now()
        retire_task(root, record)
    else:
        _write_json_atomic(archive, record)
    return {"allowed": True, "task_id": task_id, "already_authorized": already, "warnings": events}


def run_exec_cli(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="yakherd exec", description="Run a finite command under Y-PROC-1")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--heavy", action="store_true", help="serialize and use below-normal priority (default)")
    group.add_argument("--light", action="store_true", help="allow concurrent normal-priority execution")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--queue-timeout", type=float, default=DEFAULT_QUEUE_TIMEOUT_SECONDS)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--owner")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = list(args.command)
    if command[:1] == ["--"]:
        command.pop(0)
    classification = "light" if args.light else "heavy"
    previous_break_handler: Any = None
    break_handler_installed = False
    try:
        if os.name == "nt" and hasattr(signal, "SIGBREAK"):
            previous_break_handler = signal.getsignal(signal.SIGBREAK)

            def interrupt_on_break(_signum: int, _frame: Any) -> None:
                raise KeyboardInterrupt

            signal.signal(signal.SIGBREAK, interrupt_on_break)
            break_handler_installed = True
        return run_broker(
            command,
            cwd=args.cwd,
            classification=classification,
            timeout_seconds=args.timeout,
            queue_timeout_seconds=args.queue_timeout,
            owner=args.owner,
        )
    except (ProcessPolicyError, WindowsProcessError, OSError) as exc:
        print(f"process_error: {exc}", file=sys.stderr)
        return 2
    finally:
        if break_handler_installed:
            signal.signal(signal.SIGBREAK, previous_break_handler)


def run_process_cli(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="yakherd process", description="Inspect and clean Y-PROC-1 state")
    subparsers = parser.add_subparsers(dest="operation", required=True)
    status = subparsers.add_parser("status")
    status.add_argument("--json", action="store_true")
    cleanup = subparsers.add_parser("cleanup")
    selection = cleanup.add_mutually_exclusive_group(required=True)
    selection.add_argument("--task")
    selection.add_argument("--all-owned", action="store_true")
    cleanup.add_argument("--dry-run", action="store_true")
    cleanup.add_argument("--verify", action="store_true")
    resume = subparsers.add_parser("resume", help="explicitly continue after Y-PROC-1.1 warnings")
    resume.add_argument("--task", required=True)
    subparsers.add_parser("hook", help="Stop/SubagentStop session-owned cleanup hook")
    args = parser.parse_args(argv)
    try:
        if args.operation == "status":
            report = status_report()
        elif args.operation == "cleanup":
            report = cleanup_owned(
                task_id=args.task,
                all_owned=args.all_owned,
                dry_run=args.dry_run,
                verify=args.verify,
            )
        elif args.operation == "resume":
            report = resume_warning(None, args.task)
        else:
            payload = json.load(sys.stdin)
            if not isinstance(payload, dict):
                raise ProcessPolicyError("process hook input must be a JSON object")
            print(json.dumps(run_stop_hook(payload), sort_keys=True))
            return 0
        print(json.dumps(report, indent=2, sort_keys=True))
        failures = report.get("cleanup_blockers") or report.get("cleanup_failures") or [
            item for item in report.get("tasks", []) if item.get("status") == "cleanup_blocker"
        ]
        if args.operation == "resume" and not report.get("allowed"):
            return 1
        return 1 if failures else 0
    except (ProcessPolicyError, WindowsProcessError, OSError, json.JSONDecodeError) as exc:
        print(f"process_error: {exc}", file=sys.stderr)
        return 2
