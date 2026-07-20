"""
Executor: Runs shell commands safely with timeout and output capture
"""

import subprocess


# Commands that are NEVER allowed (safety layer)
BLOCKED_COMMANDS = [
    "rm -rf /",
    "rm -rf /*",
    "del /s /q c:\\",
    "format c:",
    "mkfs",
    "dd if=/dev/zero",
    ":(){:|:&};:",   # Fork bomb
    "shutdown",
    "reboot",
    "halt",
    "poweroff",
]


class Executor:
    def __init__(self, settings):
        self.settings = settings

    def run(self, command: str) -> tuple[str, str, int]:
        """
        Execute a shell command.
        Returns: (stdout, stderr, returncode)
        """
        command = self._normalize_command(command)

        if self._is_blocked(command):
            return "", f"BLOCKED: Command '{command}' is not allowed for safety reasons.", 1

        if self.settings.dry_run:
            print(f"   [DRY RUN] Would execute: {command}")
            return "[dry-run output]", "", 0

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.settings.command_timeout
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode

        except subprocess.TimeoutExpired:
            return "", f"Command timed out after {self.settings.command_timeout}s", 1

        except Exception as e:
            return "", str(e), 1

    def _is_blocked(self, command: str) -> bool:
        cmd_lower = command.lower().strip()
        for blocked in BLOCKED_COMMANDS:
            if blocked in cmd_lower:
                return True
        return False

    def _normalize_command(self, command: str) -> str:
        """Make common AI-generated Windows paths executable in cmd.exe."""
        if self.settings.os_name != "Windows":
            return command

        ps = self.settings.powershell_path
        if command.startswith(ps):
            return f'"{ps}"{command[len(ps):]}'

        docker = "C:/Program Files/Docker/Docker/Resources/bin/docker.exe"
        if command.startswith(docker):
            return f'"{docker}"{command[len(docker):]}'

        return command
