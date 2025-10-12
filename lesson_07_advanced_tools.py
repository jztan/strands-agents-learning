#!/usr/bin/env python3
"""
Lesson 7: Advanced Tools, Context & MCP

Learn advanced tool patterns for production-ready agents:
- ☑ Class-based tools with shared state
- ☑ ToolContext API for self-aware tools
- ☑ Invocation state for request-specific context
- ☑ SlidingWindowConversationManager for fixed-size history
- ☑ SummarizingConversationManager for intelligent compression
- ☑ Combined patterns for production agents
"""

from datetime import datetime

# Import shared utilities
from lesson_utils import (
    load_environment,
    create_working_model,
    check_api_keys,
    print_troubleshooting
)

# Import Strands components
from strands import Agent, tool, ToolContext
from strands.agent.conversation_manager import (
    NullConversationManager,
    SlidingWindowConversationManager,
    SummarizingConversationManager
)


# =============================================================================
# Part 1: Class-Based Tools (NotebookManager)
# =============================================================================

class NotebookManager:
    """
    Manage a simple notebook for storing user notes and ideas.

    Demonstrates class-based tools where multiple tools share state through
    instance attributes. This is useful when tools need to access common
    resources like connections, caches, or in this case, a shared notebook.

    Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/#class-based-tools
    """

    def __init__(self):
        # Shared state: all tool methods can access these instance attributes
        self.notes = {}  # key: note_id, value: content
        self.next_id = 1

    @tool
    def add_note(self, content: str) -> str:
        """Add a new note to the notebook.

        Args:
            content: The note content to store
        """
        note_id = self.next_id
        self.notes[note_id] = content
        self.next_id += 1
        return f"Added note #{note_id}: {content[:50]}..."

    @tool
    def get_note(self, note_id: int) -> str:
        """Retrieve a specific note by ID.

        Args:
            note_id: The ID of the note to retrieve
        """
        if note_id in self.notes:
            return f"Note #{note_id}: {self.notes[note_id]}"
        return f"Note #{note_id} not found"

    @tool
    def list_notes(self) -> str:
        """List all notes in the notebook."""
        if not self.notes:
            return "No notes yet"
        return "\n".join([f"#{id}: {content[:30]}..."
                          for id, content in self.notes.items()])

    @tool
    def delete_note(self, note_id: int) -> str:
        """Delete a note from the notebook.

        Args:
            note_id: The ID of the note to delete
        """
        if note_id in self.notes:
            del self.notes[note_id]
            return f"Deleted note #{note_id}"
        return f"Note #{note_id} not found"


def part1_class_based_tools():
    """Demonstrate class-based tools with shared state."""
    print("\n" + "="*70)
    print("Part 1: Class-Based Tools (NotebookManager)")
    print("="*70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Create an instance of the notebook manager
    # Each tool method (@tool decorated) has access to self.notes and self.next_id
    notebook = NotebookManager()

    # Pass the bound methods as tools to the agent
    agent = Agent(
        model=model,
        tools=[notebook.add_note, notebook.list_notes, notebook.get_note, notebook.delete_note],
        system_prompt="You are a helpful assistant with access to a notebook. Help users manage their notes."
    )

    print("\n📝 Testing notebook with multiple operations...")
    response1 = agent("Add a note: 'Buy groceries tomorrow'")
    print(f"Response 1: {response1}\n")

    response2 = agent("Add another note: 'Call dentist for appointment'")
    print(f"Response 2: {response2}\n")

    response3 = agent("What notes do I have?")
    print(f"Response 3: {response3}\n")

    print("✅ Class-based tools maintain shared state across invocations!")


# =============================================================================
# Part 2: ToolContext API - Self-Aware and Context-Aware Tools
# =============================================================================

@tool(context=True)
def log_interaction(message: str, tool_context: ToolContext) -> str:
    """Log an interaction with metadata for audit trail.

    This tool is "self-aware" - it can access information about:
    - The agent that invoked it
    - The specific tool invocation metadata
    - Custom invocation state passed in the request

    Args:
        message: The message to log
        tool_context: Automatically injected by Strands (context=True)
    """
    # Access agent properties
    agent_name = tool_context.agent.name

    # Access tool use metadata - includes toolUseId, toolName, input
    tool_id = tool_context.tool_use["toolUseId"]

    # Create log entry with metadata
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] Agent '{agent_name}' (tool {tool_id}): {message}"

    return f"Logged: {log_entry}"


