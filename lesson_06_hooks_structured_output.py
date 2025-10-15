#!/usr/bin/env python3
"""
Lesson 6: Hooks & Structured Output

Learn how to extend agent functionality using lifecycle hooks and extract type-safe
responses using Pydantic models.

Concepts covered:
- Lifecycle hooks (BeforeInvocationEvent, AfterInvocationEvent)
- Tool execution hooks (BeforeToolCallEvent, AfterToolCallEvent)
- HookProvider pattern for composable extensions
- Structured output with Pydantic models
- Type-safe data extraction from conversations

Learning goals:
[ ] Understand the agent lifecycle and hook events
[ ] Implement custom hooks for logging and monitoring
[ ] Modify tool behavior using hooks
[ ] Extract structured data using Pydantic models
[ ] Handle complex nested data structures

Official Documentation:
- Hooks: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/hooks/
- Structured Output: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/structured-output/
- API Reference: https://strandsagents.com/latest/documentation/docs/api-reference/hooks/
"""

from lesson_utils import load_environment, create_working_model, check_api_keys
from strands import Agent, tool
from strands.hooks import HookProvider, HookRegistry
from strands.hooks.events import (
    BeforeInvocationEvent,
    AfterInvocationEvent,
    BeforeToolCallEvent,
    AfterToolCallEvent,
    MessageAddedEvent,
)
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ============================================================================
# Part 1: Basic Lifecycle Hooks
# ============================================================================
# Hooks are a composable extensibility mechanism for extending agent
# functionality by subscribing to events throughout the agent lifecycle.
#
# The hook system enables monitoring, modifying, and extending agent behavior
# through strongly-typed event callbacks.
#
# Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/hooks/

def part1_basic_lifecycle_hooks():
    """Demonstrate basic lifecycle hooks for request monitoring."""
    print("\n" + "="*70)
    print("Part 1: Basic Lifecycle Hooks")
    print("="*70)

    # Method 1: Individual callback registration
    # You can register callbacks for specific events using add_callback
    print("\n1. Individual callback registration:")

    agent = Agent(model=create_working_model())

    def log_request_start(event: BeforeInvocationEvent) -> None:
        """Called before agent processes a request."""
        print(f"   🚀 Request started for agent: {event.agent.name}")
        print(f"      Timestamp: {datetime.now().strftime('%H:%M:%S')}")

    def log_request_end(event: AfterInvocationEvent) -> None:
        """Called after agent completes a request."""
        print(f"   ✅ Request completed for agent: {event.agent.name}")
        print(f"      Timestamp: {datetime.now().strftime('%H:%M:%S')}")

    # Register individual callbacks
    # Reference: https://strandsagents.com/latest/documentation/docs/api-reference/hooks/#strands.hooks.registry.HookRegistry.add_callback
    agent.hooks.add_callback(BeforeInvocationEvent, log_request_start)
    agent.hooks.add_callback(AfterInvocationEvent, log_request_end)

    response = agent("What is 2 + 2?")
    print(f"\n   Agent response: {response}")

    # Method 2: HookProvider pattern (recommended for multiple related hooks)
    # The HookProvider protocol allows a single object to register callbacks
    # for multiple events - this is the preferred composable approach
    print("\n2. HookProvider pattern (composable):")

    class RequestLoggingHook(HookProvider):
        """Reusable hook for logging request lifecycle.

        Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/hooks/#creating-a-hook-provider
        """

        def register_hooks(self, registry: HookRegistry) -> None:
            """Register all callbacks for this hook."""
            registry.add_callback(BeforeInvocationEvent, self.log_start)
            registry.add_callback(AfterInvocationEvent, self.log_end)
            registry.add_callback(MessageAddedEvent, self.log_message)

        def log_start(self, event: BeforeInvocationEvent) -> None:
            print(f"   📝 [Hook] Request starting...")

        def log_end(self, event: AfterInvocationEvent) -> None:
            print(f"   📝 [Hook] Request completed!")

        def log_message(self, event: MessageAddedEvent) -> None:
            """Log when messages are added to conversation history."""
            role = event.message.get("role", "unknown")
            print(f"   📝 [Hook] Message added: role={role}")

    # Pass hook provider during agent initialization
    agent_with_hooks = Agent(
        model=create_working_model(),
        hooks=[RequestLoggingHook()]
    )

    response = agent_with_hooks("Tell me a fun fact about Python programming.")
    print(f"\n   Agent response: {response}")


