"""
Shell tool: Utility functions for running common Linux commands
"""

import subprocess


def run(command: str, timeout: int = 30) -> tuple[str, str, int]:
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def disk_usage(path: str = "/") -> str:
    out, _, _ = run(f"df -h {path}")
    return out


def top_dirs(path: str = ".", n: int = 5) -> str:
    out, _, _ = run(f"du -sh {path}/* 2>/dev/null | sort -rh | head -{n}")
    return out


def memory_info() -> str:
    out, _, _ = run("free -h")
    return out


def cpu_info() -> str:
    out, _, _ = run("top -bn1 | head -20")
    return out


def list_processes(name: str = "") -> str:
    if name:
        out, _, _ = run(f"ps aux | grep {name} | grep -v grep")
    else:
        out, _, _ = run("ps aux --sort=-%cpu | head -15")
    return out


def check_port(port: int) -> str:
    out, _, _ = run(f"ss -tulnp | grep :{port}")
    return out or f"Port {port} is not in use"


def uptime_info() -> str:
    out, _, _ = run("uptime")
    return out