@tool(context=True)
def send_email(to: str, subject: str, body: str, tool_context: ToolContext) -> str:
    """Send email with user identification for security.

    This demonstrates accessing invocation_state - data passed per-request
    that shouldn't appear in prompts but affects tool behavior.

    Args:
        to: Email recipient
        subject: Email subject line
        body: Email body content
        tool_context: Automatically injected (context=True)
    """
    # Access invocation state for user-specific data
    user_id = tool_context.invocation_state.get("user_id", "unknown")
    user_email = tool_context.invocation_state.get("user_email", "noreply@example.com")

    # In real implementation, would verify user_id matches authenticated user
    return f"Email sent from {user_email} (user: {user_id}) to {to}\nSubject: {subject}\nBody: {body}"


@tool(context=True)
def make_api_call(endpoint: str, tool_context: ToolContext) -> str:
    """Make API call with user-specific authentication.

    Shows how invocation_state can pass sensitive data like API keys
    without exposing them in conversation history.

    Args:
        endpoint: API endpoint to call
        tool_context: Automatically injected (context=True)
    """
    api_key = tool_context.invocation_state.get("api_key")
    user_id = tool_context.invocation_state.get("user_id")

    if not api_key:
        return "Error: No API key provided in invocation state"

    # Simulate API call with user authentication
    return f"Called {endpoint} with user {user_id}'s credentials (key: {api_key[:8]}...)"