# ============================================================================
# Part 2: Tool Execution Hooks
# ============================================================================
# Hooks can intercept and modify tool execution, allowing you to:
# - Log tool usage and parameters
# - Modify tool inputs before execution
# - Process or format tool results after execution
# - Access invocation_state for context-aware behavior
#
# Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/hooks/#advanced-usage

@tool
def translate_text(text: str, target_language: str) -> str:
    """Translate text to a target language.

    Args:
        text: The text to translate
        target_language: Target language (e.g., 'Spanish', 'French', 'German')
    """
    # Simulated translation - in production, would use a real translation API
    translations = {
        "spanish": {"hello": "hola", "world": "mundo", "thank you": "gracias", "goodbye": "adiós"},
        "french": {"hello": "bonjour", "world": "monde", "thank you": "merci", "goodbye": "au revoir"},
        "german": {"hello": "hallo", "world": "welt", "thank you": "danke", "goodbye": "auf wiedersehen"},
        "italian": {"hello": "ciao", "world": "mondo", "thank you": "grazie", "goodbye": "arrivederci"},
        "japanese": {"hello": "こんにちは", "world": "世界", "thank you": "ありがとう", "goodbye": "さようなら"}
    }

    lang = target_language.lower()
    text_lower = text.lower()

    if lang in translations and text_lower in translations[lang]:
        return translations[lang][text_lower]
    else:
        # Simulate translation by adding language prefix
        return f"[{target_language}] {text}"


def part2_tool_execution_hooks():
    """Demonstrate hooks for monitoring and modifying tool execution."""
    print("\n" + "="*70)
    print("Part 2: Tool Execution Hooks")
    print("="*70)

    class ToolMonitoringHook(HookProvider):
        """Hook for monitoring and modifying tool execution.

        Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/hooks/#result-modification
        """

        def register_hooks(self, registry: HookRegistry) -> None:
            registry.add_callback(BeforeToolCallEvent, self.log_tool_call)
            registry.add_callback(AfterToolCallEvent, self.format_result)

        def log_tool_call(self, event: BeforeToolCallEvent) -> None:
            """Log tool calls before execution."""
            tool_name = event.tool_use.get("name", "unknown")
            tool_input = event.tool_use.get("input", {})

            print(f"   🔧 Tool call: {tool_name}")
            print(f"      Input: {tool_input}")

            # Access invocation_state for context
            # Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/hooks/#accessing-invocation-state-in-hooks
            user_id = event.invocation_state.get("user_id", "anonymous")
            print(f"      User: {user_id}")

        def format_result(self, event: AfterToolCallEvent) -> None:
            """Format tool results after execution.

            Event properties can be modified to influence agent behavior.
            Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/hooks/#hook-behaviors
            """
            tool_name = event.tool_use.get("name", "unknown")

            if tool_name == "translate_text":
                # Modify the tool result to add formatting
                # The 'result' property is writable for AfterToolCallEvent
                original_content = event.result["content"][0]["text"]
                event.result["content"][0]["text"] = f"Translation: {original_content}"
                print(f"   ✨ Formatted result for {tool_name}")

    # Create agent with tool monitoring hook
    agent = Agent(
        model=create_working_model(),
        tools=[translate_text],
        hooks=[ToolMonitoringHook()]
    )

    # Execute with invocation_state for context
    # invocation_state is accessible in BeforeToolCallEvent and AfterToolCallEvent
    response = agent(
        "Translate 'hello' to Spanish",
        user_id="user123"  # Custom context passed to hooks
    )

    print(f"\n   Agent response: {response}")


