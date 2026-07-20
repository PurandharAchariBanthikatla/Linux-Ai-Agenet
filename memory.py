"""
Memory: Tracks what the agent has done this session
"""

from datetime import datetime


class Memory:
    def __init__(self):
        self._history = []

    def add(self, task: str, results: list, summary: str):
        self._history.append({
            "task": task,
            "summary": summary,
            "results": results,
            "time": datetime.now().strftime("%H:%M:%S")
        })

    def get_context(self, last_n: int = 3) -> str:
        """Return last N tasks as context string for Claude"""
        if not self._history:
            return ""
        recent = self._history[-last_n:]
        lines = []
        for item in recent:
            lines.append(f"[{item['time']}] Task: {item['task']} → {item['summary']}")
        return "\n".join(lines)

    def get_history(self) -> list:
        return self._history

    def clear(self):
        self._history = []
