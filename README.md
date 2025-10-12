# Learn Strands Agent Framework - Hands-On Tutorial

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Strands](https://img.shields.io/badge/Strands-Agent%20Framework-green.svg)](https://strandsagents.com/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> **Learn by Building**: Master the Strands Agent Framework through 10 comprehensive, hands-on lessons covering everything from basics to production deployment.

## 🎯 What You'll Learn

This repository provides a complete **hands-on learning path** for the Strands Agent Framework. You'll master **10+ agent design patterns** through progressive, practical examples:

- **Foundation** → **Intermediate** → **Advanced** → **Multi-Agent** → **Production**
- **Basic Conversational** → **Tool-Enhanced** → **State & Async** → **Hooks & Context** → **Multi-Agent Orchestration** → **Distributed Systems** → **Production-Ready**

Each lesson teaches distinct architectural patterns with working code you can run, modify, and build upon.

## ✨ Features

- 🚀 **10 Comprehensive Lessons** - Complete coverage of Strands SDK
- 🛠️ **Hands-On Approach** - Working code you can run immediately
- 📋 **Clear Success Criteria** - Know when you've mastered each concept
- 🔬 **Built-in Experiments** - Explore and modify examples
- 📚 **Complete Documentation** - Detailed explanations and troubleshooting
- 🏗️ **Production-Ready Patterns** - Safety, security, and observability
- ⚡ **Modern Setup** - Uses `uv` for fast Python package management

## 🏃‍♂️ Quick Start

### Prerequisites

- **Python 3.10+**
- **uv** package manager ([install guide](https://docs.astral.sh/uv/))
- **AI Model API Key** - Choose one:
  - **OpenAI** ([get key](https://platform.openai.com/api-keys)) - Recommended
  - **Anthropic** ([get key](https://console.anthropic.com/)) - Alternative
  - **Google Gemini** ([get key](https://aistudio.google.com/app/apikey)) - Alternative
  - **AWS Bedrock** ([setup guide](https://docs.aws.amazon.com/bedrock/latest/userguide/setting-up.html)) - Enterprise
  - **Ollama** (local, free) - For advanced users
- Basic understanding of Python async/await and decorators

### Get Started in 4 Steps

#### Step 1: Clone the Repository
```bash
git clone https://github.com/jztan/strands-agents-learning.git
cd strands-agents-learning
```

#### Step 2: Install Dependencies
```bash
# Install core dependencies
uv sync

# For Jupyter notebooks (recommended for interactive learning)
uv sync --dev

# ONE-TIME: Install Jupyter kernel (required for notebooks)
uv run python -m ipykernel install --user \
  --name=strands-learning \
  --display-name="Python (Strands)"
```

#### Step 3: Configure API Key
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add ONE of the following:
# OPENAI_API_KEY=your_openai_key_here        # ← Recommended
# ANTHROPIC_API_KEY=your_anthropic_key_here  # ← Alternative
# GOOGLE_API_KEY=your_google_key_here        # ← Alternative

# Or configure AWS Bedrock (requires AWS credentials + model access):
# Step 1: Configure AWS credentials
#   aws configure  # Enter AWS Access Key ID and Secret Access Key
# Step 2: Enable model access (one-time)
#   Visit: https://console.aws.amazon.com/bedrock/
#   Go to: Model access (left sidebar)
#   Enable: Amazon Nova Lite model
```

#### Step 4: Run Your First Lesson

**Option A: Python Scripts** (complete lessons)
```bash
uv run python lesson_01_hello_world.py
```

**Option B: Jupyter Notebooks** (interactive, recommended)
```bash
# Using Jupyter Notebook
uv run jupyter notebook lesson_01_hello_world.ipynb

# Or using Jupyter Lab (modern interface)
uv run jupyter lab lesson_01_hello_world.ipynb
```

✨ **That's it!** You now have a working Strands agent with intelligent provider selection.

### 📓 Two Learning Formats

This repository provides **two formats** for each lesson:

| Format | File Type | Best For | Key Features |
|--------|-----------|----------|--------------|
| **Python Scripts** 📄 | `.py` | Reference & Production | • Run complete lessons end-to-end<br>• Easy execution: `uv run python lesson_XX.py`<br>• See full flow from start to finish<br>• Better for version control |
| **Jupyter Notebooks** 📓 | `.ipynb` | Learning & Experimenting | • Run code cell-by-cell<br>• Experiment and modify inline<br>• See outputs immediately<br>• Add your own notes<br>• No async event loop issues<br>• **Recommended for self-paced learning** |

**Quick decision:**
- 🎓 **Learning/Experimenting?** → Use Jupyter Notebooks (`.ipynb`)
- 📚 **Reference/Production?** → Use Python Scripts (`.py`)

## 📚 Learning Path & Agent Patterns

| Level | Lesson | Agent Pattern | Topics |
|-------|--------|---------------|--------|
| **Foundation** | **Lesson 1: Hello World** ✅ | Basic Conversational | Agent basics, system prompts, sync/async |
| | **Lesson 2: First Tool** ✅ | Tool-Enhanced | @tool decorator, calculator, error handling |
| | **Lesson 3: Multiple Tools** ✅ | Tool-Enhanced | Tool coordination, weather/time/converter |
| **Intermediate** | **Lesson 4: Agent State** ✅ | State & Sessions | agent.state API, FileSessionManager, persistence |
| | **Lesson 5: Async & Executors** ✅ | Async Streaming & Multi-modal | Async tools, yield, executors, images, PDFs |
| **Advanced** | **Lesson 6: Hooks & Output** 🚧 | Hooks & Structured | Lifecycle hooks, Pydantic models, logging |
| | **Lesson 7: Advanced Tools & MCP** 🚧 | Context-Aware & Integration | Class-based tools, ToolContext, conversation mgmt, MCP |
| **Multi-Agent** | **Lesson 8: Orchestration** 🚧 | Graph, Swarm & Workflow | Multi-agent patterns, state sharing |
| | **Lesson 9: Distributed Agents** 🚧 | Agents-as-Tools & A2A | Hierarchical agents, cross-platform communication |
| **Production** | **Lesson 10: Production** 🚧 | Safety, Observability & Eval | Guardrails, PII redaction, OpenTelemetry, testing |
| **Bonus** | **AWS Deployment** 🚧 | Lambda, EC2, ECS, Bedrock | Serverless, containers, managed AI, IaC |

**Progress: 5/10 lessons complete (50%)** • **Each lesson includes:** Learning objectives • Working code • Experiments • Success criteria • Common pitfalls

## 🗂️ Repository Overview

Each lesson comes in two formats:
- **`.py` files** - Complete Python scripts for reference
- **`.ipynb` files** - Interactive Jupyter notebooks for learning

Key files:
- `lesson_utils.py` - Shared utilities (model creation, environment setup)
- `.env.example` - Template for API key configuration
- `experiments/` - Your sandbox for trying variations (gitignored)

For detailed project structure and development setup, see [CONTRIBUTING.md](CONTRIBUTING.md).

## 💡 Learning Tips

- **Start Simple**: Begin with Lesson 1, don't skip ahead
- **Run the Code**: Execute every example to see it in action
- **Experiment**: Modify examples and see what happens
- **Use the Experiments Folder**: Try your own variations
- **Debug Thoughtfully**: When things break, understand why

> 🛠️ **Having issues?** Check the [Troubleshooting Guide](TROUBLESHOOTING.md)

## 🤝 Contributing

We welcome contributions! Whether you want to report bugs, suggest improvements, or submit code - we'd love your help.

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup and workflow
- Coding standards and best practices
- Testing guidelines
- How to submit pull requests

## 📖 Additional Resources

- **[Strands Documentation](https://strandsagents.com/latest/documentation/docs/)** - Official framework docs
- **[Strands GitHub](https://github.com/strands-agents/sdk-python)** - Source code and issues

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

**[⬆️ Back to Top](#learn-strands-agent-framework---hands-on-tutorial)**