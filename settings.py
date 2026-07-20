import os
import platform

class Settings:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.os_name = platform.system()
        self.max_tokens = 2048
        self.max_retries = 3          # How many times to retry on error
        self.command_timeout = int(os.getenv("COMMAND_TIMEOUT", "30"))
        self.max_output_lines = int(os.getenv("MAX_OUTPUT_LINES", "40"))
        self.max_steps = 10           # Max steps per task
        self.log_file = "logs/agent.log"
        self.dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
        self.powershell_path = "C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
