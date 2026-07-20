"""
Docker tool: Wrappers for common Docker operations
"""

from tools.shell import run


def list_containers(all: bool = False) -> str:
    flag = "-a" if all else ""
    out, _, _ = run(f"docker ps {flag}")
    return out


def container_logs(name: str, tail: int = 50) -> str:
    out, _, _ = run(f"docker logs --tail={tail} {name}")
    return out


def list_images() -> str:
    out, _, _ = run("docker images")
    return out


def container_stats() -> str:
    out, _, _ = run("docker stats --no-stream")
    return out


def exec_command(container: str, command: str) -> str:
    out, err, _ = run(f"docker exec {container} {command}")
    return out or err


def remove_stopped() -> str:
    out, _, _ = run("docker container prune -f")
    return out


def docker_compose_status(path: str = ".") -> str:
    out, _, _ = run(f"cd {path} && docker-compose ps")
    return out
