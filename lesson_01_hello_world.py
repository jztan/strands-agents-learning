#!/usr/bin/env python3
"""
Lesson 1: Hello World Agent - The Foundation of Strands
IMPLEMENTATION: Following Quality Standards with Verified Patterns

This lesson covers the most basic agent concepts:
- Basic agent initialization with Agent() class
- System prompts and their influence on behavior
- Simple conversation flow and context maintenance
- Agent invocation (sync and async patterns)
- Model configuration with different providers

Learning Goals:
✅ Agent responds to basic questions
✅ System prompt influences behavior (personality changes work)
✅ Can maintain conversation context across multiple turns
✅ Both sync and async invocations work correctly

Estimated time: 2 hours

TECHNICAL NOTES:
- Uses verified import patterns: from strands import Agent
- Multi-provider model configuration through lesson_utils
- Automatic provider selection (OpenAI, Anthropic, or Ollama)
- Includes graceful handling for missing dependencies and API keys
"""

import asyncio

# Import shared utilities for consistent setup across all lessons
from lesson_utils import (
    load_environment,
    create_working_model,
    check_api_keys,
    print_troubleshooting
)

# Import the core Strands components
from strands import Agent

print("🎯 Lesson 1: Hello World Agent")
print("=" * 50)

# ============================================================================
# Note: Model creation is now handled by lesson_utils.create_working_model()
# This eliminates code duplication across all lessons.
# ============================================================================

# ============================================================================
# Part 1: Basic Agent Creation
# ============================================================================

def basic_agent_example():
    """
    The simplest possible agent - using a working model configuration.
    Shows both default Agent() pattern and working model configuration.
    """
    print("\n📍 Part 1: Basic Agent Creation")
    print("-" * 30)

    # First, show the default pattern (may not work due to model access)
    print("📝 Default Agent() pattern:")
    Agent()  # Create but don't store unused variable
    print("✅ Default Agent() created - but may not work due to model access")

    # Now create an agent with working model configuration
    print("\n📝 Agent with working model configuration:")
    working_model = create_working_model()
    if working_model:
        agent = Agent(model=working_model)
        print("✅ Agent with working model created successfully")

        try:
            # Use the agent synchronously - this is the simplest way
            response = agent("Hello! What's your name?")
            print(f"🤖 Agent: {response}")

            # You can continue the conversation - the agent remembers context
            response = agent("What can you help me with?")
            print(f"🤖 Agent: {response}")

        except Exception as e:
            print(f"⚠️ Agent call failed: {e}")
            print("   This suggests an API key or model access issue")
    else:
        print("⚠️ No API key detected. Skipping agent invocation.")
        print("   Add API keys to your environment to test agent responses")
        print("\n💡 Key Learning: Default Agent() may use inaccessible models.")
        print("   Explicit model configuration ensures predictable behavior.")

# ============================================================================
# Part 2: System Prompts - Changing Agent Personality
# ============================================================================

def system_prompt_examples():
    """
    System prompts control how the agent behaves and responds.
    Let's see how different prompts create different personalities.
    """
    print("\n📍 Part 2: System Prompts - Agent Personalities")
    print("-" * 45)

    # Get working model configuration for all personality agents
    working_model = create_working_model()
    if not working_model:
        print("⚠️ No API key available. Skipping personality demonstrations.")
        return

    # 1. Helpful Assistant (default-style)
    helpful_agent = Agent(
        model=working_model,
        system_prompt="You are a helpful, friendly assistant. Be concise but warm in your responses."
    )

    # 2. Pirate Personality
    pirate_agent = Agent(
        model=working_model,
        system_prompt="You are a friendly pirate who speaks in pirate dialect. Use 'arr', 'matey', and nautical terms. Be helpful but maintain your pirate character."
    )

    # 3. Scientific Researcher
    scientist_agent = Agent(
        model=working_model,
        system_prompt="You are a meticulous scientific researcher. Provide evidence-based answers, cite your reasoning, and acknowledge uncertainties. Be precise and methodical."
    )

    print("✅ Created agents with different personalities")
    print("   - Helpful Assistant")
    print("   - Pirate Character")
    print("   - Scientific Researcher")

    # Test the same question with different personalities (if working model available)
    if working_model:
        question = "What's the best way to learn programming?"
        print(f"\n🤔 Question: {question}\n")

        try:
            print("🤖 Helpful Assistant:")
            response = helpful_agent(question)
            print(f"   {response}\n")

            print("🏴‍☠️ Pirate Assistant:")
            response = pirate_agent(question)
            print(f"   {response}\n")

            print("🔬 Scientific Researcher:")
            response = scientist_agent(question)
            print(f"   {response}\n")

        except Exception as e:
            print(f"⚠️ Personality test failed: {e}")
            print("   Agents created successfully, but couldn't test due to API issues")
    else:
        print("⚠️ Skipping personality test - no API key available")

