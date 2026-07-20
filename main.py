#!/usr/bin/env python3
"""
Linux AI Agent - Purandhar's DevOps Assistant
Entry point for the CLI interface.
"""

import sys

from dotenv import load_dotenv

from agent.core import AgentCore
from config.settings import Settings

load_dotenv()

BANNER = """
============================================================
  LINUX AI AGENT by Purandhar
  DevOps & Cloud Engineering Assistant
  Powered by Groq
============================================================
Type a task in natural language.

Examples:
  Check disk usage for this current project folder only
  Check whether Docker is installed
  Check whether this folder is a git repository
  Check if port 8080 is in use

Special commands:
  doctor   Check local tools and configuration
  history  Show session history
  clear    Clear session history
  exit     Stop the agent
"""


def main():
    settings = Settings()

    if not settings.api_key:
        print("ERROR: GROQ_API_KEY not set in .env file")
        print("Create a .env file with: GROQ_API_KEY=your_key_here")
        sys.exit(1)

    agent = AgentCore(settings)
    print(BANNER)

    while True:
        try:
            task = input("\nYour Task > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAgent stopped. Goodbye!")
            break

        if not task:
            continue

        command = task.lower()

        if command in ("exit", "quit", "bye"):
            print("Agent stopped. Goodbye!")
            break

        if command == "history":
            agent.show_history()
            continue

        if command == "clear":
            agent.clear_history()
            print("Session history cleared.")
            continue

        if command in ("doctor", "status"):
            agent.doctor()
            continue

        agent.run(task)


if __name__ == "__main__":
    main()
