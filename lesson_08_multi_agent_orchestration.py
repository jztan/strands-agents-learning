#!/usr/bin/env python3
"""
Lesson 8: Multi-Agent Orchestration Patterns

Learn how to build systems with multiple collaborating agents:
- ☑ Graph pattern for deterministic workflows
- ☑ Swarm pattern for autonomous collaboration
- ☑ Workflow pattern for DAG-based execution
- ☑ Agent specialization and role definition
- ☑ State sharing between agents
- ☑ Choosing the right multi-agent pattern
"""

# Import shared utilities
from lesson_utils import (
    load_environment,
    create_working_model,
    check_api_keys,
    print_troubleshooting
)

# Import Strands components
from strands import Agent
from strands.multiagent import GraphBuilder, Swarm


# =============================================================================
# Part 1: Graph Pattern - Deterministic Workflows
# =============================================================================

def part1_graph_pattern():
    """Demonstrate Graph pattern with deterministic workflow."""
    print("\n" + "="*70)
    print("Part 1: Graph Pattern - Deterministic Workflow")
    print("="*70)

    # Multi-agent workflows need higher max_tokens (1500 vs default 500)
    model = create_working_model("multiagent")

    if not model:
        print_troubleshooting()
        return

    print("\n📊 Creating specialized research workflow agents...")

    # Create specialized agents for different research tasks
    researcher = Agent(
        model=model,
        name="researcher",
        system_prompt="""You are a research specialist. Your job is to gather
        key information on the given topic. Focus on finding factual,
        up-to-date information. Be concise but thorough."""
    )

    analyst = Agent(
        model=model,
        name="analyst",
        system_prompt="""You are a data analysis specialist. Analyze the research
        findings and extract key insights, patterns, and trends. Provide
        clear analysis with supporting evidence."""
    )

    fact_checker = Agent(
        model=model,
        name="fact_checker",
        system_prompt="""You are a fact-checking specialist. Verify the accuracy
        of information and identify any potential issues or inconsistencies.
        Flag anything that needs verification."""
    )

    report_writer = Agent(
        model=model,
        name="report_writer",
        system_prompt="""You are a report writing specialist. Create a clear,
        well-structured summary combining research, analysis, and fact-checking.
        Be concise and professional."""
    )

    print("✅ Created 4 specialized agents: researcher, analyst, fact_checker, report_writer\n")

    # Build the graph using GraphBuilder
    print("🔧 Building deterministic graph workflow...")
    builder = GraphBuilder()

    # Add nodes (agents) to the graph
    builder.add_node(researcher, "research")
    builder.add_node(analyst, "analysis")
    builder.add_node(fact_checker, "fact_check")
    builder.add_node(report_writer, "report")

    # Add edges (dependencies) - defines execution flow
    # Research must complete first, then analysis and fact-checking in parallel,
    # finally report combines both
    builder.add_edge("research", "analysis")
    builder.add_edge("research", "fact_check")
    builder.add_edge("analysis", "report")
    builder.add_edge("fact_check", "report")

    # Set entry point (where workflow starts)
    builder.set_entry_point("research")

    # Configure safety limits
    builder.set_execution_timeout(300)  # 5 minute timeout

    # Build the graph
    graph = builder.build()

    print("✅ Graph built successfully!")
    print("   Flow: research → (analysis + fact_check) → report\n")

    # Execute the graph
    print("🚀 Executing graph on task: 'Benefits of remote work'...")
    result = graph("What are 3 key benefits of remote work? Keep each benefit to 1-2 sentences.")

    print(f"\n📈 Graph execution completed!")
    print(f"   Status: {result.status}")
    print(f"   Nodes executed: {[node.node_id for node in result.execution_order]}")
    print(f"   Total nodes: {result.total_nodes}")
    print(f"   Completed: {result.completed_nodes}")

    # Show final report
    if "report" in result.results:
        final_result = result.results["report"].result
        print(f"\n📄 Final Report Preview:")
        print(f"   {str(final_result)[:200]}...")

    print("\n✅ Graph pattern demonstrates deterministic, structured workflows!")


