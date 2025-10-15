#!/usr/bin/env python3
"""
Lesson 9: Distributed Multi-Agent Systems

Learn how to build distributed agent architectures with cross-platform communication:
- ☐ Agents-as-Tools pattern for hierarchical orchestration
- ☐ A2A Server for exposing agents over HTTP
- ☐ A2A Client for remote agent communication
- ☐ Combined patterns for distributed systems
- ☐ Best practices for agent discovery and error handling
"""

# Import shared utilities
from lesson_utils import (
    load_environment,
    create_working_model,
    check_api_keys,
    print_troubleshooting
)

# Import Strands components
from strands import Agent, tool


# =============================================================================
# Part 1: Agents as Tools Pattern - Hierarchical Orchestration
# =============================================================================

def part1_agents_as_tools():
    """Demonstrate Agents-as-Tools pattern with hierarchical orchestration.

    Pattern: Wrap specialized agents as callable tools for an orchestrator.
    Use case: Complex queries requiring multiple domains of expertise.

    Architecture:
        User -> Orchestrator Agent -> Specialist Agent Tools

    Benefits:
    - Separation of concerns (each agent has focused responsibility)
    - Hierarchical delegation (clear chain of command)
    - Modular architecture (specialists can be modified independently)
    - Improved performance (tailored prompts and tools per specialist)

    Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agents-as-tools/
    """
    print("\n" + "="*70)
    print("Part 1: Agents as Tools Pattern - Hierarchical Orchestration")
    print("="*70)

    model = create_working_model("multiagent")

    if not model:
        print_troubleshooting()
        return

    print("\n🏗️  Creating specialized agent tools...")

    # -------------------------------------------------------------------------
    # Step 1: Define Specialized Agent Tools
    # -------------------------------------------------------------------------
    # Each specialist is wrapped as a @tool function that creates and invokes
    # a specialized Agent with focused system prompts and capabilities.

    @tool
    def research_assistant(query: str) -> str:
        """
        Process research-related queries requiring factual information.

        Use this tool when the user asks for:
        - Historical facts and dates
        - Scientific explanations
        - Statistical data
        - General knowledge questions

        Args:
            query: A research question requiring factual information

        Returns:
            A detailed research answer with explanations
        """
        try:
            # Create a specialized research agent with focused system prompt
            research_agent = Agent(
                model=model,
                name="research_specialist",
                system_prompt="""You are a specialized research assistant.
                Focus only on providing factual, well-sourced information.
                Be concise but thorough. Explain your reasoning.
                If you're unsure, say so - don't make up information."""
            )

            # Invoke the specialist and return its response
            response = research_agent(query)
            return str(response)

        except Exception as e:
            return f"Error in research assistant: {str(e)}"

    @tool
    def data_analyst(query: str) -> str:
        """
        Perform data analysis, calculations, and quantitative reasoning.

        Use this tool when the user asks for:
        - Mathematical calculations
        - Data interpretation
        - Statistical analysis
        - Quantitative comparisons

        Args:
            query: A data analysis question requiring quantitative reasoning

        Returns:
            Analysis results with calculations and interpretations
        """
        try:
            analyst_agent = Agent(
                model=model,
                name="data_analyst_specialist",
                system_prompt="""You are a specialized data analyst.
                Focus on quantitative analysis, calculations, and data interpretation.
                Show your work step-by-step. Explain your methodology.
                Use clear numerical formatting."""
            )

            response = analyst_agent(query)
            return str(response)

        except Exception as e:
            return f"Error in data analyst: {str(e)}"

    @tool
    def creative_writer(query: str) -> str:
        """
        Generate creative content like stories, poems, or marketing copy.

        Use this tool when the user asks for:
        - Creative writing
        - Storytelling
        - Marketing copy
        - Poetic or artistic content

        Args:
            query: A creative writing request

        Returns:
            Original creative content
        """
        try:
            writer_agent = Agent(
                model=model,
                name="creative_writer_specialist",
                system_prompt="""You are a specialized creative writer.
                Focus on engaging, original content with vivid language.
                Be imaginative and expressive. Consider tone and audience.
                Create compelling narratives or copy."""
            )

            response = writer_agent(query)
            return str(response)

        except Exception as e:
            return f"Error in creative writer: {str(e)}"

    # -------------------------------------------------------------------------
    # Step 2: Create Orchestrator Agent
    # -------------------------------------------------------------------------
    # The orchestrator has clear routing logic in its system prompt and
    # access to all specialist agents as tools.

    print("✓ Created 3 specialist agent tools: research, analysis, creative")
    print("\n🎯 Creating orchestrator agent with routing logic...")

    orchestrator = Agent(
        model=model,
        name="orchestrator",
        system_prompt="""You are an intelligent orchestrator that routes queries
        to specialized agents:

        - For factual questions, history, science → Use research_assistant
        - For calculations, data analysis, numbers → Use data_analyst
        - For stories, creative content, marketing → Use creative_writer
        - For simple greetings or clarifications → Answer directly

        Always select the most appropriate specialist based on the query type.
        You can use multiple specialists if needed for complex queries.""",
        tools=[research_assistant, data_analyst, creative_writer]
    )

    print("✓ Orchestrator created with 3 specialist tools")

    # -------------------------------------------------------------------------
    # Step 3: Test Hierarchical Orchestration
    # -------------------------------------------------------------------------
    print("\n📋 Testing queries that require different specialists...\n")

    test_queries = [
        ("Research", "What caused the fall of the Roman Empire?"),
        ("Analysis", "If I invest $1000 at 5% annual interest for 3 years, how much will I have?"),
        ("Creative", "Write a short haiku about artificial intelligence"),
    ]

    for category, query in test_queries:
        print(f"[{category}] Query: {query}")
        print("-" * 70)

        try:
            response = orchestrator(query)
            print(f"Response: {response}\n")
        except Exception as e:
            print(f"Error: {str(e)}\n")

    # -------------------------------------------------------------------------
    # Key Observations
    # -------------------------------------------------------------------------
    print("\n💡 Key Concepts:")
    print("   • Each specialist agent has a focused system prompt and responsibility")
    print("   • The @tool decorator wraps agents as callable functions")
    print("   • The orchestrator intelligently routes to the right specialist")
    print("   • Specialists can be modified independently without affecting others")
    print("   • This pattern scales well with many specialized agents")


