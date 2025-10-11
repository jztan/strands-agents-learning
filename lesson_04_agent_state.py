#!/usr/bin/env python3
"""
Lesson 4: Agent State & Session Persistence

Learn how to use Strands SDK's state management features:
- Agent State API: agent.state.get() and agent.state.set()
- Building tools that read/write agent state
- Persisting state across sessions with FileSessionManager
- Understanding state vs conversation history

Learning Objectives:
□ Understand the difference between agent state and conversation history
□ Use agent.state.get() and agent.state.set() to manage state
□ Access agent state from within tools
□ Persist state across application restarts using FileSessionManager
□ Validate state with JSON-serializable data types
"""

import os
from lesson_utils import (
    load_environment,
    create_working_model,
    check_api_keys,
    print_troubleshooting,
)
from strands import Agent, tool
from strands.session.file_session_manager import FileSessionManager


# ============================================================================
# Part 1: Basic Agent State API
# ============================================================================
# Agent state provides key-value storage outside conversation context.
# Unlike conversation history, state is NOT passed to the LLM but can be
# accessed by tools and application logic.
# Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/state/


def part1_basic_state():
    """Demonstrate basic agent state get/set operations."""
    print("\n" + "=" * 70)
    print("PART 1: Basic Agent State API")
    print("=" * 70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Create agent with initial state
    agent = Agent(
        model=model,
        state={"user_name": "Alice", "preferences": {"theme": "dark"}, "count": 0},
    )

    print("\n1. Initial state:")
    print(f"   Full state: {agent.state.get()}")
    print(f"   User name: {agent.state.get('user_name')}")
    print(f"   Preferences: {agent.state.get('preferences')}")

    print("\n2. Setting new state values:")
    agent.state.set("last_action", "login")
    agent.state.set("count", 1)
    print(f"   Updated state: {agent.state.get()}")

    print("\n3. Deleting state values:")
    agent.state.delete("last_action")
    print(f"   State after deletion: {agent.state.get()}")

    print("\n4. Testing state validation (JSON-serializable only):")
    # Valid types
    agent.state.set("string_val", "hello")
    agent.state.set("number_val", 42)
    agent.state.set("boolean_val", True)
    agent.state.set("list_val", [1, 2, 3])
    agent.state.set("dict_val", {"nested": "data"})
    agent.state.set("null_val", None)
    print("   ✓ All valid JSON types accepted")

    # Invalid type (will raise ValueError)
    try:
        agent.state.set("function", lambda x: x)
        print("   ✗ ERROR: Should have rejected non-JSON type!")
    except ValueError as e:
        print(f"   ✓ Correctly rejected non-JSON type: {e}")


# ============================================================================
# Part 2: Using State in Tools
# ============================================================================
# Tools can access and modify agent state by accepting an 'agent: Agent'
# parameter. This is useful for maintaining information across tool calls.


@tool
def add_todo(item: str, agent: Agent):
    """Add a todo item to the list."""
    # Get current todos from agent state (or empty list if none)
    todos = agent.state.get("todos") or []

    # Add new item
    todos.append({"id": len(todos) + 1, "text": item, "done": False})

    # Save back to state
    agent.state.set("todos", todos)

    return f"Added todo: {item} (ID: {len(todos)})"


@tool
def list_todos(agent: Agent):
    """List all todo items."""
    todos = agent.state.get("todos") or []

    if not todos:
        return "No todos yet!"

    result = "Your todos:\n"
    for todo in todos:
        status = "✓" if todo["done"] else "○"
        result += f"{status} {todo['id']}. {todo['text']}\n"

    return result.strip()


@tool
def complete_todo(todo_id: int, agent: Agent):
    """Mark a todo as complete."""
    todos = agent.state.get("todos") or []

    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            agent.state.set("todos", todos)
            return f"Completed todo: {todo['text']}"

    return f"Todo {todo_id} not found"


@tool
def delete_todo(todo_id: int, agent: Agent):
    """Delete a todo item."""
    todos = agent.state.get("todos") or []

    # Filter out the todo with matching ID
    updated_todos = [t for t in todos if t["id"] != todo_id]

    if len(updated_todos) == len(todos):
        return f"Todo {todo_id} not found"

    agent.state.set("todos", updated_todos)
    return f"Deleted todo {todo_id}"


def part2_stateful_tools():
    """Demonstrate tools that use agent state."""
    print("\n" + "=" * 70)
    print("PART 2: Using State in Tools")
    print("=" * 70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Create agent with stateful todo tools
    agent = Agent(
        model=model,
        tools=[add_todo, list_todos, complete_todo, delete_todo],
        system_prompt="You are a helpful todo list assistant. Help users manage their tasks.",
    )

    print("\n1. Adding todos:")
    response = agent("Add 'Buy groceries' and 'Finish homework' to my list")
    print(f"   Agent: {response}")

    print("\n2. Listing todos:")
    response = agent("Show me my todos")
    print(f"   Agent: {response}")

    print("\n3. Completing a todo:")
    response = agent("Mark todo 1 as done")
    print(f"   Agent: {response}")

    print("\n4. Checking state directly:")
    print(f"   Current todos in state: {agent.state.get('todos')}")

    print("\n5. Deleting a todo:")
    response = agent("Delete todo 2")
    print(f"   Agent: {response}")


# ============================================================================
# Part 3: Session Persistence with FileSessionManager
# ============================================================================
# FileSessionManager persists agent state and conversation history to disk.
# This allows agents to maintain continuity across application restarts.
# Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/session-management/


def part3_session_persistence():
    """Demonstrate persistent sessions using FileSessionManager."""
    print("\n" + "=" * 70)
    print("PART 3: Session Persistence with FileSessionManager")
    print("=" * 70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Create a session manager with a unique session ID
    # Sessions are stored in the default temp directory unless storage_dir is specified
    session_manager = FileSessionManager(
        session_id="lesson-4-demo",
        storage_dir=".sessions",  # Store in local .sessions directory
    )

    print(f"\n1. Creating agent with session persistence:")
    print(f"   Session ID: lesson-4-demo")
    print(f"   Storage dir: .sessions/")

    # Create agent with session manager
    agent = Agent(
        model=model,
        session_manager=session_manager,
        tools=[add_todo, list_todos, complete_todo, delete_todo],
        system_prompt="You are a helpful todo list assistant.",
    )

    # Check if this is a restored session
    existing_todos = agent.state.get("todos")
    if existing_todos:
        print(f"\n2. Restored existing session with {len(existing_todos)} todos")
        response = agent("Show me my todos")
        print(f"   Agent: {response}")
    else:
        print(f"\n2. New session - adding some todos")
        response = agent("Add 'Learn Strands state management' to my list")
        print(f"   Agent: {response}")
        response = agent("Add 'Build a persistent agent' to my list")
        print(f"   Agent: {response}")

    print("\n3. Current state:")
    print(f"   Todos: {agent.state.get('todos')}")
    print(f"   Messages: {len(agent.messages)} messages in conversation")

    print("\n4. Session persistence in action:")
    print("   ✓ All state and messages are automatically saved to disk")
    print("   ✓ Run this script again to see the session restored!")
    print("   ✓ Session files stored in: .sessions/session_lesson-4-demo/")


# ============================================================================
# Part 4: State vs Conversation History
# ============================================================================
# Understanding the difference between state and conversation history is key.


def part4_state_vs_history():
    """Demonstrate the difference between state and conversation history."""
    print("\n" + "=" * 70)
    print("PART 4: State vs Conversation History")
    print("=" * 70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    agent = Agent(model=model, state={"user_id": "12345", "login_count": 0})

    print("\n1. Key Differences:")
    print("   - Conversation History (agent.messages):")
    print("     • Passed to the LLM on each request")
    print("     • Contains user/assistant messages, tool calls, tool results")
    print("     • Subject to context window limits")
    print("     • Managed by ConversationManager (default: SlidingWindow)")
    print("")
    print("   - Agent State (agent.state):")
    print("     • NOT passed to the LLM")
    print("     • Key-value storage for application data")
    print("     • No size limits (but must be JSON-serializable)")
    print("     • Accessible from tools via 'agent' parameter")

    print("\n2. Conversation history example:")
    response = agent("Hello! My name is Alice.")
    print(f"   User: Hello! My name is Alice.")
    print(f"   Agent: {response}")
    print(f"   Messages in history: {len(agent.messages)}")

    print("\n3. Agent state example:")
    agent.state.set("user_name", "Alice")
    agent.state.set("login_count", agent.state.get("login_count") + 1)
    print(f"   State updated: {agent.state.get()}")
    print(f"   (State NOT visible to LLM, only accessible via tools)")

    print("\n4. When to use each:")
    print("   Use Conversation History for:")
    print("     • User-agent dialogue")
    print("     • Context the LLM needs to see")
    print("     • Tool call/result pairs")
    print("")
    print("   Use Agent State for:")
    print("     • User preferences/settings")
    print("     • Application data (todos, counters, etc.)")
    print("     • Metadata not needed by LLM")
    print("     • Data shared between tools")


# ============================================================================
# Main Function
# ============================================================================


def main():
    """Run all lesson examples."""
    print("\n" + "=" * 70)
    print("LESSON 4: Agent State & Session Persistence")
    print("=" * 70)
    print("\nThis lesson demonstrates Strands SDK state management:")
    print("- Agent state API (get/set/delete)")
    print("- Using state in tools")
    print("- Session persistence with FileSessionManager")
    print("- State vs conversation history")

    # Load environment and check API keys
    load_environment()
    check_api_keys()

    # Run all parts
    part1_basic_state()
    part2_stateful_tools()
    part3_session_persistence()
    part4_state_vs_history()

    # Success criteria
    print("\n" + "=" * 70)
    print("SUCCESS CRITERIA")
    print("=" * 70)
    print("✓ Part 1: Basic state operations (get/set/delete) work")
    print("✓ Part 2: Tools can read/write agent state")
    print("✓ Part 3: FileSessionManager persists state to disk")
    print("✓ Part 4: Understand state vs conversation history")
    print("\nNext: Run this script again to see session restoration in Part 3!")

    # Experiments to try
    print("\n" + "=" * 70)
    print("EXPERIMENTS TO TRY")
    print("=" * 70)
    print("1. Run Part 3 multiple times to see session persistence")
    print("2. Build a shopping cart with state and session persistence")
    print("3. Track user preferences across conversations")
    print("4. Implement a counter that persists across restarts")
    print("5. Test S3SessionManager for cloud-based persistence")
    print("\nCopy this file to experiments/ and try these variations!")


if __name__ == "__main__":
    main()