# =============================================================================
# Part 2: Swarm Pattern - Autonomous Collaboration
# =============================================================================

def part2_swarm_pattern():
    """Demonstrate Swarm pattern with autonomous agent collaboration."""
    print("\n" + "="*70)
    print("Part 2: Swarm Pattern - Autonomous Collaboration")
    print("="*70)

    # Multi-agent workflows need higher max_tokens (1500 vs default 500)
    model = create_working_model("multiagent")

    if not model:
        print_troubleshooting()
        return

    print("\n🐝 Creating specialized swarm agents...")

    # Create specialized agents with clear roles
    # Simpler agent prompts that complete quickly
    idea_generator = Agent(
        model=model,
        name="idea_generator",
        system_prompt="""Generate 2-3 brief ideas. Then hand off to reviewer.""",
        description="Generates ideas"
    )

    reviewer = Agent(
        model=model,
        name="reviewer",
        system_prompt="""Review the ideas briefly (1-2 sentences). If good, approve and finish. Do NOT hand off again.""",
        description="Reviews and approves ideas"
    )

    print("✅ Created 2 specialized agents: idea_generator, reviewer\n")

    # Create a swarm with these agents
    print("🔧 Creating autonomous swarm...")
    swarm = Swarm(
        [idea_generator, reviewer],  # Simple 2-agent swarm
        entry_point=idea_generator,  # Start with idea generation
        max_handoffs=5,
        max_iterations=10,
        execution_timeout=300.0,  # 5 minutes
        node_timeout=60.0  # 1 minute per agent
    )

    print("✅ Swarm created with autonomous handoff capabilities!\n")

    # Execute the swarm
    print("🚀 Executing swarm on task: 'Features for mobile app'...")
    result = swarm("Suggest 2-3 features for a mobile todo app. Keep it brief.")

    print(f"\n📈 Swarm execution completed!")
    print(f"   Status: {result.status}")
    print(f"   Agent handoffs: {[node.node_id for node in result.node_history]}")
    print(f"   Total iterations: {result.execution_count}")

    # Show results from each agent
    print(f"\n🔍 Results from agents:")
    for agent_name, node_result in result.results.items():
        agent_output = str(node_result.result)[:150]
        print(f"   {agent_name}: {agent_output}...")

    print("\n✅ Swarm pattern demonstrates autonomous, emergent collaboration!")


# =============================================================================
# Part 3: Workflow Pattern - Sequential Coordination
# =============================================================================

def part3_workflow_pattern():
    """Demonstrate Workflow pattern with sequential task coordination."""
    print("\n" + "="*70)
    print("Part 3: Workflow Pattern - Sequential Coordination")
    print("="*70)

    # Multi-agent workflows need higher max_tokens (1500 vs default 500)
    model = create_working_model("multiagent")

    if not model:
        print_troubleshooting()
        return

    print("\n⚙️  Creating workflow agents...")

    # Create specialized agents for data processing workflow
    data_collector = Agent(
        model=model,
        name="data_collector",
        system_prompt="""You collect and extract data from sources. Organize
        the data in a structured format for analysis."""
    )

    data_analyzer = Agent(
        model=model,
        name="data_analyzer",
        system_prompt="""You analyze data to find patterns and insights.
        Use statistical thinking and identify key trends."""
    )

    report_generator = Agent(
        model=model,
        name="report_generator",
        system_prompt="""You create clear, professional reports from analysis.
        Structure findings logically with key takeaways."""
    )

    print("✅ Created 3 workflow agents: collector, analyzer, generator\n")

    # Implement simple sequential workflow
    print("🔧 Setting up sequential workflow pipeline...")
    print("   Pipeline: collect → analyze → report\n")

    task = "Analyze customer ratings (4.2/5 avg) and list top 2 improvements. Keep it brief."

    # Step 1: Data Collection
    print("📥 Step 1: Data Collection...")
    collection_result = data_collector(f"Collect and organize data for: {task}")
    print(f"   ✓ Collection complete: {str(collection_result)[:100]}...\n")

    # Step 2: Data Analysis
    print("📊 Step 2: Data Analysis...")
    analysis_prompt = f"Analyze this collected data:\n\n{collection_result}\n\nOriginal task: {task}"
    analysis_result = data_analyzer(analysis_prompt)
    print(f"   ✓ Analysis complete: {str(analysis_result)[:100]}...\n")

    # Step 3: Report Generation
    print("📄 Step 3: Report Generation...")
    report_prompt = f"Create a report from this analysis:\n\n{analysis_result}\n\nOriginal task: {task}"
    final_report = report_generator(report_prompt)
    print(f"   ✓ Report complete: {str(final_report)[:100]}...\n")

    print(f"📈 Workflow execution completed!")
    print(f"   Steps executed: collection → analysis → report")
    print(f"\n📄 Final Report Preview:")
    print(f"   {str(final_report)[:250]}...")

    print("\n✅ Workflow pattern demonstrates sequential task coordination!")


