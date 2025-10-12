#!/usr/bin/env python3
"""
Strands Agent Learning - Shared Utilities
==========================================

This module provides common functionality used across all lessons to eliminate
code duplication and ensure consistency. All lessons import from this module
for model creation, environment setup, and error handling.

Functions:
- load_environment(): Handle dotenv loading gracefully
- create_working_model(): Multi-provider model creation with intelligent fallback
- check_api_keys(): Validate and report available API keys
- print_no_api_key_warning(): Standardized warning for missing keys
- print_troubleshooting(): Common troubleshooting guidance

Constants:
- Provider availability flags: OPENAI_AVAILABLE, ANTHROPIC_AVAILABLE, OLLAMA_AVAILABLE
- Configuration constants: DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE, etc.
"""

import os

# ============================================================================
# Environment Setup
# ============================================================================

def load_environment():
    """
    Load environment variables from .env file if available.
    Gracefully handles missing python-dotenv package.

    Returns:
        bool: True if dotenv was loaded, False if not available
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return True
    except ImportError:
        print("💡 Note: python-dotenv not available. Using environment variables directly.")
        print("   For best experience, run with: uv run python lesson_XX.py")
        return False

# ============================================================================
# Provider Detection and Imports
# ============================================================================

# Import model providers with graceful failure handling
try:
    from strands.models.openai import OpenAIModel
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from strands.models.anthropic import AnthropicModel
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from strands.models.ollama import OllamaModel
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    from strands.models.gemini import GeminiModel
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from strands.models.bedrock import BedrockModel
    import boto3
    BEDROCK_AVAILABLE = True
except ImportError:
    BEDROCK_AVAILABLE = False

# ============================================================================
# Configuration Constants
# ============================================================================

# Model configuration constants
DEFAULT_MAX_TOKENS = 500
DEFAULT_TEMPERATURE = 0.7

# Provider-specific model IDs
OPENAI_MODEL = "gpt-4o-mini"
ANTHROPIC_MODEL = "claude-3-5-haiku-20241022"
GEMINI_MODEL = "gemini-2.0-flash"
BEDROCK_MODEL = "amazon.nova-lite-v1:0"  # Amazon Nova Lite (cost-efficient)

# ============================================================================
# Multi-Provider Model Creation
# ============================================================================

def create_working_model(lesson_name=""):
    """
    Create a working model configuration with intelligent provider selection.

    Tries providers in order of preference:
    1. OpenAI (gpt-4o-mini) - Fast and cost-effective
    2. Anthropic (claude-3-5-haiku-20241022) - Good for Strands
    3. Google Gemini (gemini-2.0-flash) - Balanced performance
    4. AWS Bedrock (amazon.nova-lite-v1:0) - Enterprise, AWS integrated
    5. Ollama (local models) - Free but slower

    Args:
        lesson_name (str): Optional context for adjusting model configuration.
            - "demonstration"/"demo": Lower temp (0.5), fewer tokens (300) - predictable
            - "creative": Higher temp (0.9), more tokens (800) - varied responses
            - "precise"/"tool": Very low temp (0.3), standard tokens (500) - deterministic
            - Default: Standard settings (0.7 temp, 500 tokens)

    Returns:
        Model instance or None if no providers are available
    """
    lesson_context = f" for {lesson_name}" if lesson_name else ""

    # Determine configuration based on context
    context_lower = lesson_name.lower()
    if "demo" in context_lower or "demonstration" in context_lower:
        temperature = 0.5
        max_tokens = 300
        config_note = " (predictable mode)"
    elif "creative" in context_lower:
        temperature = 0.9
        max_tokens = 800
        config_note = " (creative mode)"
    elif "precise" in context_lower or "tool" in context_lower:
        temperature = 0.3
        max_tokens = 500
        config_note = " (precise mode)"
    else:
        temperature = DEFAULT_TEMPERATURE
        max_tokens = DEFAULT_MAX_TOKENS
        config_note = ""

    # Try OpenAI first (preferred for speed/cost)
    if OPENAI_AVAILABLE:
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            print(f"🚀 Using OpenAI {OPENAI_MODEL}{lesson_context}{config_note}")
            return OpenAIModel(
                client_args={"api_key": openai_key},
                model_id=OPENAI_MODEL,
                params={
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )

    # Try Anthropic second
    if ANTHROPIC_AVAILABLE:
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            print(f"🔮 Using Anthropic {ANTHROPIC_MODEL}{lesson_context}{config_note}")
            return AnthropicModel(
                client_args={"api_key": anthropic_key},
                max_tokens=max_tokens,
                model_id=ANTHROPIC_MODEL,
                params={"temperature": temperature}
            )

    # Try Gemini third
    if GEMINI_AVAILABLE:
        gemini_key = os.getenv("GOOGLE_API_KEY")
        if gemini_key:
            print(f"🔷 Using Google Gemini {GEMINI_MODEL}{lesson_context}{config_note}")
            return GeminiModel(
                client_args={"api_key": gemini_key},
                model_id=GEMINI_MODEL,
                params={
                    "max_output_tokens": max_tokens,
                    "temperature": temperature
                }
            )

    # Try Bedrock fourth (AWS integrated)
    if BEDROCK_AVAILABLE:
        bedrock_model = _try_bedrock_connection(lesson_context, config_note, max_tokens, temperature)
        if bedrock_model:
            return bedrock_model

    # Try Ollama fifth (local option)
    if OLLAMA_AVAILABLE:
        ollama_model = _try_ollama_connection(lesson_context, config_note)
        if ollama_model:
            return ollama_model

    # No working configuration found
    print_no_working_model_error()
    return None

def _try_bedrock_connection(lesson_context="", config_note="", max_tokens=500, temperature=0.7):
    """
    Attempt to connect to AWS Bedrock and return a working model.

    Checks for AWS credentials using boto3's standard credential chain.

    Returns:
        BedrockModel instance or None if not available
    """
    try:
        # Check if AWS credentials are configured
        session = boto3.Session()
        credentials = session.get_credentials()

        if credentials is None:
            return None

        # Get current credentials to verify they're valid
        current_creds = credentials.get_frozen_credentials()
        if not current_creds.access_key:
            return None

        # Credentials found, create Bedrock model
        print(f"☁️ Using AWS Bedrock {BEDROCK_MODEL}{lesson_context}{config_note}")
        return BedrockModel(
            model_id=BEDROCK_MODEL,
            max_tokens=max_tokens,
            temperature=temperature
        )
    except Exception:
        # AWS credentials not configured or other error
        return None

def _try_ollama_connection(lesson_context="", config_note=""):
    """
    Attempt to connect to local Ollama server and return a working model.

    Returns:
        OllamaModel instance or None if not available
    """
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                model_name = models[0]["name"]  # Use first available model
                print(f"🏠 Using Ollama local model: {model_name}{lesson_context}{config_note}")
                return OllamaModel(
                    host="http://localhost:11434",
                    model_id=model_name
                )
    except Exception:
        pass  # Ollama not available
    return None

# ============================================================================
# API Key Validation
# ============================================================================

def check_api_keys():
    """
    Check for available API keys and provide user guidance.

    Returns:
        bool: True if at least one API key is available, False otherwise
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    gemini_key = os.getenv("GOOGLE_API_KEY")

    if not openai_key and not anthropic_key and not gemini_key:
        print_no_api_key_warning()
        return False

    # Check for placeholder values
    available_providers = []
    if openai_key and len(openai_key) > 10 and not openai_key.startswith("your_"):
        available_providers.append("OpenAI")
    if anthropic_key and len(anthropic_key) > 10 and not anthropic_key.startswith("your_"):
        available_providers.append("Anthropic")
    if gemini_key and len(gemini_key) > 10 and not gemini_key.startswith("your_"):
        available_providers.append("Google Gemini")

    if available_providers:
        print(f"✅ API keys detected: {', '.join(available_providers)}")
        return True
    else:
        print("⚠️ API keys appear to be placeholders/invalid")
        print("   Please add real API keys for full functionality")
        return False

