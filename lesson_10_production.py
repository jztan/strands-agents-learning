#!/usr/bin/env python3
"""
Lesson 10: Production-Ready Agents

Learn how to build production-ready agents with safety, observability, and evaluation:
- ☑ Guardrails for content filtering and safety
- ☑ PII redaction with hooks for privacy protection
- ☑ OpenTelemetry for metrics and traces
- ☑ Agent performance monitoring and evaluation
- ☑ Production deployment best practices
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
from strands.hooks import HookProvider, HookRegistry, MessageAddedEvent, AfterInvocationEvent


# =============================================================================
# Part 1: Safety & Security - Guardrails and PII Redaction
# =============================================================================

def part1_safety_security():
    """Demonstrate safety and security patterns for production agents.

    Key Patterns:
    1. Guardrails - Content filtering, topic blocking, safety boundaries
    2. PII Redaction - Protecting sensitive personal information

    Production Importance:
    - Legal compliance (GDPR, CCPA, HIPAA)
    - Risk management (reduce legal/reputational risks)
    - User trust (deliver appropriate, safe responses)
    - Security (protect sensitive data)

    Reference: https://strandsagents.com/latest/documentation/docs/user-guide/safety-security/guardrails/
              https://strandsagents.com/latest/documentation/docs/user-guide/safety-security/pii-redaction/
    """
    print("\n" + "="*70)
    print("Part 1: Safety & Security - Guardrails and PII Redaction")
    print("="*70)

    model = create_working_model()

    if not model:
        print_troubleshooting()
        return

    # -------------------------------------------------------------------------
    # Pattern 1: Bedrock Guardrails (Built-in Protection)
    # -------------------------------------------------------------------------
    print("\n📋 Pattern 1: Bedrock Guardrails")
    print("\nBedrock provides built-in guardrails for:")
    print("   • Content filtering (hate speech, profanity, violence)")
    print("   • Topic blocking (custom disallowed topics)")
    print("   • PII detection and redaction")
    print("   • Response quality enforcement")
    print("\n   Setup:")
    print("   from strands.models import BedrockModel")
    print("   ")
    print("   model = BedrockModel(")
    print("       model_id='anthropic.claude-3-5-sonnet-20241022-v2:0',")
    print("       guardrail_id='your-guardrail-id',")
    print("       guardrail_version='1',")
    print("       guardrail_trace='enabled'")
    print("   )")
    print("   ")
    print("   agent = Agent(model=model)")
    print("   response = agent('user query')")
    print("   ")
    print("   # Check if guardrail intervened")
    print("   if response.stop_reason == 'guardrail_intervened':")
    print("       print('Content blocked by guardrails')")

    # -------------------------------------------------------------------------
    # Pattern 2: Notify-Only Guardrails with Hooks (Shadow Mode)
    # -------------------------------------------------------------------------
    print("\n\n📋 Pattern 2: Notify-Only Guardrails (Shadow Mode)")
    print("\nUse hooks to monitor guardrail triggers without blocking:")
    print("   • Track when guardrails would trigger")
    print("   • Tune policies before enforcement")
    print("   • Monitor content patterns")
    print("\n   Benefits:")
    print("   • Safe testing in production")
    print("   • Data-driven policy tuning")
    print("   • Gradual rollout capability")

    print("\n🔧 Implementing Notify-Only Guardrails with Hooks...\n")

    class NotifyOnlyGuardrailsHook(HookProvider):
        """
        Hook-based guardrails that notify without blocking.

        This pattern allows monitoring what would be blocked without
        actually blocking content. Useful for:
        - Testing guardrails before enforcement
        - Gathering data for policy tuning
        - Monitoring edge cases

        In production, you would integrate with AWS Bedrock's
        ApplyGuardrail API or other guardrail services.
        """
        def __init__(self):
            # In production, initialize guardrail client here
            # self.bedrock_client = boto3.client("bedrock-runtime")
            # self.guardrail_id = "your-guardrail-id"
            self.blocked_patterns = [
                "sensitive",
                "confidential",
                "secret",
                "password",
                "credit card"
            ]

        def register_hooks(self, registry: HookRegistry) -> None:
            """Register hooks for input and output monitoring."""
            registry.add_callback(MessageAddedEvent, self.check_user_input)
            registry.add_callback(AfterInvocationEvent, self.check_assistant_response)

        def evaluate_content(self, content: str, source: str = "INPUT"):
            """
            Evaluate content for policy violations.

            In production, this would call AWS Bedrock ApplyGuardrail API
            or other guardrail service in shadow mode.
            """
            content_lower = content.lower()

            # Simple pattern matching for demonstration
            # Production would use sophisticated ML-based detection
            violations = [
                pattern for pattern in self.blocked_patterns
                if pattern in content_lower
            ]

            if violations:
                print(f"\n[GUARDRAIL] WOULD BLOCK - {source}: {content[:100]}...")
                print(f"[GUARDRAIL] Violations: {', '.join(violations)}")
                print("[GUARDRAIL] In production: integrate with Bedrock ApplyGuardrail API\n")

        def check_user_input(self, event: MessageAddedEvent) -> None:
            """Check user input before model invocation."""
            if event.message.get("role") == "user":
                content = "".join(
                    block.get("text", "")
                    for block in event.message.get("content", [])
                )
                if content:
                    self.evaluate_content(content, "INPUT")

        def check_assistant_response(self, event: AfterInvocationEvent) -> None:
            """Check assistant response after model invocation."""
            if event.agent.messages and event.agent.messages[-1].get("role") == "assistant":
                assistant_message = event.agent.messages[-1]
                content = "".join(
                    block.get("text", "")
                    for block in assistant_message.get("content", [])
                )
                if content:
                    self.evaluate_content(content, "OUTPUT")

    # Create agent with guardrail monitoring
    agent = Agent(
        model=model,
        system_prompt="You are a helpful assistant.",
        hooks=[NotifyOnlyGuardrailsHook()]
    )

    print("✓ Agent created with notify-only guardrails")
    print("\n📝 Testing with potentially sensitive content...\n")

    # Test queries that would trigger guardrails
    test_queries = [
        "What is machine learning? Answer in 2 sentences.",  # Safe query
        "Tell me about sensitive data handling in 2 sentences",  # Would trigger
    ]

    for query in test_queries:
        print(f"Query: {query}")
        print("-" * 70)
        response = agent(query)
        print(f"Response: {str(response)[:200]}...\n")

    # -------------------------------------------------------------------------
    # Pattern 3: PII Redaction with Hooks
    # -------------------------------------------------------------------------
    print("\n📋 Pattern 3: PII Redaction for Privacy")
    print("\nProtect Personally Identifiable Information (PII):")
    print("   • Names, emails, phone numbers")
    print("   • Social security numbers, credit cards")
    print("   • Addresses, IP addresses")
    print("   • Health records, financial data")
    print("\n   Implementation Options:")
    print("   1. Third-party libraries (LLM Guard, Presidio, AWS Comprehend)")
    print("   2. Hook-based redaction before/after model calls")
    print("   3. OpenTelemetry collector-level masking")
    print("\n   Example with hooks:")
    print("   class PIIRedactionHook(HookProvider):")
    print("       def register_hooks(self, registry):")
    print("           registry.add_callback(BeforeInvocationEvent, self.redact_input)")
    print("           registry.add_callback(AfterInvocationEvent, self.redact_output)")
    print("   ")
    print("   For production: Use specialized libraries like:")
    print("   • LLM Guard: pip install llm-guard")
    print("   • Microsoft Presidio: pip install presidio-analyzer")
    print("   • AWS Comprehend PII detection")

    print("\n💡 Key Takeaways:")
    print("   • Guardrails = Safety boundaries for content")
    print("   • PII Redaction = Privacy protection")
    print("   • Hooks = Flexible integration point")
    print("   • Shadow mode = Safe testing approach")
    print("   • Compliance = Legal requirement, not optional")


# =============================================================================
# Part 2: Observability - Metrics and Traces
# =============================================================================

def part2_observability():
    """Demonstrate observability patterns for production monitoring.

    Key Concepts:
    1. Metrics - Performance measurements (tokens, latency, tool usage)
    2. Traces - Execution flow visibility (spans, cycles, tool calls)
    3. Logs - Structured logging for debugging

    Why Observability Matters:
    - Debug issues in production
    - Monitor performance and costs
    - Optimize agent behavior
    - Track user satisfaction
    - Detect regressions

    Reference: https://strandsagents.com/latest/documentation/docs/user-guide/observability-evaluation/observability/
    """
    print("\n" + "="*70)
    print("Part 2: Observability - Metrics and Traces")
    print("="*70)

    model = create_working_model()

    if not model:
        print_troubleshooting()
        return

    # -------------------------------------------------------------------------
    # Pattern 1: Agent Metrics (Built-in)
    # -------------------------------------------------------------------------
    print("\n📊 Pattern 1: Built-in Agent Metrics")
    print("\nEvery agent invocation returns rich metrics:")
    print("   • Token usage (input, output, total, cache)")
    print("   • Execution time and cycles")
    print("   • Tool usage statistics")
    print("   • Latency measurements")

    print("\n🔧 Creating agent and capturing metrics...\n")

    # Simple agent for demonstration
    agent = Agent(
        model=model,
        system_prompt="You are a helpful assistant that provides concise responses."
    )

    # Invoke agent and capture result with metrics
    print("Query: 'Explain what an AI agent is in 2 sentences'")
    print("-" * 70)

    result = agent("Explain what an AI agent is in 2 sentences")

    print(f"Response: {result}\n")

    # -------------------------------------------------------------------------
    # Access Metrics from AgentResult
    # -------------------------------------------------------------------------
    print("📈 Metrics Analysis:")
    print("-" * 70)

    # Token usage
    usage = result.metrics.accumulated_usage
    print(f"\n💰 Token Usage:")
    print(f"   Input tokens:  {usage['inputTokens']}")
    print(f"   Output tokens: {usage['outputTokens']}")
    print(f"   Total tokens:  {usage['totalTokens']}")

    # Performance metrics
    metrics_data = result.metrics.accumulated_metrics
    print(f"\n⚡ Performance:")
    print(f"   Latency: {metrics_data['latencyMs']}ms")
    print(f"   Cycles:  {result.metrics.cycle_count}")

    if result.metrics.cycle_durations:
        avg_cycle = sum(result.metrics.cycle_durations) / len(result.metrics.cycle_durations)
        print(f"   Avg cycle time: {avg_cycle:.3f}s")

    # Tool usage (if any tools were called)
    if result.metrics.tool_metrics:
        print(f"\n🔧 Tool Usage:")
        for tool_name, tool_metric in result.metrics.tool_metrics.items():
            print(f"   {tool_name}:")
            print(f"      Calls: {tool_metric.call_count}")
            print(f"      Success: {tool_metric.success_count}")
            print(f"      Errors: {tool_metric.error_count}")
            print(f"      Total time: {tool_metric.total_time:.3f}s")

    # -------------------------------------------------------------------------
    # Pattern 2: Comprehensive Metrics Summary
    # -------------------------------------------------------------------------
    print("\n\n📋 Pattern 2: Comprehensive Metrics Summary")
    print("\nUse get_summary() for complete metrics overview:")

    summary = result.metrics.get_summary()
    print(f"\n   Total Duration: {summary.get('total_duration', 0):.3f}s")
    print(f"   Total Cycles: {summary.get('total_cycles', 0)}")
    print(f"   Avg Cycle Time: {summary.get('average_cycle_time', 0):.3f}s")

    print("\n   Full summary available with:")
    print("   import json")
    print("   print(json.dumps(result.metrics.get_summary(), indent=2))")

    # -------------------------------------------------------------------------
    # Pattern 3: OpenTelemetry Traces (Production Monitoring)
    # -------------------------------------------------------------------------
    print("\n\n📋 Pattern 3: OpenTelemetry Traces (Production)")
    print("\nOpenTelemetry provides industry-standard observability:")
    print("   • Distributed tracing across services")
    print("   • Integration with observability platforms")
    print("   • Standardized instrumentation")
    print("\n   Installation:")
    print("   pip install 'strands-agents[otel]'")
    print("\n   Setup:")
    print("   from strands.telemetry import StrandsTelemetry")
    print("   ")
    print("   telemetry = StrandsTelemetry()")
    print("   telemetry.setup_otlp_exporter()      # Send to collector")
    print("   telemetry.setup_console_exporter()   # Print to console")
    print("   ")
    print("   agent = Agent(")
    print("       model=model,")
    print("       trace_attributes={")
    print("           'session.id': 'abc-1234',")
    print("           'user.id': 'user@example.com',")
    print("           'environment': 'production'")
    print("       }")
    print("   )")
    print("\n   Integration with:")
    print("   • Jaeger - Open-source tracing")
    print("   • AWS X-Ray - AWS native")
    print("   • Datadog, New Relic - Commercial platforms")
    print("   • Langfuse - AI-specific observability")

    print("\n\n💡 Key Observability Practices:")
    print("   • Monitor token usage for cost optimization")
    print("   • Track latency for user experience")
    print("   • Analyze tool performance for debugging")
    print("   • Use traces for troubleshooting failures")
    print("   • Set up alerts for anomalies")
    print("   • Regular metrics reviews for optimization")


# =============================================================================
# Part 3: Evaluation - Testing and Quality Assurance
# =============================================================================

def part3_evaluation():
    """Demonstrate evaluation patterns for agent quality assurance.

    Key Patterns:
    1. Performance Testing - Metrics-based evaluation
    2. Test Case Design - Structured test scenarios
    3. Regression Detection - Monitoring for quality degradation

    Why Evaluation Matters:
    - Ensure consistent quality
    - Detect regressions early
    - Validate improvements
    - Build user confidence
    - Meet SLA requirements

    Reference: https://strandsagents.com/latest/documentation/docs/user-guide/observability-evaluation/
    """
    print("\n" + "="*70)
    print("Part 3: Evaluation - Testing and Quality Assurance")
    print("="*70)

    model = create_working_model()

    if not model:
        print_troubleshooting()
        return

    # -------------------------------------------------------------------------
    # Pattern 1: Metrics-Based Evaluation
    # -------------------------------------------------------------------------
    print("\n📊 Pattern 1: Metrics-Based Performance Evaluation")
    print("\nTrack quantitative metrics to ensure quality:")
    print("   • Response latency < SLA threshold")
    print("   • Token usage within budget")
    print("   • Tool success rate > 95%")
    print("   • Cycle count efficiency")

    print("\n🔧 Running performance evaluation...\n")

    agent = Agent(
        model=model,
        system_prompt="You are a helpful assistant."
    )

    # Define test cases with expected performance criteria
    test_cases = [
        {
            "query": "What is 2+2?",
            "max_latency_ms": 5000,
            "max_tokens": 100,
            "description": "Simple arithmetic query"
        },
        {
            "query": "Explain quantum computing in one sentence",
            "max_latency_ms": 8000,
            "max_tokens": 150,
            "description": "Concise explanation request"
        },
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}/{len(test_cases)}: {test_case['description']}")
        print("-" * 70)

        result = agent(test_case["query"])

        # Evaluate metrics against criteria
        latency = result.metrics.accumulated_metrics["latencyMs"]
        total_tokens = result.metrics.accumulated_usage["totalTokens"]

        passed = True
        issues = []

        if latency > test_case["max_latency_ms"]:
            passed = False
            issues.append(f"Latency {latency}ms > {test_case['max_latency_ms']}ms")

        if total_tokens > test_case["max_tokens"]:
            passed = False
            issues.append(f"Tokens {total_tokens} > {test_case['max_tokens']}")

        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"Status: {status}")
        print(f"Latency: {latency}ms (max: {test_case['max_latency_ms']}ms)")
        print(f"Tokens: {total_tokens} (max: {test_case['max_tokens']})")

        if issues:
            print(f"Issues: {', '.join(issues)}")

        results.append({
            "test": test_case["description"],
            "passed": passed,
            "latency": latency,
            "tokens": total_tokens
        })
        print()

    # -------------------------------------------------------------------------
    # Summary Report
    # -------------------------------------------------------------------------
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    pass_rate = (passed_count / total_count) * 100 if total_count > 0 else 0

    print("📈 Evaluation Summary:")
    print("-" * 70)
    print(f"Tests Run: {total_count}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {total_count - passed_count}")
    print(f"Pass Rate: {pass_rate:.1f}%")

    avg_latency = sum(r["latency"] for r in results) / len(results)
    avg_tokens = sum(r["tokens"] for r in results) / len(results)

    print(f"\nAverage Latency: {avg_latency:.0f}ms")
    print(f"Average Tokens: {avg_tokens:.0f}")

    # -------------------------------------------------------------------------
    # Pattern 2: Structured Test Suite Design
    # -------------------------------------------------------------------------
    print("\n\n📋 Pattern 2: Structured Test Suite Design")
    print("\nBest practices for agent testing:")
    print("\n   1. Functional Tests")
    print("      • Core capabilities work correctly")
    print("      • Tools execute successfully")
    print("      • Error handling works")
    print("\n   2. Performance Tests")
    print("      • Latency within SLA")
    print("      • Token usage optimized")
    print("      • Resource utilization acceptable")
    print("\n   3. Quality Tests")
    print("      • Response relevance and accuracy")
    print("      • Tone and style consistency")
    print("      • Safety and appropriateness")
    print("\n   4. Regression Tests")
    print("      • Previous bugs don't reoccur")
    print("      • Quality doesn't degrade")
    print("      • Performance maintains baseline")

    # -------------------------------------------------------------------------
    # Pattern 3: LLM Judge for Quality Evaluation
    # -------------------------------------------------------------------------
    print("\n\n📋 Pattern 3: LLM Judge for Quality Evaluation")
    print("\nUse an LLM to evaluate response quality:")
    print("\n   Example:")
    print("   judge_agent = Agent(")
    print("       model=model,")
    print("       system_prompt='You are an expert evaluator...'")
    print("   )")
    print("   ")
    print("   evaluation = judge_agent(f'''")
    print("   Evaluate this response on a scale of 1-10:")
    print("   Query: {original_query}")
    print("   Response: {agent_response}")
    print("   ")
    print("   Criteria: Relevance, Accuracy, Helpfulness")
    print("   ''')")
    print("\n   Benefits:")
    print("   • Automated quality assessment")
    print("   • Consistent evaluation criteria")
    print("   • Scale to large test suites")
    print("   • Catch subtle quality issues")

    print("\n\n💡 Key Evaluation Principles:")
    print("   • Define clear success criteria")
    print("   • Automate testing where possible")
    print("   • Monitor metrics continuously")
    print("   • Establish performance baselines")
    print("   • Test before and after changes")
    print("   • Use both quantitative and qualitative measures")


# =============================================================================
# Part 4: Production Deployment Best Practices
# =============================================================================

def part4_production_best_practices():
    """Summarize production deployment best practices.

    Key Topics:
    1. Security and Privacy
    2. Monitoring and Alerting
    3. Scalability and Performance
    4. Cost Optimization
    5. Incident Response
    """
    print("\n" + "="*70)
    print("Part 4: Production Deployment Best Practices")
    print("="*70)

    print("\n🛡️ Security and Privacy:")
    print("   ✓ Enable guardrails for content safety")
    print("   ✓ Implement PII redaction")
    print("   ✓ Use secure credential management")
    print("   ✓ Encrypt data in transit and at rest")
    print("   ✓ Regular security audits")
    print("   ✓ Access control and authentication")

    print("\n📊 Monitoring and Alerting:")
    print("   ✓ Set up OpenTelemetry tracing")
    print("   ✓ Monitor token usage and costs")
    print("   ✓ Track latency and error rates")
    print("   ✓ Alert on anomalies and failures")
    print("   ✓ Dashboard for key metrics")
    print("   ✓ Log aggregation and search")

    print("\n⚡ Scalability and Performance:")
    print("   ✓ Async/streaming for responsiveness")
    print("   ✓ Caching for repeated queries")
    print("   ✓ Connection pooling for efficiency")
    print("   ✓ Load balancing for distribution")
    print("   ✓ Auto-scaling for demand")
    print("   ✓ Rate limiting for protection")

    print("\n💰 Cost Optimization:")
    print("   ✓ Monitor token usage patterns")
    print("   ✓ Use caching to reduce API calls")
    print("   ✓ Optimize prompts for efficiency")
    print("   ✓ Choose appropriate models")
    print("   ✓ Set budget alerts")
    print("   ✓ Regular cost reviews")

    print("\n🚨 Incident Response:")
    print("   ✓ Defined escalation procedures")
    print("   ✓ Runbooks for common issues")
    print("   ✓ Fallback mechanisms")
    print("   ✓ Circuit breakers for failures")
    print("   ✓ Post-incident reviews")
    print("   ✓ Continuous improvement")

    print("\n📐 Architecture Patterns:")
    print("   • Microservices for modularity")
    print("   • Event-driven for scalability")
    print("   • Queue-based for reliability")
    print("   • Multi-region for availability")
    print("   • Blue-green for safe deployments")

    print("\n🔄 Deployment Strategies:")
    print("   • Canary releases (gradual rollout)")
    print("   • Feature flags (controlled activation)")
    print("   • A/B testing (comparative evaluation)")
    print("   • Shadow mode (risk-free testing)")
    print("   • Rollback procedures (quick recovery)")


# =============================================================================
# Main Function
# =============================================================================

def main():
    """Run all examples demonstrating production-ready patterns."""
    load_environment()

    print("="*70)
    print(" Lesson 10: Production-Ready Agents")
    print("="*70)
    print("\n🎯 Learning Objectives:")
    print("   1. Implement guardrails for content safety")
    print("   2. Protect PII with redaction hooks")
    print("   3. Monitor agents with metrics and traces")
    print("   4. Evaluate agent quality systematically")
    print("   5. Apply production deployment best practices")

    # Check API keys
    check_api_keys()

    # Run examples
    part1_safety_security()
    part2_observability()
    part3_evaluation()
    part4_production_best_practices()

    # Success criteria
    print("\n" + "="*70)
    print("✅ Success Criteria")
    print("="*70)
    print("\nYou've mastered production-ready agents when you can:")
    print("   ☑ Implement guardrails for content safety")
    print("   ☑ Use hooks for PII redaction")
    print("   ☑ Access and interpret agent metrics")
    print("   ☑ Set up OpenTelemetry tracing")
    print("   ☑ Design structured test suites")
    print("   ☑ Evaluate agents with quantitative metrics")
    print("   ☑ Apply production deployment best practices")
    print("   ☑ Understand security, monitoring, and scalability trade-offs")

    # Experiments
    print("\n🧪 Experiments to Try:")
    print("   ")
    print("   Setup: Copy this lesson to experiments/ before tinkering:")
    print("      cp lesson_10_production.py experiments/my_production_agent.py")
    print("      uv run python experiments/my_production_agent.py")
    print("   ")
    print("   Exercises:")
    print("   1. Integrate with AWS Bedrock Guardrails")
    print("   2. Implement PII redaction with LLM Guard or Presidio")
    print("   3. Set up OpenTelemetry with Jaeger locally")
    print("   4. Create comprehensive test suite with 20+ test cases")
    print("   5. Implement LLM Judge for quality evaluation")
    print("   6. Build metrics dashboard with visualization")
    print("   7. Add alerting for latency/error rate thresholds")
    print("   8. Implement caching layer for repeated queries")
    print("   9. Create incident response runbook")
    print("   10. Deploy agent with canary release strategy")

    print("\n🎓 Congratulations!")
    print("   You've completed all 10 lessons of the Strands Agent Framework!")
    print("   You now have the skills to build production-ready AI agents.")
    print("\n📚 Next Steps:")
    print("   • Build your own production agent")
    print("   • Explore AWS deployment options")
    print("   • Contribute to the Strands community")
    print("   • Share your agent projects!")


if __name__ == "__main__":
    main()