# ============================================================================
# Part 3: Structured Output with Pydantic
# ============================================================================
# Structured output enables type-safe, validated responses using Pydantic models.
# Instead of parsing raw text, you define the exact structure and receive a
# validated Python object.
#
# Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/structured-output/

def part3_structured_output():
    """Demonstrate structured output for type-safe data extraction."""
    print("\n" + "="*70)
    print("Part 3: Structured Output with Pydantic")
    print("="*70)

    # Example 1: Basic structured extraction
    print("\n1. Basic structured extraction:")

    class PersonInfo(BaseModel):
        """Extract person information from text.

        Pydantic models define the structure for structured output.
        Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/structured-output/#usage
        """
        name: str = Field(description="Full name of the person")
        age: int = Field(description="Age in years")
        occupation: str = Field(description="Job or profession")

    agent = Agent(model=create_working_model())

    # Extract structured information from text
    result = agent.structured_output(
        PersonInfo,
        "Sarah Chen is a 28-year-old data scientist working at a tech startup."
    )

    print(f"   Name: {result.name}")
    print(f"   Age: {result.age}")
    print(f"   Occupation: {result.occupation}")
    print(f"   Type: {type(result)}")  # Pydantic model instance

    # Example 2: Complex nested models
    print("\n2. Complex nested models:")

    class Address(BaseModel):
        """Nested model for address information."""
        street: str
        city: str
        country: str
        postal_code: Optional[str] = None

    class Contact(BaseModel):
        """Nested model for contact information."""
        email: Optional[str] = None
        phone: Optional[str] = None

    class DetailedPerson(BaseModel):
        """Complete person profile with nested data.

        Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/structured-output/#complex-nested-models
        """
        name: str = Field(description="Full name")
        age: int = Field(description="Age in years")
        address: Address = Field(description="Home address")
        contacts: List[Contact] = Field(default_factory=list, description="Contact methods")
        skills: List[str] = Field(default_factory=list, description="Professional skills")

    result = agent.structured_output(
        DetailedPerson,
        """
        Extract information about: John Smith, a 35-year-old software architect.
        He lives at 123 Market Street, San Francisco, CA 94103.
        Contact him at john.smith@example.com or (415) 555-0123.
        His skills include Python, Kubernetes, and system design.
        """
    )

    print(f"   Name: {result.name}")
    print(f"   Age: {result.age}")
    print(f"   Address: {result.address.street}, {result.address.city}")
    print(f"   Email: {result.contacts[0].email if result.contacts else 'N/A'}")
    print(f"   Skills: {', '.join(result.skills)}")

    # Example 3: Using conversation history
    print("\n3. Structured output from conversation:")

    class CityInfo(BaseModel):
        """Extract city information from conversation.

        structured_output can work with existing conversation context.
        Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/structured-output/#using-conversation-history
        """
        city: str
        country: str
        population: Optional[int] = None
        famous_for: List[str] = Field(default_factory=list)
        best_season: Optional[str] = None

    conversation_agent = Agent(model=create_working_model())

    # Build up conversation context
    conversation_agent("What do you know about Tokyo, Japan?")
    conversation_agent("What's the population and what is it famous for?")
    conversation_agent("When is the best time to visit?")

    # Extract structured information from the conversation
    city_data = conversation_agent.structured_output(
        CityInfo,
        "Extract all the information we discussed about this city"
    )

    print(f"   City: {city_data.city}")
    print(f"   Country: {city_data.country}")
    print(f"   Population: {city_data.population if city_data.population else 'Not specified'}")
    print(f"   Famous for: {', '.join(city_data.famous_for)}")
    print(f"   Best season: {city_data.best_season if city_data.best_season else 'Not specified'}")


# ============================================================================
# Part 4: Combining Hooks and Structured Output
# ============================================================================
# Hooks and structured output work together for production-ready patterns