# ============================================================================
# Error Messages and User Guidance
# ============================================================================

def print_no_api_key_warning():
    """Print standardized warning for missing API keys."""
    print("⚠️ No API keys found in environment variables.")
    print("   To get full functionality, set up at least one:")
    print("   1. Copy .env.example to .env")
    print("   2. Add one of these API keys:")
    print("      • OPENAI_API_KEY (get from: https://platform.openai.com/api-keys)")
    print("      • ANTHROPIC_API_KEY (get from: https://console.anthropic.com/)")
    print("      • GOOGLE_API_KEY (get from: https://aistudio.google.com/app/apikey)")
    print("      • AWS Credentials (configure: aws configure)")
    print("   3. Or run Ollama locally for free (slower)")
    print("      • Install: https://ollama.ai")
    print("      • Run: ollama serve")
    print("      • Pull model: ollama pull llama3.1")

def print_no_working_model_error():
    """Print error message when no model providers are available."""
    print("⚠️ No working model configuration found")
    print("   Please set up at least one:")
    print("   • OPENAI_API_KEY (recommended - fast & cost-effective)")
    print("   • ANTHROPIC_API_KEY (alternative - Strands optimized)")
    print("   • GOOGLE_API_KEY (alternative - balanced performance)")
    print("   • Or run Ollama locally (free but slower)")

def print_troubleshooting():
    """Print comprehensive troubleshooting guidance."""
    print("\nTroubleshooting:")
    print("1. Make sure your .env file has at least one API key:")
    print("   • OPENAI_API_KEY (recommended)")
    print("   • ANTHROPIC_API_KEY (alternative)")
    print("   • GOOGLE_API_KEY (alternative)")
    print("2. Run `uv sync` to install dependencies")
    print("3. Verify API keys are valid:")
    print("   • OpenAI: https://platform.openai.com/api-keys")
    print("   • Anthropic: https://console.anthropic.com/")
    print("   • Google Gemini: https://aistudio.google.com/app/apikey")
    print("4. Check account credits/usage limits")
    print("5. For Ollama: ensure server is running (`ollama serve`)")

# ============================================================================
# Convenience Functions
# ============================================================================

def setup_lesson_environment(lesson_name=""):
    """
    Complete lesson environment setup in one function call.

    Args:
        lesson_name (str): Name of the lesson for context

    Returns:
        tuple: (model, dotenv_available) or (None, dotenv_available) if setup fails
    """
    # Load environment
    dotenv_available = load_environment()

    # Check API keys
    if not check_api_keys():
        return None, dotenv_available

    # Create model
    model = create_working_model(lesson_name)
    return model, dotenv_available

# ============================================================================
# Module Information
# ============================================================================

__version__ = "1.0.0"
__author__ = "Strands Agent Learning Project"
__description__ = "Shared utilities for Strands agent lessons"

# Export commonly used items for convenience
__all__ = [
    "load_environment",
    "create_working_model",
    "check_api_keys",
    "print_no_api_key_warning",
    "print_troubleshooting",
    "setup_lesson_environment",
    "OPENAI_AVAILABLE",
    "ANTHROPIC_AVAILABLE",
    "GEMINI_AVAILABLE",
    "BEDROCK_AVAILABLE",
    "OLLAMA_AVAILABLE",
    "DEFAULT_MAX_TOKENS",
    "DEFAULT_TEMPERATURE"
]