# =============================================================================
# Part 2: A2A Server - Exposing Agents over HTTP
# =============================================================================

def part2_a2a_server():
    """Demonstrate A2A Server for exposing agents over HTTP.

    Pattern: Expose a Strands agent as an A2A-compatible HTTP server.
    Use case: Make agents accessible remotely via standardized protocol.

    The A2A (Agent-to-Agent) protocol enables:
    - Multi-agent workflows across platforms
    - Agent marketplaces and discovery
    - Cross-platform integration
    - Distributed AI systems

    Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agent-to-agent/
    """
    print("\n" + "="*70)
    print("Part 2: A2A Server - Exposing Agents over HTTP")
    print("="*70)

    print("\n📦 A2A Server Installation:")
    print("   To use A2A functionality, install with the a2a extra:")
    print("   $ pip install 'strands-agents[a2a]'")
    print("   or")
    print("   $ uv pip install 'strands-agents[a2a]'")

    print("\n🔍 Checking A2A availability...")

    try:
        from strands.multiagent.a2a import A2AServer
        print("✓ A2A dependencies are installed")
    except ImportError:
        print("✗ A2A dependencies not found")
        print("\n⚠️  To run A2A examples:")
        print("   1. Install A2A dependencies: uv pip install 'strands-agents[a2a]'")
        print("   2. Re-run this lesson")
        print("\n   Skipping A2A server example for now...")
        return

    model = create_working_model("multiagent")

    if not model:
        print_troubleshooting()
        return

    print("\n🏗️  Creating an agent to expose as A2A server...")

    # -------------------------------------------------------------------------
    # Step 1: Create a Strands Agent
    # -------------------------------------------------------------------------
    # Any Strands agent can be exposed as an A2A server

    calculator_agent = Agent(
        model=model,
        name="Calculator Agent",
        description="A calculator agent that can perform arithmetic operations.",
        system_prompt="""You are a helpful calculator assistant.
        Perform arithmetic calculations accurately and explain your work.
        If asked non-math questions, politely redirect to mathematical queries."""
    )

    print("✓ Created calculator agent")

    # -------------------------------------------------------------------------
    # Step 2: Create A2A Server
    # -------------------------------------------------------------------------
    # Wrap the agent with A2AServer to expose it via HTTP
    # Configuration options:
    # - agent: The Strands Agent to expose
    # - host: Hostname to bind (default: "127.0.0.1")
    # - port: Port to bind (default: 9000)
    # - version: Agent version (default: "0.0.1")
    # - http_url: Public URL for path-based mounting (optional)

    print("\n🌐 Creating A2A server...")
    print("   Server will expose the agent at: http://127.0.0.1:9000")

    a2a_server = A2AServer(
        agent=calculator_agent,
        host="127.0.0.1",
        port=9000
    )

    print("✓ A2A server created")

    # -------------------------------------------------------------------------
    # Step 3: Server Usage Information
    # -------------------------------------------------------------------------
    print("\n📚 How to start the server:")
    print("   In a separate terminal or background process:")
    print("   ")
    print("   from strands import Agent")
    print("   from strands.multiagent.a2a import A2AServer")
    print("   ")
    print("   agent = Agent(...)")
    print("   server = A2AServer(agent=agent)")
    print("   server.serve()  # Starts the HTTP server")
    print("   ")
    print("   The server supports:")
    print("   • Agent card discovery at /.well-known/agent-card.json")
    print("   • SendMessageRequest (non-streaming)")
    print("   • SendStreamingMessageRequest (streaming)")

    print("\n💡 Advanced Server Features:")
    print("   • Custom middleware via to_fastapi_app() or to_starlette_app()")
    print("   • Path-based mounting for load balancers (http_url parameter)")
    print("   • Custom task storage with task_store parameter")
    print("   • Custom queue management with queue_manager parameter")

    print("\n⚠️  Note: This example doesn't start the server to avoid blocking.")
    print("   See experiments section for a complete server implementation.")


