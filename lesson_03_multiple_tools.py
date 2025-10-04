#!/usr/bin/env python3
"""
Lesson 3: Multiple Tools & Context

This lesson demonstrates how agents select and orchestrate multiple tools.

Concepts covered:
- Tool selection logic based on descriptions
- Multiple tool registration with `tools=[tool1, tool2, tool3]`
- Tool orchestration and chaining in single response
- Complex reasoning chains with multiple steps
- Tool interdependencies and combined results
- Context-aware tool selection

Learning goals:
□ Agent selects appropriate tool based on query intent
□ Can chain multiple tools in one response seamlessly
□ Handles ambiguous requests using conversation context
□ Combines tool results into coherent responses
□ Tool selection is accurate even with overlapping capabilities
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from strands import Agent, tool

# Import shared utilities for model configuration
from lesson_utils import (
    load_environment,
    create_working_model,
    check_api_keys,
    print_troubleshooting
)


# =============================================================================
# TOOL 1: Weather Tool
# =============================================================================

@tool
def get_weather(city: str) -> str:
    """Get current weather conditions for a city.

    Args:
        city: The name of the city to get weather for

    Returns:
        Current weather conditions including temperature and description
    """
    # Mock weather data for demonstration
    # In production, this would call a real weather API
    weather_data = {
        "Tokyo": {"temp": 22, "condition": "Partly cloudy", "humidity": 65},
        "New York": {"temp": 18, "condition": "Rainy", "humidity": 80},
        "London": {"temp": 15, "condition": "Foggy", "humidity": 75},
        "Paris": {"temp": 20, "condition": "Sunny", "humidity": 55},
        "Sydney": {"temp": 25, "condition": "Clear", "humidity": 50},
        "Singapore": {"temp": 30, "condition": "Hot and humid", "humidity": 85},
        "San Francisco": {"temp": 16, "condition": "Partly cloudy", "humidity": 70},
    }

    # Normalize city name for matching
    city_normalized = city.strip()

    # Try to find matching city (case-insensitive)
    for known_city, data in weather_data.items():
        if known_city.lower() == city_normalized.lower():
            return (
                f"Weather in {known_city}: {data['condition']}, "
                f"{data['temp']}°C, {data['humidity']}% humidity"
            )

    # City not found in our mock data
    return f"Weather data not available for {city}. Available cities: {', '.join(weather_data.keys())}"


# =============================================================================
# TOOL 2: Time/Timezone Tool
# =============================================================================

@tool
def get_time(city: str) -> str:
    """Get current time for a city.

    Args:
        city: The name of the city to get time for

    Returns:
        Current local time and timezone information
    """
    # Map cities to their timezones
    # Using Python 3.10+ zoneinfo for timezone handling
    city_timezones = {
        "Tokyo": "Asia/Tokyo",
        "New York": "America/New_York",
        "London": "Europe/London",
        "Paris": "Europe/Paris",
        "Sydney": "Australia/Sydney",
        "Singapore": "Asia/Singapore",
        "San Francisco": "America/Los_Angeles",
    }

    # Normalize city name
    city_normalized = city.strip()

    # Try to find matching city (case-insensitive)
    for known_city, tz_name in city_timezones.items():
        if known_city.lower() == city_normalized.lower():
            try:
                # Get current time in the city's timezone
                tz = ZoneInfo(tz_name)
                local_time = datetime.now(tz)

                # Format the time nicely
                time_str = local_time.strftime("%I:%M %p")
                date_str = local_time.strftime("%A, %B %d, %Y")

                return (
                    f"Current time in {known_city}: {time_str} ({tz_name})\n"
                    f"Date: {date_str}"
                )
            except Exception as e:
                return f"Error getting time for {known_city}: {str(e)}"

    # City not found in our data
    return f"Time data not available for {city}. Available cities: {', '.join(city_timezones.keys())}"


# =============================================================================
# TOOL 3: Unit Converter Tool
# =============================================================================

@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between different units of measurement.

    Supports temperature (C, F, K), distance (m, km, mi, ft), and weight (kg, lb, oz).

    Args:
        value: The numeric value to convert
        from_unit: The source unit (e.g., 'C', 'F', 'km', 'kg')
        to_unit: The target unit (e.g., 'F', 'C', 'mi', 'lb')

    Returns:
        Converted value with units
    """
    # Normalize units to lowercase
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    # Temperature conversions
    if from_unit in ['c', 'celsius', 'f', 'fahrenheit', 'k', 'kelvin']:
        # Convert to Celsius first
        if from_unit in ['f', 'fahrenheit']:
            celsius = (value - 32) * 5/9
        elif from_unit in ['k', 'kelvin']:
            celsius = value - 273.15
        else:  # Already Celsius
            celsius = value

        # Convert from Celsius to target
        if to_unit in ['f', 'fahrenheit']:
            result = celsius * 9/5 + 32
            return f"{value}°{from_unit.upper()} = {result:.1f}°F"
        elif to_unit in ['k', 'kelvin']:
            result = celsius + 273.15
            return f"{value}°{from_unit.upper()} = {result:.1f}K"
        elif to_unit in ['c', 'celsius']:
            return f"{value}°{from_unit.upper()} = {celsius:.1f}°C"
        else:
            return f"Unknown temperature unit: {to_unit}. Use C, F, or K."

    # Distance conversions
    elif from_unit in ['m', 'meter', 'meters', 'km', 'kilometer', 'kilometers',
                       'mi', 'mile', 'miles', 'ft', 'feet', 'foot']:
        # Convert to meters first
        if from_unit in ['km', 'kilometer', 'kilometers']:
            meters = value * 1000
        elif from_unit in ['mi', 'mile', 'miles']:
            meters = value * 1609.34
        elif from_unit in ['ft', 'feet', 'foot']:
            meters = value * 0.3048
        else:  # Already meters
            meters = value

        # Convert from meters to target
        if to_unit in ['km', 'kilometer', 'kilometers']:
            result = meters / 1000
            return f"{value} {from_unit} = {result:.2f} km"
        elif to_unit in ['mi', 'mile', 'miles']:
            result = meters / 1609.34
            return f"{value} {from_unit} = {result:.2f} miles"
        elif to_unit in ['ft', 'feet', 'foot']:
            result = meters / 0.3048
            return f"{value} {from_unit} = {result:.1f} feet"
        elif to_unit in ['m', 'meter', 'meters']:
            return f"{value} {from_unit} = {meters:.2f} meters"
        else:
            return f"Unknown distance unit: {to_unit}. Use m, km, mi, or ft."

    # Weight conversions
    elif from_unit in ['kg', 'kilogram', 'kilograms', 'lb', 'pound', 'pounds',
                       'oz', 'ounce', 'ounces']:
        # Convert to kilograms first
        if from_unit in ['lb', 'pound', 'pounds']:
            kg = value * 0.453592
        elif from_unit in ['oz', 'ounce', 'ounces']:
            kg = value * 0.0283495
        else:  # Already kg
            kg = value

        # Convert from kg to target
        if to_unit in ['lb', 'pound', 'pounds']:
            result = kg / 0.453592
            return f"{value} {from_unit} = {result:.2f} lb"
        elif to_unit in ['oz', 'ounce', 'ounces']:
            result = kg / 0.0283495
            return f"{value} {from_unit} = {result:.2f} oz"
        elif to_unit in ['kg', 'kilogram', 'kilograms']:
            return f"{value} {from_unit} = {kg:.2f} kg"
        else:
            return f"Unknown weight unit: {to_unit}. Use kg, lb, or oz."

    else:
        return (
            f"Unknown unit type: {from_unit}. Supported categories:\n"
            "- Temperature: C, F, K\n"
            "- Distance: m, km, mi, ft\n"
            "- Weight: kg, lb, oz"
        )


