# 🤖 Linux AI Agent — Purandhar's DevOps Assistant

A personal AI-powered CLI agent that understands natural language tasks and executes them on your Linux machine using Claude (Anthropic).

## Features

- 🧠 **Natural language** → shell commands via Claude API
- 🔄 **Auto-retry & self-fix** — if a command fails, the agent asks Claude to fix it
- 🐳 **DevOps-ready** — Docker, Kubernetes, AWS CLI, Git, Terraform support
- 💾 **Session memory** — tracks what you've done this session
- 🛡️ **Safety layer** — blocks dangerous commands (rm -rf /, etc.)

## Quick Start

```bash
# 1. Clone / download
cd linux-ai-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env
nano .env   # Add ANTHROPIC_API_KEY=your_key_here

# 4. Run!
python main.py
```

## Usage Examples

```
🟢 Your Task > Check disk usage and show top 5 largest directories
🟢 Your Task > List all running docker containers and their memory usage
🟢 Your Task > Show git status and last 5 commits
🟢 Your Task > Check if port 8080 is already in use
🟢 Your Task > Find all .log files larger than 100MB
🟢 Your Task > Show failed systemd services
🟢 Your Task > List all AWS S3 buckets in ap-south-1
```

## Special Commands

| Command | Action |
|---------|--------|
| `history` | Show all tasks done this session |
| `clear` | Clear session history |
| `exit` / `quit` | Stop the agent |

## Project Structure

```
linux-ai-agent/
├── main.py              # CLI entry point
├── agent/
│   ├── core.py          # Main Plan→Execute→Fix loop
│   ├── planner.py       # Claude API integration
│   ├── executor.py      # Shell command runner
│   ├── observer.py      # Success/error detection
│   └── memory.py        # Session history
├── tools/
│   ├── shell.py         # Linux system commands
│   ├── docker_tool.py   # Docker operations
│   ├── git_tool.py      # Git operations
│   ├── aws_tool.py      # AWS CLI wrappers
│   └── file_ops.py      # File read/write/search
├── config/
│   └── settings.py      # Configuration
├── tests/
│   └── test_executor.py
├── .env                 # Your API key (not committed)
└── requirements.txt
```

## Built by Purandhar Achari Banthikatla
- GitHub: [PurandharAchariBanthikatla](https://github.com/PurandharAchariBanthikatla)
- LinkedIn: [linkedin.com/in/purandhar-achari-banthi-katla-726a73265](https://linkedin.com/in/purandhar-achari-banthi-katla-726a73265)
- #PurandharLearns