# ============================================================================
# Part 3: Model Configuration (Following Official Documentation)
# ============================================================================

def model_configuration_example():
    """
    This example demonstrates model configuration using the shared utilities.
    The actual model selection is handled by lesson_utils.create_working_model()
    which uses intelligent provider fallback.
    """
    print("\n📍 Part 3: Model Configuration")
    print("-" * 35)

    # Check if any API keys are available
    if not check_api_keys():
        print("⚠️ No API keys configured. Showing how model configuration works.")
        print("   The lesson_utils.create_working_model() function handles:")
        print("   • OpenAI (gpt-4o-mini) - First choice")
        print("   • Anthropic (claude-3-5-haiku) - Second choice")
        print("   • Ollama (local models) - Third choice")
        return

    try:
        # Use shared utilities for consistent model creation
        model = create_working_model("Part 3 demonstration")
        if not model:
            print("❌ No working model configuration found")
            return

        print("✅ Model configured successfully using shared utilities")
        print("   • Provider selection handled automatically")
        print("   • Configuration consistent across all lessons")
        print("   • Fallback logic for reliability")

        # Create agent with the configured model
        agent = Agent(
            model=model,
            system_prompt="You are a concise, helpful assistant. Keep responses under 2 sentences."
        )

        print("✅ Agent with configured model created")

        # Test the configured agent
        try:
            response = agent("Explain machine learning in simple terms")
            print(f"🤖 Agent response: {response}")
        except Exception as e:
            print(f"⚠️ Model test failed: {e}")

    except Exception as e:
        print(f"❌ Model configuration failed: {e}")

# ============================================================================
# Part 4: Async Operations
# ============================================================================

async def async_agent_example():
    """
    For production applications, you'll often want async operations.
    This is essential when building web services or handling multiple conversations.
    """
    print("\n📍 Part 4: Async Agent Operations")
    print("-" * 37)

    # Create an agent with working model configuration
    working_model = create_working_model()
    if not working_model:
        print("⚠️ Skipping async tests - no API key available")
        return

    agent = Agent(
        model=working_model,
        system_prompt="You are a helpful assistant who loves to help with coding questions."
    )

    try:
        # Use invoke_async() for asynchronous operations
        print("Asking question asynchronously...")
        response = await agent.invoke_async("What's the difference between lists and tuples in Python?")
        print(f"🤖 Async response: {response}")

        # You can run multiple async operations concurrently
        print("\nRunning multiple questions concurrently...")

        questions = [
            "What is Python?",
            "What is JavaScript?",
            "What is Rust?"
        ]

        # Create multiple concurrent requests
        tasks = [agent.invoke_async(question) for question in questions]

        # Wait for all responses
        responses = await asyncio.gather(*tasks)

        for question, response in zip(questions, responses):
            print(f"❓ Q: {question}")
            print(f"🤖 A: {response}\n")

    except Exception as e:
        print(f"⚠️ Async test failed: {e}")

# ============================================================================
# Part 5: Streaming Responses (Real-time)
# ============================================================================