# =============================================================================
# Part 3: A2A Client - Remote Agent Communication
# =============================================================================

def part3_a2a_client():
    """Demonstrate A2A Client for communicating with remote agents.

    Pattern: Connect to and invoke remote agents via A2A protocol.
    Use case: Interact with agents hosted on different servers/platforms.

    Client types:
    - Synchronous: Single request-response
    - Streaming: Real-time streamed responses
    - Tool wrapper: Use remote agents as local tools

    Reference: https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agent-to-agent/
    """
    print("\n" + "="*70)
    print("Part 3: A2A Client - Remote Agent Communication")
    print("="*70)

    print("\n🔍 Checking A2A client availability...")

    try:
        from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
        from a2a.types import Message, Part, Role, TextPart
        print("✓ A2A client dependencies are installed")
    except ImportError:
        print("✗ A2A client dependencies not found")
        print("\n⚠️  To run A2A client examples:")
        print("   Install: uv pip install 'strands-agents[a2a]'")
        print("\n   Skipping A2A client example for now...")
        return

    print("\n📚 A2A Client Patterns:")
    print("\n1. Synchronous Client (request-response):")
    print("   async def send_sync_message(message, base_url='http://127.0.0.1:9000'):")
    print("       async with httpx.AsyncClient() as client:")
    print("           resolver = A2ACardResolver(httpx_client=client, base_url=base_url)")
    print("           agent_card = await resolver.get_agent_card()")
    print("           ")
    print("           config = ClientConfig(httpx_client=client, streaming=False)")
    print("           factory = ClientFactory(config)")
    print("           a2a_client = factory.create(agent_card)")
    print("           ")
    print("           msg = Message(kind='message', role=Role.user, parts=[...])")
    print("           async for event in a2a_client.send_message(msg):")
    print("               return event  # Single response")

    print("\n2. Streaming Client (real-time responses):")
    print("   # Same as above but with streaming=True")
    print("   config = ClientConfig(httpx_client=client, streaming=True)")
    print("   # Iterate through multiple events as they stream")

    print("\n3. A2A Client Tool Provider (easiest):")
    print("   from strands_tools.a2a_client import A2AClientToolProvider")
    print("   ")
    print("   provider = A2AClientToolProvider(")
    print("       known_agent_urls=['http://127.0.0.1:9000']")
    print("   )")
    print("   agent = Agent(tools=provider.tools)")
    print("   # Agent can now discover and interact with A2A servers")

    print("\n💡 Key A2A Client Concepts:")
    print("   • Agent Card: Metadata describing agent capabilities (auto-discovered)")
    print("   • Client Factory: Creates appropriate client based on agent card")
    print("   • Message Protocol: Standardized message format across platforms")
    print("   • Streaming vs Sync: Choose based on response time expectations")

    print("\n⚠️  Note: A2A clients require a running A2A server to connect to.")
    print("   See experiments section for complete client/server implementations.")


# =============================================================================
# Part 4: Combined Pattern - Distributed Architecture
# =============================================================================