# =============================================================================
# EXAMPLES: Tool Selection and Orchestration
# =============================================================================

def part1_single_tool_selection():
    """Demonstrate agent selecting the appropriate tool based on query."""
    print("\n" + "="*70)
    print("Part 1: Single Tool Selection")
    print("="*70)
    print("Concept: Agent automatically selects the right tool based on query intent")
    print()

    working_model = create_working_model("tool selection")
    if not working_model:
        print("⚠️  No working model available - skipping examples")
        return

    # Create agent with all three tools
    agent = Agent(
        model=working_model,
        tools=[get_weather, get_time, convert_units],
        system_prompt="You are a helpful assistant with access to weather, time, and unit conversion tools."
    )

    # Test queries that should each use exactly one tool
    queries = [
        "What's the weather in Tokyo?",
        "What time is it in New York?",
        "Convert 100 km to miles",
    ]

    for query in queries:
        print(f"\n📝 Query: {query}")
        agent(query)


def part2_tool_chaining():
    """Demonstrate agent using multiple tools in one response."""
    print("\n" + "="*70)
    print("Part 2: Tool Chaining")
    print("="*70)
    print("Concept: Agent can use multiple tools in a single response")
    print()

    working_model = create_working_model("tool chaining")
    if not working_model:
        print("⚠️  No working model available - skipping examples")
        return

    agent = Agent(
        model=working_model,
        tools=[get_weather, get_time, convert_units],
        system_prompt="You are a helpful assistant. Use multiple tools when needed to give complete answers."
    )

    # Queries that benefit from using multiple tools
    queries = [
        "What's the weather and time in London?",
        "Tell me about Paris - weather, time, and convert 20°C to Fahrenheit",
    ]

    for query in queries:
        print(f"\n📝 Query: {query}")
        agent(query)


