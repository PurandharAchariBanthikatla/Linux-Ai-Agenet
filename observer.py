"""
Observer: Evaluates command results and decides if they succeeded or failed
"""


ERROR_KEYWORDS = [
    "error", "failed", "not found", "permission denied",
    "no such file", "command not found", "cannot", "unable to",
    "fatal", "exception", "traceback", "refused"
]


class Observer:
    def evaluate(self, stdout: str, stderr: str, returncode: int) -> str:
        """
        Returns: 'success' or 'error'
        """
        if returncode != 0:
            return "error"

        # Even with returncode 0, some tools write errors to stdout
        combined = (stdout + stderr).lower()
        for keyword in ERROR_KEYWORDS:
            if keyword in combined and returncode != 0:
                return "error"

        return "success"

    def summarize(self, stdout: str, max_lines: int = 20) -> str:
        """Truncate long output for display"""
        lines = stdout.strip().splitlines()
        if len(lines) > max_lines:
            half = max_lines // 2
            return "\n".join(lines[:half]) + f"\n... [{len(lines) - max_lines} lines hidden] ...\n" + "\n".join(lines[-half:])
        return stdout