def part4_combined_pattern():
    """Demonstrate combining Agents-as-Tools with A2A protocol.

    Pattern: Local orchestrator with both local and remote specialist agents.
    Use case: Distributed systems where some agents run locally, others remotely.

    Architecture:
        User -> Local Orchestrator -> Local Specialists (Agents-as-Tools)
                                  \-> Remote Specialists (A2A Clients)

    Benefits:
    - Flexible deployment (local vs remote based on requirements)
    - Scalability (distribute compute-intensive agents)
    - Integration (connect agents across different platforms)
    - Reusability (share specialist agents across systems)
    """
    print("\n" + "="*70)
    print("Part 4: Combined Pattern - Distributed Architecture")
    print("="*70)

    print("\n🏗️  Real-World Distributed Architecture:")
    print("\n   Scenario: Research & Analysis System")
    print("   • Local Orchestrator (this system)")
    print("   • Local Agent: Quick data analyst")
    print("   • Remote Agent: Heavy computation research engine (A2A)")
    print("   • Remote Agent: Specialized domain expert (A2A)")

    print("\n📐 Architecture Pattern:")
    print("   ")
    print("   ┌─────────────────────────────────────────┐")
    print("   │         User Application                │")
    print("   └──────────────┬──────────────────────────┘")
    print("                  │")
    print("   ┌──────────────▼──────────────────────────┐")
    print("   │    Local Orchestrator Agent             │")
    print("   │    (Agents-as-Tools pattern)            │")
    print("   └──┬──────────────────┬───────────────────┘")
    print("      │                  │")
    print("   ┌──▼─────────┐   ┌───▼──────────────────┐")
    print("   │ Local      │   │ Remote Agents (A2A)  │")
    print("   │ Specialist │   │ • Research Engine    │")
    print("   │ Tools      │   │ • Domain Expert      │")
    print("   └────────────┘   │ • Compute Cluster    │")
    print("                    └──────────────────────┘")

    print("\n💡 When to Use This Pattern:")
    print("   ✓ Some agents need expensive compute (GPUs, large models)")
    print("   ✓ Some agents have proprietary data/access")
    print("   ✓ Need to integrate agents from different providers")
    print("   ✓ Want to share specialized agents across multiple systems")
    print("   ✓ Need geographic distribution for latency/compliance")

    print("\n🔧 Implementation Approaches:")
    print("\n   1. Class-based A2A Tool (Recommended):")
    print("      • Discover agent card once during initialization")
    print("      • Wrap as @tool for orchestrator")
    print("      • Reduces repeated discovery overhead")
    print("   ")
    print("   2. A2AClientToolProvider (Quick Start):")
    print("      • Automatic agent discovery")
    print("      • Natural language interface")
    print("      • Good for dynamic agent marketplaces")
    print("   ")
    print("   3. Direct A2A Client (Full Control):")
    print("      • Manual message construction")
    print("      • Custom error handling")
    print("      • Advanced streaming scenarios")

    print("\n📊 Design Considerations:")
    print("   • Latency: Remote agents add network overhead")
    print("   • Reliability: Handle network failures gracefully")
    print("   • Security: Authenticate remote agent access")
    print("   • Cost: Consider compute/API costs per agent")
    print("   • Monitoring: Track performance of distributed calls")


# =============================================================================
# Main Function
# =============================================================================

def main():
    """Run all examples demonstrating distributed multi-agent patterns."""
    load_environment()

    print("="*70)
    print(" Lesson 9: Distributed Multi-Agent Systems")
    print("="*70)
    print("\n🎯 Learning Objectives:")
    print("   1. Understand Agents-as-Tools pattern for hierarchical orchestration")
    print("   2. Learn how to expose agents via A2A Server")
    print("   3. Connect to remote agents using A2A Client")
    print("   4. Combine patterns for distributed architectures")
    print("   5. Apply best practices for distributed agent systems")

    # Check API keys
    check_api_keys()

    # Run examples
    part1_agents_as_tools()
    part2_a2a_server()
    part3_a2a_client()
    part4_combined_pattern()

    # Success criteria
    print("\n" + "="*70)
    print("✅ Success Criteria")
    print("="*70)
    print("\nYou've mastered distributed agents when you can:")
    print("   ☐ Wrap specialized agents as tools with @tool decorator")
    print("   ☐ Build orchestrator agents that route to specialists")
    print("   ☐ Expose agents as A2A servers over HTTP")
    print("   ☐ Connect to remote agents using A2A clients")
    print("   ☐ Combine local and remote agents in distributed architectures")
    print("   ☐ Choose appropriate patterns for different use cases")
    print("   ☐ Handle errors and failures in distributed systems")

    # Experiments
    print("\n🧪 Experiments to Try:")
    print("   ")
    print("   Setup: Copy this lesson to experiments/ before tinkering:")
    print("      cp lesson_09_distributed_agents.py experiments/my_distributed_system.py")
    print("      uv run python experiments/my_distributed_system.py")
    print("   ")
    print("   Exercises:")
    print("   1. Add more specialist agents (translator, code reviewer, etc.)")
    print("   2. Create a multi-tier orchestration (orchestrator of orchestrators)")
    print("   3. Implement error handling and retries for specialist calls")
    print("   4. Build a complete A2A server and client pair")
    print("   5. Create a class-based A2A tool that caches agent cards")
    print("   6. Implement fallback logic when remote agents are unavailable")
    print("   7. Add monitoring/logging for distributed agent calls")
    print("   8. Create a load balancer that distributes across multiple remote agents")
    print("   9. Implement authentication for A2A server endpoints")
    print("   10. Build a real-world distributed system (e.g., research pipeline)")


if __name__ == "__main__":
    main()
