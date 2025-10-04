#!/usr/bin/env python3
"""
Lesson 2: First Tool - Extending Agent Capabilities
IMPLEMENTATION: Following Quality Standards with Verified Patterns

This lesson introduces tools - the foundation of agent capabilities:
- The @tool decorator for function-based tools
- Tool specifications and JSON schemas
- Tool invocation logic by the agent
- Tool result handling and formatting
- Error handling in tools (try/except patterns)
- Tool descriptions for proper selection

Learning Goals:
✅ Tool is correctly invoked for math questions
✅ Agent explains its calculations clearly
✅ Handles errors gracefully (division by zero, invalid input)
✅ Agent knows when NOT to use the calculator (non-math queries)
✅ Tool results are properly formatted in responses

Estimated time: 2 hours

TECHNICAL NOTES:
- Uses verified import patterns: from strands import Agent, tool
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

# Import Strands components
from strands import Agent, tool

print("🎯 Lesson 2: First Tool - Calculator")
print("=" * 40)

# ============================================================================
# Note: Model creation is now handled by lesson_utils.create_working_model()
# This eliminates code duplication across all lessons.
# ============================================================================

# ============================================================================
# Part 1: Creating Your First Tool
# ============================================================================

@tool
def calculator(expression: str) -> str:
    """
    Evaluate mathematical expressions safely.

    This tool can handle basic arithmetic operations including:
    - Addition (+), Subtraction (-), Multiplication (*), Division (/)
    - Exponentiation (**)
    - Parentheses for grouping

    Args:
        expression: A mathematical expression as a string (e.g., "2 + 3 * 4")

    Returns:
        str: The result of the calculation or an error message

    Examples:
        calculator("2 + 3") → "5"
        calculator("10 / 2") → "5.0"
        calculator("2 ** 3") → "8"
    """
    try:
        # Use eval() safely with restricted globals for basic math operations
        # In production, consider using a proper math expression parser
        import math
        import builtins

        # Get safe built-in functions
        safe_builtins = ['abs', 'round', 'min', 'max', 'pow']
        allowed_names = {}
        for name in safe_builtins:
            if hasattr(builtins, name):
                allowed_names[name] = getattr(builtins, name)

        # Add math constants and functions
        allowed_names.update({
            'pi': math.pi,
            'e': math.e,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
        })

        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": {}}, allowed_names)

        # Format the result nicely
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)

    except ZeroDivisionError:
        return "Error: Division by zero is not allowed"
    except SyntaxError:
        return f"Error: Invalid mathematical expression '{expression}'"
    except NameError as e:
        return f"Error: Unknown function or variable in '{expression}'"
    except Exception as e:
        return f"Error: Could not evaluate '{expression}' - {str(e)}"

# ============================================================================
# Part 2: Agent with Calculator Tool
# ============================================================================

def basic_calculator_agent():
    """
    Create an agent with the calculator tool and test basic functionality.
    """
    print("\n📍 Part 2: Agent with Calculator Tool")
    print("-" * 35)

    # Get working model configuration
    working_model = create_working_model()
    if not working_model:
        print("⚠️ No working model configuration found. Skipping calculator demonstrations.")
        print("   This function requires a working model from lesson_utils.create_working_model()")
        return

    # Create an agent with the calculator tool and working model
    agent = Agent(
        model=working_model,
        tools=[calculator],  # Register our calculator tool
        system_prompt="""You are a helpful assistant with calculator capabilities.
        When someone asks a math question, use the calculator tool to get accurate results.
        Always explain your calculations clearly."""
    )

    # Test basic calculations
    test_questions = [
        "What is 15 + 27?",
        "Calculate 144 divided by 12",
        "What's 2 to the power of 8?",
        "Can you compute (25 + 15) * 2?"
    ]

    for question in test_questions:
        print(f"\n👤 Question: {question}")
        response = agent(question)
        print(f"🤖 Agent: {response}")

# ============================================================================
# Part 3: Error Handling and Edge Cases
# ============================================================================

def test_error_handling():
    """
    Test how the agent handles various error cases and edge scenarios.
    """
    print("\n📍 Part 3: Error Handling and Edge Cases")
    print("-" * 42)

    working_model = create_working_model()
    if not working_model:
        print("⚠️ No API key available. Skipping error handling tests.")
        return

    agent = Agent(
        model=working_model,
        tools=[calculator],
        system_prompt="""You are a helpful assistant with a calculator tool.
        ALWAYS use the calculator tool for ANY mathematical expression or calculation request,
        even if you think it might have errors. The tool will handle errors and return
        appropriate error messages. After getting the tool's result, explain it to the user."""
    )

    # Test error cases
    error_test_cases = [
        "What is 10 divided by 0?",  # Division by zero
        "Calculate 2 +",  # Invalid syntax
        "Calculate unknown_variable",  # Unknown variable
        "Calculate hello + world",  # Invalid expression
    ]

    for test_case in error_test_cases:
        print(f"\n👤 Question: {test_case}")
        response = agent(test_case)
        print(f"🤖 Agent: {response}")

# ============================================================================
# Part 4: Tool Selection Logic
# ============================================================================

