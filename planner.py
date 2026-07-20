"""
Planner: Sends tasks to Groq and gets structured shell steps back
"""

import json
from groq import Groq


SYSTEM_PROMPT = """You are an expert Linux DevOps AI Agent. Your job is to help a DevOps/Cloud Engineer named Purandhar execute tasks on his Linux machine.

When given a task, respond ONLY with a valid JSON object. No markdown, no explanation outside the JSON.

For tasks that need shell commands, respond with:
{
  "summary": "One-line description of what you're doing",
  "steps": [
    {"command": "shell command here", "description": "What this step does"},
    {"command": "another command", "description": "What this does"}
  ]
}

For tasks that are questions or don't need commands:
{
  "summary": "Question answered",
  "steps": [],
  "answer": "Your explanation here"
}

Rules:
- Use safe, non-destructive commands by default
- Prefer commands that work on the operating system named in the user's task context
- On Windows, use commands that work from cmd.exe, or wrap PowerShell commands with the full path: C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -NoProfile -Command "..."
- On Windows port checks, use Get-NetTCPConnection through the full PowerShell path instead of netstat
- On Windows, quote executable paths that contain spaces, such as "C:/Program Files/Docker/Docker/Resources/bin/docker.exe"
- For Git tasks, first check whether the current directory is inside a Git repository with: git rev-parse --is-inside-work-tree
- If the current directory is not a Git repository, explain that the user must cd into a repo instead of running git status/log
- For "check whether" tasks, prefer commands that print a clear yes/no result and exit with code 0 for both yes and no
- For Git repository checks on Windows, use a PowerShell if statement around git rev-parse so "not a repo" prints a message instead of becoming a failed step
- For Docker installation checks on Windows, use Get-Command docker -ErrorAction SilentlyContinue in a PowerShell if statement and print "Docker is installed" or "Docker is not installed or not on PATH"
- For disk usage on Windows, avoid recursive scans of the whole C drive because they can time out. Prefer quick commands such as Get-PSDrive, or scan only the current project directory.
- For Docker, Kubernetes, AWS CLI, Git, Terraform — use correct CLI syntax
- Break complex tasks into clear sequential steps
- If a task is dangerous (rm -rf /, format disk), refuse with answer explaining why
- Keep commands simple and readable
"""

FIX_PROMPT = """A command failed. Suggest a fix for this operating system: {os_name}.

Failed command: {command}
Error output: {error}

Respond ONLY with JSON:
{{
  "command": "fixed command here",
  "explanation": "What was wrong and what changed"
}}

If no fix is possible, respond with:
{{
  "command": "",
  "explanation": "Why it cannot be fixed"
}}
"""


class Planner:
    def __init__(self, settings):
        self.settings = settings
        self.client = Groq(api_key=settings.api_key)

    def plan(self, task: str, context: str = "") -> dict:
        user_message = f"Operating system: {self.settings.os_name}\nTask: {task}"
        if context:
            user_message += f"\n\nRecent context:\n{context}"

        try:
            response = self.client.chat.completions.create(
                model=self.settings.model,
                max_tokens=self.settings.max_tokens,
                temperature=0,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )
            raw = response.choices[0].message.content.strip()
            return self._parse_json(raw)
        except Exception as e:
            print(f"❌ Groq planner error: {e}")
            return {}

    def fix(self, command: str, error: str, context: str = "") -> dict:
        prompt = FIX_PROMPT.format(
            os_name=self.settings.os_name,
            command=command,
            error=error[:500],
        )
        try:
            response = self.client.chat.completions.create(
                model=self.settings.model,
                max_tokens=512,
                temperature=0,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            )
            raw = response.choices[0].message.content.strip()
            return self._parse_json(raw)
        except Exception as e:
            print(f"❌ Groq fix planner error: {e}")
            return {}

    def _parse_json(self, text: str) -> dict:
        # Strip markdown fences if present
        text = text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:-1])
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from mixed text
            import re
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except Exception:
                    pass
            return {"summary": "Parse error", "steps": [], "answer": text}
