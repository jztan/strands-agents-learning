# Troubleshooting Guide

## Common Issues and Solutions

### ❌ "No working model configuration found"
```bash
# Copy the environment file and add at least one API key
cp .env.example .env
# Edit .env and add one of:
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here
```

### ❌ "401 Unauthorized" or "403 Forbidden"
- **OpenAI**: Check key at https://platform.openai.com/api-keys
- **Anthropic**: Check key at https://console.anthropic.com/
- Ensure sufficient credits in your account
- Verify your key is correctly set in `.env` file

### ❌ Module import errors
```bash
# Reinstall dependencies
uv sync
```

### ❌ Lessons run slowly
- OpenAI/Anthropic should be fast - check internet connection
- Local Ollama models are slower but free
- The lessons automatically choose the fastest available provider

### ❌ Jupyter Notebook: "ModuleNotFoundError: No module named 'strands'"
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