def test_tool_selection():
    """
    Test when the agent chooses to use or not use the calculator tool.
    The agent should be smart about when calculation is actually needed.
    """
    print("\n📍 Part 4: Tool Selection Logic")
    print("-" * 35)

    working_model = create_working_model()
    if not working_model:
        print("⚠️ No API key available. Skipping tool selection tests.")
        return

    agent = Agent(
        model=working_model,
        tools=[calculator],
        system_prompt="""You are a helpful assistant. Use the calculator tool when
        mathematical calculations are needed, but answer other questions normally
        without using tools."""
    )

    # Mix of math and non-math questions
    mixed_questions = [
        "What is 25 * 4?",  # Should use calculator
        "What is your name?",  # Should NOT use calculator
        "Tell me about Python programming",  # Should NOT use calculator
        "What's the square root of 144?",  # Should use calculator
        "What's the capital of France?",  # Should NOT use calculator
        "Calculate the area of a circle with radius 5 (use π ≈ 3.14159)",  # Should use calculator
    ]

    for question in mixed_questions:
        print(f"\n👤 Question: {question}")
        response = agent(question)
        print(f"🤖 Agent: {response}")
        # Note: In real usage, you might want to check if the tool was actually called

# ============================================================================
# Part 5: Complex Mathematical Expressions
# ============================================================================

def test_complex_calculations():
    """
    Test the calculator with more complex mathematical expressions.
    """
    print("\n📍 Part 5: Complex Mathematical Expressions")
    print("-" * 45)

    working_model = create_working_model()
    if not working_model:
        print("⚠️ No API key available. Skipping complex calculation tests.")
        return

    agent = Agent(
        model=working_model,
        tools=[calculator],
        system_prompt="""You are a mathematical assistant. Break down complex
        calculations step by step when helpful, and always verify your results."""
    )

    complex_questions = [
        "What is (15 + 25) * (30 - 10) / 4?",
        "Calculate 2**10 - 500",
        "What's the result of 100 * 0.15 + 50?",
        "Can you solve: 3 * (4 + 5) - 2 * 6?",
    ]

    for question in complex_questions:
        print(f"\n👤 Question: {question}")
        response = agent(question)
        print(f"🤖 Agent: {response}")

# ============================================================================
# Part 6: Async Tool Usage
# ============================================================================

async def async_calculator_example():
    """
    Demonstrate using tools with async agent operations.

    Note: When running multiple queries concurrently, each should use a separate
    agent instance to avoid conversation history contamination.
    """
    print("\n📍 Part 6: Async Tool Usage")
    print("-" * 30)

    working_model = create_working_model()
    if not working_model:
        print("⚠️ No API key available. Skipping async tool tests.")
        return

    # Define questions to ask
    questions = [
        "What is 123 + 456?",
        "Calculate 789 * 12",
        "What's 1000 / 25?",
    ]

    print("Running multiple calculations concurrently...")

    async def ask_question(question):
        """Helper function to ask a question with a fresh agent instance."""
        agent = Agent(
            model=working_model,
            tools=[calculator],
            system_prompt="You are a helpful calculator assistant."
        )
        return await agent.invoke_async(question)

    # Create concurrent tasks with separate agent instances
    tasks = [ask_question(q) for q in questions]

    # Wait for all results
    responses = await asyncio.gather(*tasks)

    # Display results
    for question, response in zip(questions, responses):
        print(f"\n👤 Q: {question}")
        print(f"🤖 A: {response}")

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """
    Run all examples to demonstrate tool concepts.
    """
    print("Welcome to Lesson 2: Your First Tool!")
    print("This lesson shows how to extend agents with custom capabilities.\n")

    # Load environment and check setup using shared utilities
    load_environment()

    # Check API keys and provide guidance
    if not check_api_keys():
        print("   Tool examples require a working model configuration.")
        return

    try:
        # Run synchronous examples
        basic_calculator_agent()
        test_error_handling()
        test_tool_selection()
        test_complex_calculations()

        # Run async example
        print("\n🔄 Running async example...")
        asyncio.run(async_calculator_example())

        print("\n" + "=" * 50)
        print("🎉 Lesson 2 Complete!")
        print("=" * 50)
        print("\n✅ Success Criteria Checklist:")
        print("   □ Tool is correctly invoked for math questions")
        print("   □ Agent explains calculations clearly")
        print("   □ Handles errors gracefully (division by zero, invalid input)")
        print("   □ Agent knows when NOT to use the calculator")
        print("   □ Tool results are properly formatted in responses")
        print("\n🧪 Experiments to Try:")
        print("   ")
        print("   Setup: Copy this lesson to experiments/ before tinkering:")
        print("      cp lesson_02_first_tool.py experiments/my_calculator_variant.py")
        print("      uv run python experiments/my_calculator_variant.py")
        print("   ")
        print("   Exercises:")
        print("   1. Add more mathematical functions (sin, cos, log)")
        print("   2. Test with very large numbers or complex expressions")
        print("   3. Create a unit converter tool following the same pattern")
        print("   4. Try word problems that require calculation")
        print("   5. Test edge cases like floating point precision")
        print("\n💡 Key Concepts Learned:")
        print("   • @tool decorator creates reusable agent capabilities")
        print("   • Tool descriptions help agents choose the right tool")
        print("   • Error handling in tools prevents agent crashes")
        print("   • Agents can intelligently decide when to use tools")
        print("\n➡️  Next: Run `uv run python lesson_03_multiple_tools.py`")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print_troubleshooting()

if __name__ == "__main__":
    main()
