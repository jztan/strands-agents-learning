# Contributing to Strands Agents Learning

Thank you for your interest in contributing to this project! We welcome contributions from everyone who wants to help make learning the Strands Agent Framework easier and more effective.

## 🤝 How You Can Help

### Report Issues
Found a bug, unclear explanation, or have a suggestion? [Open an issue](https://github.com/jztan/strands-agents-learning/issues) with:
- Clear description of the problem or suggestion
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)

### Suggest Improvements
Have ideas for better examples or explanations?
- Open an issue with the `enhancement` label
- Describe what could be improved and why
- Provide specific examples if possible

### Submit Pull Requests
Want to fix bugs, improve code, or add new examples?
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Make your changes following our [coding standards](#coding-standards)
4. Test your changes thoroughly
5. Submit a pull request with a clear description

### Improve Documentation
Help make explanations clearer:
- Fix typos and grammar
- Add missing explanations
- Improve code comments
- Enhance README sections

### Share and Star
- ⭐ Star the repo if it helped you learn!
- Share with others learning Strands
- Write blog posts or create videos

## 🗂️ Repository Overview

Each lesson comes in two formats:
- **`.py` files** - Complete Python scripts for reference and direct execution
- **`.ipynb` files** - Interactive Jupyter notebooks for hands-on learning

Key files:
- `lesson_utils.py` - Shared utilities (model creation, environment setup, error handling)
- `.env.example` - Template for API key configuration
- `experiments/` - Your sandbox for trying variations (gitignored)
- `pyproject.toml` - Project dependencies managed with `uv`

The repository uses a simple trunk-based development model on the `main` branch with sequential commits, one per lesson.

## 📁 Project Structure

Understanding the repository layout helps you navigate and contribute effectively:

```
strands-agents-learning/
├── README.md                           # Project overview and quick start (for learners)
├── CONTRIBUTING.md                     # This file - contribution guidelines (for contributors)
├── TROUBLESHOOTING.md                  # Common issues and solutions
├── CLAUDE.md                           # Instructions for Claude Code AI assistant (not committed)
├── learning-plan.md                    # Detailed curriculum and implementation plan (not committed)
├── pyproject.toml                      # Project dependencies and metadata
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore configuration
├── LICENSE                             # Apache 2.0 license
├── setup_notebook_filter.sh            # Git filter for cleaning notebook outputs
│
├── lesson_utils.py                     # Shared utilities for all lessons
│   # - Multi-provider model creation (OpenAI, Anthropic, Gemini, Ollama)
│   # - Environment setup and API key validation
│   # - Standardized error handling
│   # - All lessons import from this module (DRY principle)
│
├── lesson_01_hello_world.py            # Lesson 1: Python script ✅
├── lesson_01_hello_world.ipynb         # Lesson 1: Jupyter notebook ✅
├── lesson_02_first_tool.py             # Lesson 2: Python script ✅
├── lesson_02_first_tool.ipynb          # Lesson 2: Jupyter notebook ✅
├── lesson_03_multiple_tools.py         # Lesson 3: Python script ✅
├── lesson_03_multiple_tools.ipynb      # Lesson 3: Jupyter notebook ✅
├── lesson_04_agent_state.py            # Lesson 4: Python script ✅
├── lesson_04_agent_state.ipynb         # Lesson 4: Jupyter notebook ✅
├── lesson_05_async_executors_mcp.py    # Lesson 5: Python script ✅
├── lesson_05_async_executors_mcp.ipynb # Lesson 5: Jupyter notebook ✅
├── lesson_06_hooks_structured.py       # Lesson 6: Python script 🚧
├── lesson_06_hooks_structured.ipynb    # Lesson 6: Jupyter notebook 🚧
├── lesson_07_advanced_tools.py         # Lesson 7: Python script 🚧
├── lesson_07_advanced_tools.ipynb      # Lesson 7: Jupyter notebook 🚧
├── lesson_08_multi_agent.py            # Lesson 8: Python script 🚧
├── lesson_08_multi_agent.ipynb         # Lesson 8: Jupyter notebook 🚧
├── lesson_09_distributed_agents.py     # Lesson 9: Python script 🚧
├── lesson_09_distributed_agents.ipynb  # Lesson 9: Jupyter notebook 🚧
├── lesson_10_production.py             # Lesson 10: Python script 🚧
├── lesson_10_production.ipynb          # Lesson 10: Jupyter notebook 🚧
│
└── experiments/                        # User sandbox for variations (gitignored)
    └── .gitignore                      # Ensures experiments stay local
```

### File Organization Principles

- **Lesson Files**: Each lesson has both `.py` (script) and `.ipynb` (notebook) versions
- **lesson_utils.py**: Shared infrastructure - never duplicate code across lessons
- **experiments/**: User workspace for trying variations - completely gitignored
- **Documentation**: README for learners, CONTRIBUTING for developers

## 🔧 Development Setup

### Prerequisites
- Python 3.10+
- `uv` package manager ([install guide](https://docs.astral.sh/uv/))
- Git

### Setting Up Your Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/strands-agents-learning.git
   cd strands-agents-learning
   ```

2. **Install Dependencies**
   ```bash
   # Core dependencies
   uv sync

   # Development dependencies (includes Jupyter)
   uv sync --dev
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Add at least one API key to .env
   ```

4. **Test Your Setup**
   ```bash
   uv run python lesson_01_hello_world.py
   ```

## 📝 Coding Standards

### Code Style
- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and concise

### Lesson File Standards

When creating or modifying lesson files, follow these conventions:

#### File Structure
```python
#!/usr/bin/env python3
"""
Lesson X: Title
- Bullet points of concepts covered
- Learning goals as checkboxes
"""

from lesson_utils import (
    load_environment,
    create_working_model,
    check_api_keys
)

# Part 1, 2, 3... functions demonstrating concepts

def main():
    """Run all examples."""
    load_environment()
    check_api_keys()
    # ... run parts
    # ... print success criteria and experiments

if __name__ == "__main__":
    main()
```

#### Experiments Section (Python Files Only)
Use consistent formatting:
```python
print("\n🧪 Experiments to Try:")
print("   ")
print("   Setup: Copy this lesson to experiments/ before tinkering:")
print("      cp lesson_XX_name.py experiments/my_variant_name.py")
print("      uv run python experiments/my_variant_name.py")
print("   ")
print("   Exercises:")
print("   1. First experiment description")
print("   2. Second experiment description")
```

### Documentation Standards
- Use clear, beginner-friendly language
- Provide code examples for concepts
- Include expected output where helpful
- Add comments explaining Strands-specific patterns
- Reference official documentation when relevant

### DRY Principle
- Use `lesson_utils.py` for common functionality
- Never duplicate infrastructure code across lessons
- Extract reusable patterns into utilities

## 🧪 Testing Guidelines

### Manual Testing
Before submitting a PR:
1. Run all modified lesson files end-to-end
2. Test with at least one AI provider (OpenAI, Anthropic, or Gemini)
3. Verify examples work as documented
4. Check that error messages are helpful

### Provider Testing
Test lessons with different providers to ensure provider-agnostic design:
```bash
# Test with OpenAI
ANTHROPIC_API_KEY="" GOOGLE_API_KEY="" uv run python lesson_XX.py

# Test with Anthropic
OPENAI_API_KEY="" GOOGLE_API_KEY="" uv run python lesson_XX.py

# Test with Gemini
OPENAI_API_KEY="" ANTHROPIC_API_KEY="" uv run python lesson_XX.py
```

## 📓 Jupyter Notebook Contributions

### Important: Clean Outputs Before Committing

Notebooks should **never** be committed with execution outputs to:
- Prevent accidental exposure of API keys/responses
- Keep repository lightweight
- Avoid merge conflicts

### Setup Notebook Filter (One-Time)
```bash
./setup_notebook_filter.sh
```

This configures Git to automatically strip outputs when committing.

### Manual Cleanup (If Needed)
```bash
jupyter nbconvert --clear-output --inplace lesson_XX.ipynb
```

### Notebook Standards
- Use markdown cells for section headers
- Keep code cells focused (one concept per cell)
- Add explanatory markdown between code cells
- Test notebook by running "Restart & Run All"

## 🌳 Git Workflow

### Branch Naming
- `feature/description` - New features or lessons
- `fix/description` - Bug fixes
- `docs/description` - Documentation improvements
- `refactor/description` - Code refactoring

### Commit Messages
- Use clear, imperative messages
- Format: `Action: Description`
- Examples:
  - `Add: Lesson 6 hooks and structured output`
  - `Fix: Model configuration in lesson_utils`
  - `Docs: Improve quick start instructions`
  - `Refactor: Extract common error handling`

**Important:** Do NOT include AI attribution in commits:
- ❌ "Generated with Claude Code"
- ❌ "Co-Authored-By: Claude"
- ✅ Focus on what changed and why

### Commit Guidelines
- Keep commits atomic (one logical change per commit)
- Ensure each commit is runnable
- Write descriptive commit messages
- Reference issues when applicable (`Fixes #123`)

## 🔍 Code Review Process

### What We Look For
- Code follows style guidelines
- Changes are well-tested
- Documentation is clear and accurate
- No breaking changes to existing lessons
- Maintains provider-agnostic design

### Review Timeline
- We aim to review PRs within 7 days
- Complex changes may take longer
- Be patient and responsive to feedback

## 🚫 What NOT to Commit

### Security
- Never commit real API keys
- Never commit `.env` files
- Never commit credentials of any kind

### Outputs
- No Jupyter notebook outputs
- No API response logs
- No cached model responses

### Personal Files
- No personal experiments (use `experiments/` - it's gitignored)
- No IDE-specific files (already in `.gitignore`)
- No temporary or backup files

## 📚 Resources for Contributors

### Strands Agent Framework
- [Official Documentation](https://strandsagents.com/latest/documentation/)
- [GitHub Repository](https://github.com/strandsagents/strands-agents)
- [API Reference](https://strandsagents.com/latest/documentation/api-reference/)

### Learning Materials
- Study existing lessons for patterns
- Check `learning-plan.md` for implementation standards
- Review `CLAUDE.md` for project conventions

## ❓ Questions?

- Open a [discussion](https://github.com/jztan/strands-agents-learning/discussions) for general questions
- Tag issues with `question` label
- Reach out to maintainers for guidance

---

Thank you for contributing to Strands Agents Learning! Your efforts help others learn and build with the Strands Agent Framework.
