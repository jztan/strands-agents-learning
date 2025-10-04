# Learn Strands Agent Framework - Hands-On Tutorial

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Strands](https://img.shields.io/badge/Strands-Agent%20Framework-green.svg)](https://strandsagents.com/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> **Learn by Building**: Master the Strands Agent Framework through 7 progressive, hands-on lessons that take you from beginner to expert.

## 🎯 What You'll Learn

This repository provides a complete **hands-on learning path** for the Strands Agent Framework. You'll master **8 agent design patterns** through progressive, practical examples:

- **Basic Conversational** → **Tool-Enhanced** → **Stateful** → **Asynchronous** → **Context-Aware** → **Multi-Agent Systems**

Each lesson teaches a distinct architectural pattern with working code you can run, modify, and build upon.

## ✨ Features

- 🚀 **7 Progressive Lessons** - Each builds on the previous
- 🛠️ **Hands-On Approach** - Working code you can run immediately
- 📋 **Clear Success Criteria** - Know when you've mastered each concept
- 🔬 **Built-in Experiments** - Explore and modify examples
- 📚 **Complete Documentation** - Detailed explanations and troubleshooting
- ⚡ **Modern Setup** - Uses `uv` for fast Python package management

## 🏃‍♂️ Quick Start

### Prerequisites

- **Python 3.10+**
- **uv** package manager ([install guide](https://docs.astral.sh/uv/))
- **AI Model API Key** - Choose one:
  - **OpenAI** ([get key](https://platform.openai.com/api-keys)) - Recommended
  - **Anthropic** ([get key](https://console.anthropic.com/)) - Alternative
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
| **Beginner** | **Lesson 1: Hello World** ✅ | Basic Conversational | Agent basics, system prompts, sync/async |
| | **Lesson 2: First Tool** ✅ | Tool-Enhanced | @tool decorator, calculator, error handling |
| | **Lesson 3: Multiple Tools** ✅ | Tool-Enhanced | Tool coordination, weather/time/converter |
| **Intermediate** | **Lesson 4: Stateful Tools** 🚧 | Stateful | Persistence, state management, todo lists |
| | **Lesson 5: Async & Streaming** 🚧 | Asynchronous | File processing, progress updates |
| **Advanced** | **Lesson 6: Context-Aware** 🚧 | Context-Aware | Self-introspection, adaptive behavior |
| | **Lesson 7: Multi-Agent** 🚧 | Graph, Swarm & Workflow | Multi-agent collaboration patterns |

**Each lesson includes:** Clear learning objectives • Working code examples • Hands-on experiments • Success criteria • Common pitfalls

## 🗂️ Project Structure

```
strands-agents-learning/
├── README.md                        # Project overview and quick start
├── TROUBLESHOOTING.md               # Common issues and solutions
├── pyproject.toml                   # Project dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore configuration
├── LICENSE                          # Apache 2.0 license
├── lesson_utils.py                  # Shared utilities for all lessons
├── lesson_01_hello_world.py         # Lesson 1: Python script ✅
├── lesson_01_hello_world.ipynb      # Lesson 1: Jupyter notebook ✅
├── lesson_02_first_tool.py          # Lesson 2: Python script ✅
├── lesson_02_first_tool.ipynb       # Lesson 2: Jupyter notebook ✅
├── lesson_03_multiple_tools.py      # Lesson 3: Python script ✅
├── lesson_03_multiple_tools.ipynb   # Lesson 3: Jupyter notebook ✅
├── setup_notebook_filter.sh         # Clean notebook outputs before commits
└── experiments/                     # Your experimental code goes here
    └── .gitignore                   # Keeps experiments local
```

## 💡 Learning Tips

- **Start Simple**: Begin with Lesson 1, don't skip ahead
- **Run the Code**: Execute every example to see it in action
- **Experiment**: Modify examples and see what happens
- **Use the Experiments Folder**: Try your own variations
- **Debug Thoughtfully**: When things break, understand why

> 🛠️ **Having issues?** Check the [Troubleshooting Guide](TROUBLESHOOTING.md)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

- 🐛 **Report Issues**: Found a bug or unclear explanation? [Open an issue](https://github.com/jztan/strands-agents-learning/issues)
- 💡 **Suggest Improvements**: Ideas for better examples or explanations
- 🔧 **Submit PRs**: Fix bugs, improve code, or add new examples
- 📚 **Improve Documentation**: Make explanations clearer
- ⭐ **Share**: Star the repo if it helped you learn!

**Note:** When contributing notebook changes, run `./setup_notebook_filter.sh` before committing to remove execution outputs. This keeps the repository lightweight and prevents accidental exposure of API responses.

## 📖 Additional Resources

- **[Strands Documentation](https://strandsagents.com/latest/documentation/)** - Official framework docs
- **[Strands GitHub](https://github.com/strandsagents/strands-agents)** - Source code and issues

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

**[⬆️ Back to Top](#learn-strands-agent-framework---hands-on-tutorial)**