def part2_tool_context():
    """Demonstrate ToolContext API for self-aware tools."""
    print("\n" + "="*70)
    print("Part 2: ToolContext API - Self-Aware Tools")
    print("="*70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    agent = Agent(
        model=model,
        tools=[log_interaction, send_email, make_api_call],
        name="ContextAgent",  # This name will be accessible via tool_context.agent.name
        system_prompt="You are a helpful assistant with logging, email, and API capabilities."
    )

    print("\n🔍 Testing self-aware logging tool...")
    response1 = agent("Log this message: 'User session started'")
    print(f"Response: {response1}\n")

    print("📧 Testing email with user context...")
    # Pass invocation_state with user-specific data
    response2 = agent(
        "Send an email to john@example.com with subject 'Meeting Tomorrow' and body 'See you at 2pm'",
        user_id="user_123",
        user_email="alice@company.com"
    )
    print(f"Response: {response2}\n")

    print("🔌 Testing API call with credentials...")
    response3 = agent(
        "Make an API call to /users/profile",
        user_id="user_123",
        api_key="sk_live_abc123xyz789"
    )
    print(f"Response: {response3}\n")

    print("✅ ToolContext provides access to agent properties, tool metadata, and invocation state!")


# =============================================================================
# Part 3: SlidingWindowConversationManager
# =============================================================================

def part3_sliding_window():
    """Demonstrate SlidingWindowConversationManager for fixed-size history."""
    print("\n" + "="*70)
    print("Part 3: SlidingWindowConversationManager")
    print("="*70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Create conversation manager with small window to demonstrate pruning
    conversation_manager = SlidingWindowConversationManager(
        window_size=6,  # Keep only 6 most recent messages (user + assistant pairs)
        should_truncate_results=True  # Truncate large tool results
    )

    notebook = NotebookManager()
    agent = Agent(
        model=model,
        tools=[notebook.add_note, notebook.list_notes],
        conversation_manager=conversation_manager,
        system_prompt="You are a helpful assistant with a notebook."
    )

    print(f"\n📊 Initial message count: {len(agent.messages)}")
    print(f"Window size: 6 messages\n")

    # Have a longer conversation to trigger window management
    print("💬 Having 8 exchanges (will exceed window size)...")

    agent("Add note: Meeting at 3pm")
    print(f"   After exchange 1: {len(agent.messages)} messages")

    agent("Add note: Buy coffee beans")
    print(f"   After exchange 2: {len(agent.messages)} messages")

    agent("Add note: Call Sarah back")
    print(f"   After exchange 3: {len(agent.messages)} messages")

    agent("Add note: Review pull request")
    print(f"   After exchange 4: {len(agent.messages)} messages")

    agent("Add note: Schedule dentist")
    print(f"   After exchange 5: {len(agent.messages)} messages")

    agent("Add note: Pay electricity bill")
    print(f"   After exchange 6: {len(agent.messages)} messages")

    agent("Add note: Water plants")
    print(f"   After exchange 7: {len(agent.messages)} messages")

    response = agent("What's the most recent note?")
    print(f"   After exchange 8: {len(agent.messages)} messages")
    print(f"\n   Final response: {response}")

    print(f"\n✅ Window maintained at ~{len(agent.messages)} messages (window_size=6)")
    print("   Older messages were automatically pruned!")


# =============================================================================
# Part 4: SummarizingConversationManager
# =============================================================================

def part4_summarizing():
    """Demonstrate SummarizingConversationManager for intelligent compression."""
    print("\n" + "="*70)
    print("Part 4: SummarizingConversationManager")
    print("="*70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Custom system prompt for technical summarization
    custom_prompt = """Summarize this conversation focusing on:
- Key information the user provided or requested
- Important decisions or preferences expressed
- Action items or tasks discussed
- Technical details like names, numbers, or specifications
Format as concise bullet points in third person."""

    conversation_manager = SummarizingConversationManager(
        summary_ratio=0.3,  # Summarize 30% of messages when context reduction needed
        preserve_recent_messages=3,  # Always keep 3 most recent messages
        summarization_system_prompt=custom_prompt
    )

    notebook = NotebookManager()
    agent = Agent(
        model=model,
        tools=[notebook.add_note, notebook.list_notes],
        conversation_manager=conversation_manager,
        system_prompt="You are a helpful project planning assistant with a notebook."
    )

    print(f"\n📊 Initial message count: {len(agent.messages)}")
    print("   Summary ratio: 0.3 (30%)")
    print("   Preserve recent: 3 messages\n")

    print("💬 Having extended planning conversation...")

    agent("I'm planning a new web application project")
    print(f"   After exchange 1: {len(agent.messages)} messages")

    agent("Add note: Project name is TaskMaster Pro")
    print(f"   After exchange 2: {len(agent.messages)} messages")

    agent("Add note: Target launch date Q2 2025")
    print(f"   After exchange 3: {len(agent.messages)} messages")

    agent("Add note: Use React frontend with FastAPI backend")
    print(f"   After exchange 4: {len(agent.messages)} messages")

    agent("Add note: PostgreSQL database with Redis cache")
    print(f"   After exchange 5: {len(agent.messages)} messages")

    agent("Add note: Deploy on AWS using ECS Fargate")
    print(f"   After exchange 6: {len(agent.messages)} messages")

    response = agent("What are the key technical decisions we've made?")
    print(f"   After exchange 7: {len(agent.messages)} messages")
    print(f"\n   Final response: {response}")

    print(f"\n✅ Summarization preserves context while managing token usage!")
    print("   Older messages were summarized into key points.")


# =============================================================================
# Part 5: Combined Pattern - ResearchAssistant
# =============================================================================

class ResearchAssistant:
    """
    Research assistant with source tracking and citation logging.

    This demonstrates a production-ready pattern combining:
    - Class-based tools for shared state (sources, citations)
    - ToolContext for user tracking and audit logging
    - Invocation state for user identification
    - Integration with conversation management

    Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/#class-based-tools
    """

    def __init__(self):
        # Shared state across all tool methods
        self.sources = {}  # Collected research sources
        self.citations = []  # Citation log with timestamps

    @tool(context=True)
    def add_source(self, url: str, title: str, summary: str,
                   tool_context: ToolContext) -> str:
        """Add a research source with automatic logging.

        Args:
            url: URL of the source
            title: Title of the source
            summary: Brief summary of the content
            tool_context: Injected context for logging
        """
        # Access invocation state for user tracking
        user_id = tool_context.invocation_state.get("user_id", "anonymous")
        tool_id = tool_context.tool_use["toolUseId"]

        # Store source with metadata
        self.sources[url] = {
            "title": title,
            "summary": summary,
            "added_by": user_id,
            "tool_id": tool_id,
            "timestamp": datetime.now().isoformat()
        }
        return f"Added source: {title} ({url})"

    @tool(context=True)
    def cite_source(self, url: str, tool_context: ToolContext) -> str:
        """Cite a source in your work.

        Args:
            url: URL of the source to cite
            tool_context: Injected context for tracking
        """
        if url not in self.sources:
            return f"Source {url} not found. Add it first with add_source."

        source = self.sources[url]
        user_id = tool_context.invocation_state.get("user_id", "anonymous")

        # Log citation with metadata
        citation = {
            "url": url,
            "title": source["title"],
            "cited_by": user_id,
            "timestamp": datetime.now().isoformat()
        }
        self.citations.append(citation)

        return f"Citation: {source['title']} - {url}"

    @tool
    def list_sources(self) -> str:
        """List all research sources."""
        if not self.sources:
            return "No sources added yet"

        result = "Research Sources:\n"
        for url, info in self.sources.items():
            result += f"- {info['title']}: {url}\n"
            result += f"  Summary: {info['summary']}\n"
            result += f"  Added by: {info['added_by']}\n"
        return result

    @tool
    def get_bibliography(self) -> str:
        """Generate bibliography from citations."""
        if not self.citations:
            return "No citations yet"

        result = "Bibliography:\n"
        for i, cite in enumerate(self.citations, 1):
            result += f"{i}. {cite['title']} - {cite['url']}\n"
        return result


def part5_combined_pattern():
    """Demonstrate combined pattern with ResearchAssistant."""
    print("\n" + "="*70)
    print("Part 5: Combined Pattern - ResearchAssistant")
    print("="*70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Create research assistant with all capabilities
    research = ResearchAssistant()

    # Combine with conversation management for long research sessions
    agent = Agent(
        model=model,
        tools=[
            research.add_source,
            research.cite_source,
            research.list_sources,
            research.get_bibliography
        ],
        conversation_manager=SlidingWindowConversationManager(window_size=10),
        system_prompt="You are a research assistant helping users collect and cite sources."
    )

    print("\n🔬 Using research assistant with context...")

    # Add sources with user context
    response1 = agent(
        "Add this source: https://arxiv.org/abs/1706.03762 titled 'Attention Is All You Need' "
        "with summary 'Introduces the Transformer architecture for sequence modeling'",
        user_id="researcher_alice"
    )
    print(f"Response 1: {response1}\n")

    response2 = agent(
        "Add another source: https://arxiv.org/abs/2005.14165 titled 'GPT-3 Paper' "
        "with summary 'Language models are few-shot learners'",
        user_id="researcher_alice"
    )
    print(f"Response 2: {response2}\n")

    response3 = agent(
        "Cite the Attention paper",
        user_id="researcher_alice"
    )
    print(f"Response 3: {response3}\n")

    response4 = agent("Generate a bibliography")
    print(f"Response 4: {response4}\n")

    print("✅ Combined pattern demonstrates production-ready agent design:")
    print("   • Class-based tools for shared state")
    print("   • ToolContext for user tracking and logging")
    print("   • Invocation state for per-request context")
    print("   • Conversation management for long sessions")


# =============================================================================
# Main Execution
# =============================================================================

def main():
    """Run all examples for Lesson 7."""
    print("\n" + "="*70)
    print("LESSON 7: Advanced Tools, Context & MCP")
    print("="*70)

    # Setup
    load_environment()
    check_api_keys()

    # Run all parts
    part1_class_based_tools()
    part2_tool_context()
    part3_sliding_window()
    part4_summarizing()
    part5_combined_pattern()

    # Success criteria
    print("\n" + "="*70)
    print("✅ SUCCESS CRITERIA")
    print("="*70)
    print("   ☑ Class-based tools share instance state correctly")
    print("   ☑ ToolContext accesses agent properties (name)")
    print("   ☑ Tool use ID and invocation data retrieved")
    print("   ☑ SlidingWindowConversationManager maintains window size")
    print("   ☑ SummarizingConversationManager preserves key information")
    print("   ☑ Context-aware tools adapt based on invocation state")
    print("   ☑ Combined pattern demonstrates production-ready design")

    # Experiments
    print("\n🧪 Experiments to Try:")
    print("   ")
    print("   Setup: Copy this lesson to experiments/ before tinkering:")
    print("      cp lesson_07_advanced_tools.py experiments/my_advanced_tools.py")
    print("      uv run python experiments/my_advanced_tools.py")
    print("   ")
    print("   Exercises:")
    print("   1. Build ContactManager class with add/search/update/delete contacts")
    print("   2. Create self-aware tool that tracks its own usage statistics")
    print("   3. Add custom summarization prompt optimizing for code discussions")
    print("   4. Build BookmarkManager with tags and search capabilities")
    print("   5. Create tool using invocation_state for multi-tenant applications")
    print("   6. Test SlidingWindow vs Summarizing with 50+ turn conversation")
    print("   7. Build FileOrganizer class with categorize/move/search methods")
    print("   8. Add custom conversation manager with hybrid window+summarization")
    print("   ")


if __name__ == "__main__":
    main()