def part3_context_aware_selection():
    """Demonstrate agent using context from conversation."""
    print("\n" + "="*70)
    print("Part 3: Context-Aware Tool Selection")
    print("="*70)
    print("Concept: Agent remembers context and applies it to ambiguous follow-ups")
    print()

    working_model = create_working_model("context awareness")
    if not working_model:
        print("⚠️  No working model available - skipping examples")
        return

    agent = Agent(
        model=working_model,
        tools=[get_weather, get_time, convert_units],
        system_prompt="You are a helpful assistant. Remember context from previous messages."
    )

    # Multi-turn conversation with ambiguous follow-up
    print("\n📝 Turn 1: What's the weather in Tokyo?")
    agent("What's the weather in Tokyo?")

    print("\n📝 Turn 2: What about Sydney? (ambiguous - should infer 'weather')")
    agent("What about Sydney?")

    print("\n📝 Turn 3: And the time there? (should know 'there' = Sydney)")
    agent("And the time there?")


def part4_error_handling():
    """Demonstrate tools handling errors gracefully."""
    print("\n" + "="*70)
    print("Part 4: Error Handling")
    print("="*70)
    print("Concept: Tools handle invalid inputs gracefully with helpful messages")
    print()

    working_model = create_working_model("error handling")
    if not working_model:
        print("⚠️  No working model available - skipping examples")
        return

    agent = Agent(
        model=working_model,
        tools=[get_weather, get_time, convert_units],
        system_prompt="You are a helpful assistant. When tools return errors, explain them clearly."
    )

    # Test error cases
    queries = [
        "What's the weather in Atlantis?",  # Non-existent city
        "Convert 100 meters to bananas",     # Invalid unit
    ]

    for query in queries:
        print(f"\n📝 Query: {query}")
        agent(query)


def part5_combined_reasoning():
    """Demonstrate complex queries requiring reasoning and multiple tool calls."""
    print("\n" + "="*70)
    print("Part 5: Combined Reasoning with Multiple Tools")
    print("="*70)
    print("Concept: Agent combines tool results with reasoning to answer complex queries")
    print()

    working_model = create_working_model("combined reasoning")
    if not working_model:
        print("⚠️  No working model available - skipping examples")
        return

    agent = Agent(
        model=working_model,
        tools=[get_weather, get_time, convert_units],
        system_prompt="You are a helpful travel assistant. Combine tool information with reasoning."
    )

    # Complex query requiring multiple tools and reasoning
    query = (
        "I'm in New York and want to call someone in Singapore. "
        "What's the weather like there, what time is it, and is it a good time to call?"
    )

    print(f"\n📝 Query: {query}")
    agent(query)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Run all examples demonstrating multiple tool usage."""
    load_environment()
    check_api_keys()

    print("\n" + "="*70)
    print("LESSON 3: MULTIPLE TOOLS & CONTEXT")
    print("="*70)
    print("Learn how agents select and orchestrate multiple tools intelligently")
    print()

    # Run all demonstration parts
    part1_single_tool_selection()
    part2_tool_chaining()
    part3_context_aware_selection()
    part4_error_handling()
    part5_combined_reasoning()

    # Success criteria
    print("\n" + "="*70)
    print("✅ SUCCESS CRITERIA")
    print("="*70)
    print("""
After completing this lesson, you should have seen:

□ Agent selects appropriate tool based on query intent
  - Weather queries use get_weather
  - Time queries use get_time
  - Conversion queries use convert_units

□ Can chain multiple tools in one response seamlessly
  - "Weather and time in London" uses both tools
  - Results are combined coherently

□ Handles ambiguous requests using conversation context
  - "What about Sydney?" infers weather from previous question
  - "And the time there?" knows "there" refers to Sydney

□ Combines tool results into coherent responses
  - Tool outputs are integrated into natural language
  - Agent adds reasoning and interpretation

□ Tool selection is accurate even with overlapping capabilities
  - Doesn't confuse temperature conversion with weather
  - Selects correct tool even when multiple could apply
    """)

    # Experiments to try
    print("\n" + "="*70)
    print("🧪 EXPERIMENTS TO TRY")
    print("="*70)
    print()
    print("   Setup: Copy this lesson to experiments/ before tinkering:")
    print("      cp lesson_03_multiple_tools.py experiments/my_multi_tool_variant.py")
    print("      uv run python experiments/my_multi_tool_variant.py")
    print()
    print("   Exercises:")
    print("   1. Multi-city comparison:")
    print("      'Compare weather between Tokyo, New York, and London'")
    print()
    print("   2. Complex unit conversion chains:")
    print("      'Convert 5 km to miles, then to feet'")
    print()
    print("   3. Time zone calculations:")
    print("      'If it's 3pm in San Francisco, what time is it in Singapore?'")
    print()
    print("   4. Add a new tool:")
    print("      - Create currency converter")
    print("      - Add to tools list")
    print("      - Test tool orchestration with 4 tools")
    print()
    print("   5. Test ambiguous context:")
    print("      - Start conversation about Paris")
    print("      - Ask follow-ups without mentioning city name")
    print("      - See if agent maintains context")
    print()
    print("   6. Error recovery:")
    print("      - Give intentionally bad inputs")
    print("      - See how agent explains errors")
    print("      - Test if agent suggests corrections")

    print("\n" + "="*70)
    print("Next: Lesson 4 - Stateful Tools with Classes")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
