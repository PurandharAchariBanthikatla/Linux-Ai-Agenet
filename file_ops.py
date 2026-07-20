"""
File operations: Safe file reading, searching, and writing
"""

import os


def read_file(path: str, max_lines: int = 100) -> str:
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        if len(lines) > max_lines:
            return "".join(lines[:max_lines]) + f"\n... [{len(lines) - max_lines} more lines] ..."
        return "".join(lines)
    except Exception as e:
        return f"Error reading {path}: {e}"


def write_file(path: str, content: str) -> str:
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"✅ Written to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"


def search_in_file(path: str, keyword: str) -> str:
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        matches = [(i+1, l.strip()) for i, l in enumerate(lines) if keyword.lower() in l.lower()]
        if not matches:
            return f"No matches for '{keyword}' in {path}"
        return "\n".join(f"Line {n}: {l}" for n, l in matches)
    except Exception as e:
        return f"Error: {e}"


def list_dir(path: str = ".") -> str:
    try:
        items = os.listdir(path)
        dirs = [f"📁 {i}" for i in items if os.path.isdir(os.path.join(path, i))]
        files = [f"📄 {i}" for i in items if os.path.isfile(os.path.join(path, i))]
        return "\n".join(sorted(dirs) + sorted(files))
    except Exception as e:
        return f"Error: {e}"