# =============================================================================
# Part 4: Pattern Comparison
# =============================================================================

def part4_pattern_comparison():
    """Compare the three multi-agent patterns."""
    print("\n" + "="*70)
    print("Part 4: Pattern Comparison")
    print("="*70)

    print("""
🔍 Understanding When to Use Each Pattern:

┌─────────────────────────────────────────────────────────────────────┐
│ GRAPH PATTERN - Deterministic Workflows                             │
├─────────────────────────────────────────────────────────────────────┤
│ Use when:                                                            │
│  • You need conditional logic and branching                          │
│  • Execution flow should be predictable                              │
│  • Multiple paths need to converge (e.g., parallel analysis)         │
│  • You want explicit error handling paths                            │
│                                                                       │
│ Examples:                                                             │
│  • Customer support routing (intent-based branching)                 │
│  • Data validation with error paths                                  │
│  • Document approval workflows                                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ SWARM PATTERN - Autonomous Collaboration                             │
├─────────────────────────────────────────────────────────────────────┤
│ Use when:                                                            │
│  • Problem benefits from multiple specialized perspectives           │
│  • Path between agents should emerge naturally                       │
│  • Agents need shared context and working memory                     │
│  • You want autonomous agent-to-agent handoffs                       │
│                                                                       │
│ Examples:                                                             │
│  • Software development (research → design → code → review)          │
│  • Incident response (detection → diagnosis → resolution)            │
│  • Creative brainstorming with multiple viewpoints                   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ WORKFLOW PATTERN - Sequential Coordination                           │
├─────────────────────────────────────────────────────────────────────┤
│ Use when:                                                            │
│  • You have a simple, repeatable sequential process                  │
│  • Each step clearly depends on the previous one                     │
│  • No complex branching or parallel paths needed                     │
│  • You want straightforward, easy-to-understand flow                 │
│                                                                       │
│ Examples:                                                             │
│  • Data processing pipelines (extract → transform → load)            │
│  • Content creation (research → write → edit)                        │
│  • Onboarding processes (create account → assign training → notify)  │
└─────────────────────────────────────────────────────────────────────┘

📊 Quick Comparison Table:

Feature              | Graph      | Swarm      | Workflow
---------------------|------------|------------|------------
Execution Flow       | Controlled | Autonomous | Sequential
Path Determination   | Dev-defined| Agent-led  | Dev-defined
Supports Cycles      | Yes        | Yes        | No
Parallel Execution   | Yes        | No         | Possible*
State Sharing        | Shared dict| Shared ctx | Result passing
Complexity          | Medium     | Medium     | Low
Use Case Fit        | Structured | Creative   | Simple pipelines

* Workflow tool from strands-agents-tools supports parallel execution

💡 Key Insight:
   Choose based on how much control you want over the execution path:
   • Graph = Explicit control with dynamic decisions
   • Swarm = Emergent path through autonomous handoffs
   • Workflow = Simple sequential steps
    """)


# =============================================================================
# Part 5: Shared State Across Patterns
# =============================================================================

