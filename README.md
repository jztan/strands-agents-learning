# Learn Strands Agent Framework - Hands-On Tutorial

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Strands](https://img.shields.io/badge/Strands-Agent%20Framework-green.svg)](https://strandsagents.com/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

> **Learn by Building**: Master the Strands Agent Framework through 7 progressive, hands-on lessons that take you from beginner to expert.

## 🎯 What You'll Learn

This repository provides a complete **hands-on learning path** for the Strands Agent Framework. You'll build a **Personal AI Assistant** that evolves through increasingly sophisticated agent design patterns:

- **Basic Conversational Agent** → **Tool-Enhanced** → **Stateful** → **Asynchronous** → **Context-Aware** → **Multi-Agent Systems**

By the end, you'll have deep understanding of **7 different agent architectures** and a fully functional AI assistant you built yourself.

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

```bash
# 1. Clone and enter the repository
git clone https://github.com/jztan/strands-agents-learning.git
cd strands-agents-learning

# 2. Install dependencies
uv sync

# For interactive Jupyter notebooks (recommended for learning):
uv sync --dev

# ⚠️ ONE-TIME: Install Jupyter kernel (required for notebooks)
uv run python -m ipykernel install --user --name=strands-learning --display-name="Python (Strands)"

# 3. Set up your API key (choose one)
cp .env.example .env
# Edit .env and add one of:
# OPENAI_API_KEY=your_openai_key_here (recommended)
# ANTHROPIC_API_KEY=your_anthropic_key_here

# 4. Choose your learning format:

# Option A: Python Scripts (run complete lessons)
uv run python lesson_01_hello_world.py

# Option B: Jupyter Notebooks (interactive, cell-by-cell)
uv run jupyter notebook lesson_01_hello_world.ipynb
# The notebook will automatically use the "Python (Strands)" kernel

# Or use Jupyter Lab (modern interface):
uv run jupyter lab lesson_01_hello_world.ipynb
```

That's it! You now have a working Strands agent with intelligent provider selection. 🎉

### 📓 Two Learning Formats

This repository supports **two ways to learn**:

1. **Python Scripts** (`.py` files)
   - ✅ Run complete lessons end-to-end
   - ✅ Easy to execute: `uv run python lesson_XX.py`
   - ✅ Good for seeing full flow
   - ✅ Better for version control

2. **Jupyter Notebooks** (`.ipynb` files) - **Recommended for learning!**
   - ✅ Run code cell-by-cell
   - ✅ Experiment and modify inline
   - ✅ See outputs immediately
   - ✅ Add your own notes
   - ✅ No async event loop issues
   - ✅ Perfect for self-paced learning

**Choose based on your goal:**
- **Learning/Experimenting?** → Use notebooks 📓
- **Reference/Production?** → Use scripts 📄

## 📊 Progress Tracker

**Overall Progress: 2/7 lessons complete (29%)**

| Status | Lesson | Topic | Time | Concepts |
|--------|--------|-------|------|----------|
| ✅ | **Lesson 1** | Hello World Agent | 2h | Agent basics, system prompts, sync/async |
| ✅ | **Lesson 2** | First Tool | 2h | @tool decorator, calculator, error handling |
| 🚧 | **Lesson 3** | Multiple Tools | 3h | Tool coordination, weather/time APIs |
| 🚧 | **Lesson 4** | Stateful Tools | 3h | Persistence, state management, todo lists |
| 🚧 | **Lesson 5** | Async & Streaming | 3h | File processing, progress updates |
| 🚧 | **Lesson 6** | Context-Aware | 4h | Self-introspection, adaptive behavior |
| 🚧 | **Lesson 7** | Multi-Agent Systems | 4h | Graph/Swarm patterns, collaboration |

**Legend:** ✅ Complete | 🚧 TBC (To Be Created)

---

## 📚 Learning Path

### **Beginner Level (Lessons 1-3)** - *4-6 hours*
- **Lesson 1**: Hello World Agent - Basic conversational agent ✅
- **Lesson 2**: First Tool - Add calculation capabilities ✅
- **Lesson 3**: Multiple Tools - Weather, time, and unit conversion *(TBC)*

### **Intermediate Level (Lessons 4-5)** - *6-8 hours* *(TBC)*
- **Lesson 4**: Stateful Tools - Todo list and note-taking with persistence *(TBC)*
- **Lesson 5**: Async & Streaming - File processing with real-time progress *(TBC)*

### **Advanced Level (Lessons 6-7)** - *8-10 hours* *(TBC)*
- **Lesson 6**: Context-Aware - Self-aware and adaptive agent *(TBC)*
- **Lesson 7**: Multi-Agent - Graph and Swarm collaboration patterns *(TBC)*

Each lesson includes:
- ✅ **Clear learning objectives**
- 🛠️ **Working code examples**
- 🧪 **Hands-on experiments**
- 📈 **Success criteria**
- 🐛 **Common pitfalls and solutions**

## 🗂️ Project Structure

```
strands-agents-learning/
├── README.md                        # Project overview and quick start
├── learning-plan.md                 # Complete learning plan with detailed explanations
├── pyproject.toml                   # Project dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore configuration
├── LICENSE                          # Apache 2.0 license
├── lesson_utils.py                  # Shared utilities for all lessons
├── lesson_01_hello_world.py         # Lesson 1: Python script ✅
├── lesson_01_hello_world.ipynb      # Lesson 1: Jupyter notebook ✅
├── lesson_02_first_tool.py          # Lesson 2: Python script ✅
├── lesson_02_first_tool.ipynb       # Lesson 2: Jupyter notebook ✅
└── experiments/                     # Your experimental code goes here
    └── .gitignore                   # Keeps experiments local
```

## 🎯 Agent Design Patterns You'll Master

### Single Agent Patterns (Lessons 1-6)
1. **Basic Conversational** - Request-response with system prompts
2. **Tool-Enhanced** - Extending capabilities with function calls
3. **Stateful** - Maintaining context and data across interactions
4. **Asynchronous** - Concurrent processing and streaming
5. **Context-Aware** - Self-introspection and adaptive behavior

### Multi-Agent Patterns (Lesson 7)
6. **Graph Pattern** - Structured workflows with conditional logic
7. **Swarm Pattern** - Autonomous collaboration between specialists

## 🔧 Environment Setup

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Add at least one API key to `.env`** - choose your preferred provider:

   **Option A: OpenAI (Recommended)**
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   - Get key: https://platform.openai.com/api-keys
   - Model: GPT-4o-mini (fast, cost-effective)

   **Option B: Anthropic Claude**
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```
   - Get key: https://console.anthropic.com/
   - Model: Claude 3.5 Haiku (optimized for Strands)

   **Option C: Ollama (Local, Free)**
   - Install: https://ollama.ai
   - Run: `ollama serve`
   - Pull model: `ollama pull llama3.1`

3. **Run lessons sequentially** - each builds on the previous!

> **🤖 Smart Provider Selection**: The lessons automatically detect and use the best available provider. You only need ONE API key!

## 💡 Learning Tips

- **Start Simple**: Begin with Lesson 1, don't skip ahead
- **Run the Code**: Execute every example to see it in action
- **Experiment**: Modify examples and see what happens
- **Use the Experiments Folder**: Try your own variations
- **Read the Learning Plan**: Check `learning-plan.md` for detailed explanations
- **Debug Thoughtfully**: When things break, understand why

## 🧪 How to Experiment

When each lesson suggests experiments to try, **DO NOT modify the lesson files directly**. Instead:

1. **Copy code to experiments folder**:
   ```bash
   # Example: Experimenting with Lesson 1
   cp lesson_01_hello_world.py experiments/my_personality_test.py
   ```

2. **Modify and run your experiment**:
   ```bash
   # Run from the project root directory
   uv run python experiments/my_personality_test.py
   ```

3. **Try the suggested experiments** from each lesson:
   - Create new system prompts and personalities
   - Modify model parameters (temperature, max_tokens)
   - Combine concepts from multiple lessons
   - Build your own custom tools and agents

The `experiments/` folder is your sandbox - break things, try wild ideas, and learn by doing! The original lesson files remain as clean references you can always return to.

## 🛠️ Troubleshooting

### Common Issues and Solutions

**❌ "No working model configuration found"**
```bash
# Copy the environment file and add at least one API key
cp .env.example .env
# Edit .env and add one of:
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here
```

**❌ "401 Unauthorized" or "403 Forbidden"**
- **OpenAI**: Check key at https://platform.openai.com/api-keys
- **Anthropic**: Check key at https://console.anthropic.com/
- Ensure sufficient credits in your account
- Verify your key is correctly set in `.env` file

**❌ Module import errors**
```bash
# Reinstall dependencies
uv sync
```

**❌ Lessons run slowly**
- OpenAI/Anthropic should be fast - check internet connection
- Local Ollama models are slower but free
- The lessons automatically choose the fastest available provider

**❌ Jupyter Notebook: "ModuleNotFoundError: No module named 'strands'"**
```bash
# Install the Jupyter kernel (one-time setup)
uv run python -m ipykernel install --user --name=strands-learning --display-name="Python (Strands)"

# Then restart Jupyter and the kernel will be available
# The notebook should automatically use "Python (Strands)" kernel
```

If still not working:
- In Jupyter: Click **Kernel** → **Change Kernel** → Select **"Python (Strands)"**
- Verify kernel is installed: `uv run jupyter kernelspec list`
- Should show `strands-learning` in the list

## 🤝 Contributing

We welcome contributions! Here's how you can help:

- 🐛 **Report Issues**: Found a bug or unclear explanation? [Open an issue](https://github.com/jztan/strands-agents-learning/issues)
- 💡 **Suggest Improvements**: Ideas for better examples or explanations
- 🔧 **Submit PRs**: Fix bugs, improve code, or add new examples
- 📚 **Improve Documentation**: Make explanations clearer
- ⭐ **Share**: Star the repo if it helped you learn!

### Development Setup
```bash
git clone https://github.com/jztan/strands-agents-learning.git
cd strands-agents-learning
uv sync --dev

# Setup git filter to auto-clean notebook outputs (recommended)
./setup_notebook_filter.sh
```

**Why clean notebook outputs?**
- Keeps repository lightweight
- Avoids huge git diffs from output changes
- Prevents accidental exposure of API responses
- Learners see fresh outputs when they run cells

## 📖 Additional Resources

- **[Strands Documentation](https://strandsagents.com/latest/documentation/)** - Official framework docs
- **[Strands GitHub](https://github.com/strandsagents/strands-agents)** - Source code and issues

## 🏆 What You'll Build

By completing all lessons, you'll have built a **sophisticated Personal AI Assistant** that can:

- Hold natural conversations
- Perform calculations and unit conversions
- Manage todos and notes with persistence
- Process files with real-time progress updates
- Adapt behavior based on conversation context
- Collaborate with other agents to solve complex problems

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Strands AI](https://strandsagents.com/)** - For creating an amazing agent framework
- **Contributors** - Everyone who helps improve this learning resource
- **Community** - Learners who provide feedback and share their experience

---

## 🎉 Get Started Now!

**Ready to learn Strands agents?**

1. Set up your API key in `.env` (OpenAI, Anthropic, or Ollama)
2. Run `uv run python lesson_01_hello_world.py`
3. Watch your first Strands agent come to life! 🚀

---

<div align="center">

**[⬆️ Back to Top](#learn-strands-agent-framework---hands-on-tutorial)**

Made with ❤️ for the AI agent development community

</div>