def part4_combined_patterns():
    """Demonstrate combining hooks with structured output."""
    print("\n" + "="*70)
    print("Part 4: Combining Hooks and Structured Output")
    print("="*70)

    class AuditHook(HookProvider):
        """Audit hook that tracks structured output requests."""

        def __init__(self):
            self.structured_requests = []

        def register_hooks(self, registry: HookRegistry) -> None:
            registry.add_callback(BeforeInvocationEvent, self.track_request)
            registry.add_callback(AfterInvocationEvent, self.log_completion)

        def track_request(self, event: BeforeInvocationEvent) -> None:
            # Track if this is a structured output request
            print(f"   📊 Audit: Request started at {datetime.now().strftime('%H:%M:%S')}")

        def log_completion(self, event: AfterInvocationEvent) -> None:
            print(f"   📊 Audit: Request completed at {datetime.now().strftime('%H:%M:%S')}")

    class ProductInfo(BaseModel):
        """Product information model."""
        name: str
        price: float
        category: str
        in_stock: bool

    # Create agent with audit hook
    agent = Agent(
        model=create_working_model(),
        hooks=[AuditHook()]
    )

    # Use structured output with hook monitoring
    product = agent.structured_output(
        ProductInfo,
        "Extract product info: The UltraBook Pro laptop costs $1299, it's a computer, and is currently available."
    )

    print(f"\n   Product: {product.name}")
    print(f"   Price: ${product.price}")
    print(f"   Category: {product.category}")
    print(f"   Available: {'Yes' if product.in_stock else 'No'}")


# ============================================================================
# Main execution
# ============================================================================

def main():
    """Run all examples demonstrating hooks and structured output."""
    load_environment()
    check_api_keys()

    print("\n🎯 Lesson 6: Hooks & Structured Output")
    print("=" * 70)

    part1_basic_lifecycle_hooks()
    part2_tool_execution_hooks()
    part3_structured_output()
    part4_combined_patterns()

    print("\n" + "="*70)
    print("✅ Success! You've learned:")
    print("   - Agent lifecycle events and hook registration")
    print("   - HookProvider pattern for composable extensions")
    print("   - Tool execution monitoring and modification")
    print("   - Structured output with Pydantic models")
    print("   - Complex nested data extraction")
    print("   - Combining hooks with structured output")

    print("\n📚 Key Takeaways:")
    print("   1. Hooks provide composable extensibility throughout agent lifecycle")
    print("   2. Use HookProvider pattern for reusable, multi-event hooks")
    print("   3. BeforeToolCallEvent/AfterToolCallEvent enable tool behavior modification")
    print("   4. Structured output transforms unstructured text into type-safe objects")
    print("   5. Pydantic models enable validation and IDE type hints")
    print("   6. invocation_state provides context to hooks across invocations")

    print("\n🧪 Experiments to Try:")
    print("   ")
    print("   Setup: Copy this lesson to experiments/ before tinkering:")
    print("      cp lesson_06_hooks_structured_output.py experiments/my_hooks_variant.py")
    print("      uv run python experiments/my_hooks_variant.py")
    print("   ")
    print("   Exercises:")
    print("   1. Create a PerformanceMonitoringHook that tracks request duration")
    print("   2. Build a ToolCacheHook that caches tool results to avoid redundant calls")
    print("   3. Implement a ValidationHook that checks tool inputs before execution")
    print("   4. Create a Pydantic model to extract meeting details from text")
    print("   5. Build a hook that automatically logs structured outputs to a file")
    print("   6. Combine multiple hooks (logging + performance + audit) on one agent")
    print("   7. Experiment with cancel_tool in BeforeToolCallEvent to prevent execution")
    print("   8. Create a hook that modifies tool_use parameters before execution")

    print("\n📖 Next Steps:")
    print("   - Lesson 7: Advanced Tools, Context & MCP")
    print("   - Lesson 10: Production observability with OpenTelemetry")


if __name__ == "__main__":
    main()