async def streaming_example():
    """
    For better user experience, you can stream responses as they're generated.
    This shows text appearing in real-time, like ChatGPT's interface.
    """
    print("\n📍 Part 5: Streaming Responses")
    print("-" * 32)

    working_model = create_working_model()
    if not working_model:
        print("⚠️ Skipping streaming test - no API key available")
        return

    agent = Agent(
        model=working_model,
        system_prompt="You are a storyteller. Tell engaging, creative stories."
    )

    try:
        print("Streaming a story (watch it appear in real-time):")
        print("Story: ", end="", flush=True)

        # Use stream_async() to get real-time responses
        async for event in agent.stream_async("Tell me a short story about a robot learning to paint"):
            # Each event contains a piece of the response
            if hasattr(event, 'content'):
                print(event.content, end="", flush=True)

        print("\n")

    except Exception as e:
        print(f"⚠️ Streaming test failed: {e}")

# ============================================================================
# Part 6: Multi-turn Conversations
# ============================================================================

def multi_turn_conversation():
    """
    Agents automatically maintain conversation context.
    This enables natural back-and-forth conversations.
    """
    print("\n📍 Part 6: Multi-turn Conversations")
    print("-" * 38)

    working_model = create_working_model()
    if not working_model:
        print("⚠️ Skipping conversation test - no API key available")
        print("✅ Agent would be created successfully for multi-turn conversations")
        return

    agent = Agent(
        model=working_model,
        system_prompt="You are a helpful programming tutor. Remember what we discuss and build on it."
    )

    # Simulate a conversation about learning Python
    conversation = [
        "I'm new to programming. Should I start with Python?",
        "What's the first Python concept I should learn?",
        "Can you give me a simple example of that concept?",
        "What should I learn after variables?"
    ]

    try:
        for i, message in enumerate(conversation, 1):
            print(f"\n👤 Turn {i}: {message}")
            response = agent(message)
            print(f"🤖 Agent: {response}")

    except Exception as e:
        print(f"⚠️ Conversation test failed: {e}")

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """
    Run all examples to demonstrate core agent concepts.
    Each example builds on the previous ones.
    """
    print("Welcome to Strands Agent Framework!")
    print("This lesson covers the foundation concepts.\n")

    # Load environment and check setup using shared utilities
    dotenv_available = load_environment()

    # Check API keys and provide guidance
    if not check_api_keys():
        print("   Continuing with limited functionality...\n")

    # Note about environment setup
    if not dotenv_available:
        print("💡 For better experience: pip install python-dotenv")
        print("   Or run with: uv run python lesson_01_hello_world.py\n")

    try:
        # Run synchronous examples
        basic_agent_example()
        system_prompt_examples()
        model_configuration_example()
        multi_turn_conversation()

        # Run asynchronous examples
        print("\n🔄 Running async examples...")
        asyncio.run(async_agent_example())
        asyncio.run(streaming_example())

        print("\n" + "=" * 50)
        print("🎉 Lesson 1 Complete!")
        print("=" * 50)
        print("\n✅ Success Criteria Checklist:")
        print("   □ Agent responds to basic questions")
        print("   □ System prompt influences behavior (try different personalities)")
        print("   □ Can maintain conversation context across turns")
        print("   □ Both sync and async invocations work")
        print("\n🧪 Experiments to Try:")
        print("   ")
        print("   Setup: Copy this lesson to experiments/ before tinkering:")
        print("      cp lesson_01_hello_world.py experiments/my_personality_test.py")
        print("      uv run python experiments/my_personality_test.py")
        print("   ")
        print("   Exercises:")
        print("   1. Change system prompts to create different personalities")
        print("   2. Test multi-turn conversations with follow-up questions")
        print("   3. Try different model parameters (temperature, max_tokens)")
        print("   4. Test how the agent handles ambiguous requests")
        print("   5. Experiment with different providers and models:")
        print("      - Try with OPENAI_API_KEY (fast, cost-effective)")
        print("      - Try with ANTHROPIC_API_KEY (alternative provider)")
        print("      - Test with Ollama local models (free but slower)")
        print("      - Compare response styles between providers")
        print("\n➡️ Next: Run `uv run python lesson_02_first_tool.py`")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print_troubleshooting()

if __name__ == "__main__":
    main()
