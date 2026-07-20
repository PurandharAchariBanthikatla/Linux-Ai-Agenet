"""
Git tool: Common Git operations for DevOps workflows
"""

from tools.shell import run


def status() -> str:
    out, _, _ = run("git status")
    return out


def recent_commits(n: int = 5) -> str:
    out, _, _ = run(f"git log --oneline -n {n}")
    return out


def diff() -> str:
    out, _, _ = run("git diff --stat")
    return out


def branches() -> str:
    out, _, _ = run("git branch -a")
    return out


def push(branch: str = "") -> str:
    cmd = f"git push origin {branch}" if branch else "git push"
    out, err, rc = run(cmd)
    return out or err


def pull() -> str:
    out, err, rc = run("git pull")
    return out or err


def add_and_commit(message: str) -> str:
    run("git add -A")
    out, err, rc = run(f'git commit -m "{message}"')
    return out or err
