"""
AgentCore: Orchestrates the Plan -> Execute -> Observe -> Fix loop.
"""

from agent.executor import Executor
from agent.memory import Memory
from agent.observer import Observer
from agent.planner import Planner


class AgentCore:
    def __init__(self, settings):
        self.settings = settings
        self.planner = Planner(settings)
        self.executor = Executor(settings)
        self.observer = Observer()
        self.memory = Memory()

    def run(self, task: str):
        print(f"\nThinking about: {task}")
        print("-" * 60)

        plan = self.planner.plan(task, self.memory.get_context())
        if not plan:
            print("Could not generate a plan. Try rephrasing your task.")
            return

        print(f"Plan: {plan.get('summary', 'Executing steps...')}\n")
        steps = plan.get("steps", [])

        if not steps:
            answer = plan.get("answer", "")
            if answer:
                print(f"Answer:\n{answer}")
                self.memory.add(task, [], answer)
            return

        results = []
        for i, step in enumerate(steps, 1):
            command = step.get("command", "").strip()
            description = step.get("description", command)

            if not command:
                continue

            print(f"Step {i}/{len(steps)}: {description}")
            print(f"   $ {command}")

            output, error, returncode = self.executor.run(command)
            status = self.observer.evaluate(output, error, returncode)

            if output:
                self._print_output("Output", output)

            if status == "error":
                print(f"   Error: {error or 'Command failed with no error output.'}")

                if i <= self.settings.max_retries:
                    print("\nAttempting to fix...")
                    fix = self.planner.fix(command, error, self.memory.get_context())
                    if fix and fix.get("command"):
                        fixed_cmd = fix["command"]
                        print(f"   Fix: $ {fixed_cmd}")
                        output, error, returncode = self.executor.run(fixed_cmd)
                        if returncode == 0:
                            if output:
                                self._print_output("Fixed output", output)
                            else:
                                print("   Fixed. Command completed with no output.")
                            results.append({"cmd": fixed_cmd, "out": output, "status": "fixed"})
                        else:
                            print(f"   Fix failed: {error or 'No error output.'}")
                            results.append({"cmd": command, "out": error, "status": "failed"})
                    else:
                        print("   No fix available. Skipping step.")
                        results.append({"cmd": command, "out": error, "status": "failed"})
                else:
                    results.append({"cmd": command, "out": error, "status": "failed"})
            else:
                if not output:
                    print("   Command completed with no output.")
                results.append({"cmd": command, "out": output, "status": "success"})

            print()

        success = sum(1 for r in results if r["status"] in ("success", "fixed"))
        total = len(results)
        print("-" * 60)
        print(f"Done. {success}/{total} steps completed successfully.\n")

        self.memory.add(task, results, plan.get("summary", ""))

    def show_history(self):
        history = self.memory.get_history()
        if not history:
            print("No history yet.")
            return
        print("\nSession History:")
        for i, item in enumerate(history, 1):
            print(f"  {i}. [{item['time']}] {item['task']} -> {item['summary']}")

    def clear_history(self):
        self.memory.clear()

    def doctor(self):
        print("\nAgent Doctor")
        print("-" * 60)
        checks = [
            ("Operating system", self.settings.os_name),
            ("Groq API key", "configured" if self.settings.api_key else "missing"),
            ("Groq model", self.settings.model),
            ("Dry run", str(self.settings.dry_run)),
            ("Command timeout", f"{self.settings.command_timeout}s"),
            ("Max output lines", str(self.settings.max_output_lines)),
        ]
        for label, value in checks:
            print(f"{label}: {value}")

        commands = [
            ("Git repository", "git rev-parse --is-inside-work-tree"),
            ("Git available", "git --version"),
            (
                "Docker available",
                f'"{self.settings.powershell_path}" -NoProfile -Command "if (Get-Command docker -ErrorAction SilentlyContinue) {{ docker --version }} else {{ \'not installed or not on PATH\' }}"',
            ),
            (
                "Port 8080",
                f'"{self.settings.powershell_path}" -NoProfile -Command "if (Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue) {{ \'in use\' }} else {{ \'free\' }}"',
            ),
        ]
        for label, command in commands:
            output, error, returncode = self.executor.run(command)
            value = output or error or "no output"
            print(f"{label}: {value.strip()} (exit {returncode})")

    def _print_output(self, label: str, text: str):
        display_output = self.observer.summarize(text, self.settings.max_output_lines)
        print(f"   {label}:\n{self._indent(display_output)}")

    def _indent(self, text: str, spaces: int = 5) -> str:
        prefix = " " * spaces
        return "\n".join(prefix + line for line in text.strip().splitlines())