def part5_shared_state():
    """Demonstrate shared state passing across multi-agent patterns."""
    print("\n" + "="*70)
    print("Part 5: Shared State Across Patterns")
    print("="*70)

    # Multi-agent workflows need higher max_tokens (1500 vs default 500)
    model = create_working_model("multiagent")

    if not model:
        print_troubleshooting()
        return

    print("""
🔑 Shared State with invocation_state:

Both Graph and Swarm patterns support passing shared state to all agents
through the `invocation_state` parameter. This enables sharing context and
configuration without exposing it to the LLM.

Common use cases:
• User identification (user_id, session_id)
• Configuration flags (debug_mode, feature_flags)
• Shared resources (database connections, API clients)
• Security context (authentication tokens, permissions)
""")

    # Create simple agents
    agent1 = Agent(model=model, name="agent1", system_prompt="You are agent 1")
    agent2 = Agent(model=model, name="agent2", system_prompt="You are agent 2")

    # Create a simple graph
    builder = GraphBuilder()
    builder.add_node(agent1, "step1")
    builder.add_node(agent2, "step2")
    builder.add_edge("step1", "step2")
    builder.set_entry_point("step1")
    graph = builder.build()

    # Shared state that will be passed to all agents
    shared_state = {
        "user_id": "user_123",
        "session_id": "sess_456",
        "debug_mode": True,
        "feature_flags": {"new_ui": True, "beta_features": False}
    }

    print("\n🔧 Example: Passing shared state to Graph...\n")
    print(f"   Shared state: {shared_state}\n")

    # Execute with shared state (in real usage, tools would access via ToolContext)
    result = graph(
        "Process this request",
        **shared_state  # Passed as invocation_state
    )

    print(f"✅ Graph executed with shared state!")
    print(f"   Status: {result.status}")
    print("""
💡 Note: Tools can access invocation_state via ToolContext:

   @tool(context=True)
   def my_tool(query: str, tool_context: ToolContext) -> str:
       user_id = tool_context.invocation_state.get("user_id")
       debug = tool_context.invocation_state.get("debug_mode", False)
       # Use context for personalized, context-aware operations
       return f"Processing for user {user_id}"

This keeps sensitive data (like user IDs, API keys) out of conversation
history while still making it available to tools and hooks.
""")


# =============================================================================
# Main Execution
# =============================================================================

def main():
    """Run all examples for Lesson 8."""
    print("\n" + "="*70)
    print("LESSON 8: Multi-Agent Orchestration Patterns")
    print("="*70)

    # Setup
    load_environment()
    check_api_keys()

    # Run all parts
    part1_graph_pattern()
    part2_swarm_pattern()
    part3_workflow_pattern()
    part4_pattern_comparison()
    part5_shared_state()

    # Success criteria
    print("\n" + "="*70)
    print("✅ SUCCESS CRITERIA")
    print("="*70)
    print("   ☑ Graph pattern executes deterministic workflow with parallel branches")
    print("   ☑ Swarm pattern shows autonomous agent handoffs")
    print("   ☑ Workflow pattern demonstrates sequential coordination")
    print("   ☑ State sharing works with invocation_state")
    print("   ☑ Understand when to use each pattern")
    print("   ☑ Can compare Graph vs Swarm vs Workflow tradeoffs")

    # Experiments
    print("\n🧪 Experiments to Try:")
    print("   ")
    print("   Setup: Copy this lesson to experiments/ before tinkering:")
    print("      cp lesson_08_multi_agent_orchestration.py experiments/my_multi_agent.py")
    print("      uv run python experiments/my_multi_agent.py")
    print("   ")
    print("   Exercises:")
    print("   1. Build customer support graph with intent-based routing")
    print("   2. Create swarm with 5+ specialized agents (add tester, documenter)")
    print("   3. Add conditional edges to graph (quality check with retry loop)")
    print("   4. Implement error handling path in graph workflow")
    print("   5. Compare same task with Graph vs Swarm (which works better?)")
    print("   6. Build data pipeline workflow with validation steps")
    print("   7. Create nested pattern: Swarm node inside a Graph")
    print("   8. Add shared state tools that use invocation_state context")
    print("   9. Implement cyclic graph with max execution limits")
    print("   10. Build multi-agent system for code generation + review + testing")
    print("   ")


if __name__ == "__main__":
    main()
