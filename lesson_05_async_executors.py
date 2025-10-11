#!/usr/bin/env python3
"""
Lesson 5: Async Streaming, Executors & Multi-modal

Master async operations, streaming, tool execution strategies, and multi-modal content:
- Async tool definition with async def and await
- Streaming progress updates with yield in async tools
- Using agent.stream_async() for real-time responses
- ConcurrentToolExecutor for parallel tool execution (default)
- SequentialToolExecutor for ordered tool execution
- Multi-modal content (images, PDFs, documents)

Learning Objectives:
□ Create async tools with yield for streaming progress
□ Use stream_async() to consume real-time updates
□ Compare ConcurrentToolExecutor vs SequentialToolExecutor performance
□ Process multi-modal content (images, PDFs) in agent messages
□ Understand when to use concurrent vs sequential execution
"""

import asyncio
import time
from datetime import datetime

from strands import Agent, tool
from strands.tools.executors import ConcurrentToolExecutor, SequentialToolExecutor

from lesson_utils import (
    load_environment,
    create_working_model,
    check_api_keys,
    print_troubleshooting,
)


# ============================================================================
# Part 1: Async Tools with Streaming Progress
# ============================================================================
# Async tools can yield intermediate results to provide real-time progress updates.
# Each yielded value becomes a streaming event.
# Reference: strandsagents.com/latest/.../tools/python-tools/


@tool
async def process_dataset(records: int) -> str:
    """Process records with progress updates."""
    start = datetime.now()

    for i in range(1, records + 1):
        await asyncio.sleep(0.1)  # Simulate processing time
        if i % 10 == 0:
            elapsed = (datetime.now() - start).total_seconds()
            yield f"Processed {i}/{records} records in {elapsed:.1f}s"

    total_time = (datetime.now() - start).total_seconds()
    yield f"✓ Completed {records} records in {total_time:.1f}s"


@tool
async def download_file(url: str, size_mb: int = 10) -> str:
    """Simulate downloading a file with progress updates."""
    chunks = 10
    chunk_size = size_mb / chunks

    yield f"Starting download: {url} ({size_mb}MB)"

    for i in range(1, chunks + 1):
        await asyncio.sleep(0.2)  # Simulate download time
        progress = (i / chunks) * 100
        downloaded = chunk_size * i
        yield f"Downloaded {downloaded:.1f}MB / {size_mb}MB ({progress:.0f}%)"

    yield f"✓ Download complete: {url}"


async def part1_async_streaming():
    """Demonstrate async tools with streaming progress."""
    print("\n" + "=" * 70)
    print("PART 1: Async Tools with Streaming Progress")
    print("=" * 70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Create agent with async streaming tools
    agent = Agent(
        model=model,
        tools=[process_dataset, download_file],
        system_prompt="You are a helpful assistant with data processing capabilities.",
    )

    print("\n1. Streaming progress from async tools:")
    print("   Using agent.stream_async() to get real-time updates")

    async for event in agent.stream_async("Process 30 records"):
        # Check for tool stream events (progress updates)
        if tool_stream := event.get("tool_stream_event"):
            if update := tool_stream.get("data"):
                print(f"   📊 Progress: {update}")

        # Check for final text response
        if "data" in event and not event.get("tool_stream_event"):
            print(f"   🤖 Agent: {event['data']}", end="")

    print("\n\n2. Download simulation with progress:")
    async for event in agent.stream_async("Download a 5MB file from example.com"):
        if tool_stream := event.get("tool_stream_event"):
            if update := tool_stream.get("data"):
                print(f"   📥 {update}")

        if "data" in event and not event.get("tool_stream_event"):
            print(f"   🤖 Agent: {event['data']}", end="")


# ============================================================================
# Part 2: ConcurrentToolExecutor (Default)
# ============================================================================
# ConcurrentToolExecutor executes multiple tools in parallel when the
# LLM requests multiple tools in a single response.
# Reference: strandsagents.com/latest/.../tools/executors/


@tool
async def get_weather(city: str) -> str:
    """Get weather forecast for a city."""
    await asyncio.sleep(1.0)  # Simulate API call
    return f"Weather in {city}: Sunny, 72°F"


@tool
async def get_time(city: str) -> str:
    """Get current time in a city."""
    await asyncio.sleep(1.0)  # Simulate API call
    return f"Time in {city}: 2:30 PM"


@tool
async def get_population(city: str) -> str:
    """Get population of a city."""
    await asyncio.sleep(1.0)  # Simulate database query
    return f"Population of {city}: ~1.5 million"


async def part2_concurrent_executor():
    """Demonstrate ConcurrentToolExecutor for parallel execution."""
    print("\n" + "=" * 70)
    print("PART 2: ConcurrentToolExecutor (Parallel Execution)")
    print("=" * 70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # ConcurrentToolExecutor is the default, but we can specify it explicitly
    agent = Agent(
        model=model,
        tool_executor=ConcurrentToolExecutor(),
        tools=[get_weather, get_time, get_population],
        system_prompt="Use tools to answer user questions about cities.",
    )

    print("\n1. Concurrent execution (tools run in parallel):")
    print("   Requesting multiple pieces of information...")

    start_time = time.time()
    response = await agent.invoke_async(
        "What's the weather, time, and population in Seattle?"
    )
    elapsed = time.time() - start_time

    print(f"\n   Agent: {response}")
    print(f"\n   ⚡ Total time: {elapsed:.2f}s")
    print(
        "   💡 With concurrent execution, "
        "3 tools (each taking 1s) complete in ~1s!"
    )


# ============================================================================
# Part 3: SequentialToolExecutor (Ordered Execution)
# ============================================================================
# SequentialToolExecutor executes tools one after another in the order
# specified by the LLM. Useful for dependent operations.


@tool
async def take_screenshot(filename: str) -> str:
    """Take a screenshot and save to file."""
    await asyncio.sleep(0.5)  # Simulate screenshot capture
    return f"Screenshot saved to {filename}"


@tool
async def send_email(recipient: str, attachment: str) -> str:
    """Send an email with an attachment."""
    await asyncio.sleep(0.5)  # Simulate email sending
    return f"Email sent to {recipient} with attachment: {attachment}"


@tool
async def compress_file(filename: str) -> str:
    """Compress a file to save space."""
    await asyncio.sleep(0.5)  # Simulate compression
    compressed = filename.replace(".png", ".zip")
    return f"Compressed {filename} to {compressed}"


async def part3_sequential_executor():
    """Demonstrate SequentialToolExecutor for ordered execution."""
    print("\n" + "=" * 70)
    print("PART 3: SequentialToolExecutor (Ordered Execution)")
    print("=" * 70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Use SequentialToolExecutor for dependent operations
    agent = Agent(
        model=model,
        tool_executor=SequentialToolExecutor(),
        tools=[take_screenshot, compress_file, send_email],
        system_prompt="Execute tasks in the correct order for dependent operations.",
    )

    print("\n1. Sequential execution (tools run in order):")
    print("   Task: Take screenshot → Compress → Email")

    start_time = time.time()
    response = await agent.invoke_async(
        "Take a screenshot named report.png, compress it, "
        "then email the compressed file to boss@company.com"
    )
    elapsed = time.time() - start_time

    print(f"\n   Agent: {response}")
    print(f"\n   ⏱️  Total time: {elapsed:.2f}s")
    print(
        "   💡 With sequential execution, "
        "operations happen in the correct order!"
    )


# ============================================================================
# Part 4: Performance Comparison
# ============================================================================
# Compare concurrent vs sequential execution performance.


@tool
async def fetch_data(source: str) -> str:
    """Fetch data from a source (simulated)."""
    await asyncio.sleep(1.0)  # Simulate network delay
    return f"Data from {source}: [sample data]"


async def part4_performance_comparison():
    """Compare concurrent vs sequential executor performance."""
    print("\n" + "=" * 70)
    print("PART 4: Performance Comparison")
    print("=" * 70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Test with ConcurrentToolExecutor
    print("\n1. Testing ConcurrentToolExecutor:")
    concurrent_agent = Agent(
        model=model,
        tool_executor=ConcurrentToolExecutor(),
        tools=[fetch_data],
        system_prompt="Fetch data from multiple sources.",
    )

    start = time.time()
    await concurrent_agent.invoke_async("Fetch data from API-A, API-B, and API-C")
    concurrent_time = time.time() - start
    print(f"   ⚡ Concurrent time: {concurrent_time:.2f}s")

    # Test with SequentialToolExecutor
    print("\n2. Testing SequentialToolExecutor:")
    sequential_agent = Agent(
        model=model,
        tool_executor=SequentialToolExecutor(),
        tools=[fetch_data],
        system_prompt="Fetch data from multiple sources.",
    )

    start = time.time()
    await sequential_agent.invoke_async("Fetch data from API-A, API-B, and API-C")
    sequential_time = time.time() - start
    print(f"   ⏱️  Sequential time: {sequential_time:.2f}s")

    # Show comparison
    print("\n3. Performance Summary:")
    print(f"   Concurrent: {concurrent_time:.2f}s")
    print(f"   Sequential: {sequential_time:.2f}s")
    speedup = sequential_time / concurrent_time if concurrent_time > 0 else 1
    print(
        f"   Speedup: {speedup:.2f}x faster with concurrent execution!"
    )


# ============================================================================
# Part 5: Multi-modal Content (Images, PDFs)
# ============================================================================
# Agents can process multi-modal content including images and PDFs.
# We'll create a sample receipt image and actually analyze it with agents.
# Reference: https://strandsagents.com/latest/documentation/docs/examples/python/multimodal/


def create_sample_receipt():
    """Create a sample receipt image for demonstration."""
    from PIL import Image, ImageDraw, ImageFont

    # Create a white image
    width, height = 400, 600
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    # Try to use a better font, fall back to default if not available
    try:
        font_large = ImageFont.truetype("Arial.ttf", 24)
        font_medium = ImageFont.truetype("Arial.ttf", 18)
        font_small = ImageFont.truetype("Arial.ttf", 14)
    except IOError:
        # Use default font if Arial not available
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw receipt content
    y = 20
    draw.text((width // 2 - 70, y), "ACME GROCERY", fill="black", font=font_large)
    y += 40
    draw.text((width // 2 - 60, y), "123 Main Street", fill="black", font=font_small)
    y += 25
    draw.text(
        (width // 2 - 80, y), "Springfield, IL 62701", fill="black", font=font_small
    )
    y += 40
    draw.line([(20, y), (width - 20, y)], fill="black", width=2)
    y += 20

    # Receipt details
    draw.text((20, y), "Receipt #: 2025-001234", fill="black", font=font_small)
    y += 25
    draw.text((20, y), "Date: October 11, 2025", fill="black", font=font_small)
    y += 25
    draw.text((20, y), "Time: 14:32 PM", fill="black", font=font_small)
    y += 40
    draw.line([(20, y), (width - 20, y)], fill="black", width=1)
    y += 20

    # Line items
    items = [
        ("Organic Apples (2 lbs)", "$5.99"),
        ("Whole Wheat Bread", "$3.49"),
        ("Free-Range Eggs (12)", "$4.99"),
        ("Almond Milk (1 gal)", "$4.29"),
        ("Fresh Salmon (1 lb)", "$12.99"),
        ("Mixed Greens", "$3.49"),
    ]

    for item, price in items:
        draw.text((20, y), item, fill="black", font=font_small)
        draw.text((width - 80, y), price, fill="black", font=font_small)
        y += 25

    y += 10
    draw.line([(20, y), (width - 20, y)], fill="black", width=1)
    y += 20

    # Subtotal, tax, total
    draw.text((20, y), "Subtotal:", fill="black", font=font_medium)
    draw.text((width - 85, y), "$35.24", fill="black", font=font_medium)
    y += 30
    draw.text((20, y), "Tax (8.5%):", fill="black", font=font_medium)
    draw.text((width - 80, y), "$3.00", fill="black", font=font_medium)
    y += 30
    draw.line([(20, y), (width - 20, y)], fill="black", width=2)
    y += 20
    draw.text((20, y), "TOTAL:", fill="black", font=font_large)
    draw.text((width - 90, y), "$38.24", fill="black", font=font_large)

    y += 60
    draw.line([(20, y), (width - 20, y)], fill="black", width=1)
    y += 20
    draw.text(
        (width // 2 - 90, y), "Thank you for shopping!", fill="black", font=font_small
    )

    # Save the image
    filename = "sample_receipt.png"
    img.save(filename)
    return filename


async def part5_multimodal_content():
    """Demonstrate ACTUAL multi-modal content processing with real images."""
    import os

    print("\n" + "=" * 70)
    print("PART 5: Multi-modal Content (Images, PDFs)")
    print("=" * 70)

    model = create_working_model()
    if not model:
        print_troubleshooting()
        return

    # Create sample receipt image
    print("\n📸 Creating sample receipt image for demonstration...")
    receipt_path = create_sample_receipt()
    print(f"   ✓ Created: {receipt_path}")

    # Read image as bytes for multi-modal message
    with open(receipt_path, "rb") as f:
        image_bytes = f.read()

    # Example 1: Document Analyzer with image in message
    # This works with both OpenAI and Anthropic models
    print("\n1. Document Analyzer Demo:")
    print("   Passing image directly in message (provider-agnostic)...")

    analyzer = Agent(
        model=model,
        system_prompt=(
            "You are a document analyzer. "
            "Analyze images and extract all visible text and key information."
        ),
    )

    print(f"   Analyzing {receipt_path}...\n")

    # Pass image directly in message using Bedrock Converse format
    # This format works with OpenAI, Anthropic, and other providers in Strands
    message = [
        {"text": "Analyze this receipt image and extract key information:"},
        {"image": {"format": "png", "source": {"bytes": image_bytes}}},
    ]

    response = await analyzer.invoke_async(message)

    print("\n   📄 Analysis Result:")
    print(f"   {response}")

    # Example 2: Receipt Extractor with structured extraction
    print("\n2. Receipt/Invoice Extractor Demo:")
    print("   Extracting structured financial data...")

    receipt_extractor = Agent(
        model=model,
        system_prompt=(
            "You are a receipt and invoice data extractor. "
            "Extract and format the following information:\n"
            "- Store name\n"
            "- Date and time\n"
            "- All line items with prices\n"
            "- Subtotal, tax, and total amounts\n"
            "Present the data in a clear, structured format."
        ),
    )

    print(f"   Extracting structured data from {receipt_path}...\n")

    message = [
        {"text": "Extract all financial data from this receipt:"},
        {"image": {"format": "png", "source": {"bytes": image_bytes}}},
    ]

    response = await receipt_extractor.invoke_async(message)

    print("\n   💰 Extracted Data:")
    print(f"   {response}")

    # Clean up
    print(f"\n🧹 Cleaning up: Removing {receipt_path}")
    os.remove(receipt_path)

    # Educational notes
    print("\n💡 Key Takeaways:")
    print("   ✓ Images passed directly in messages (provider-agnostic)")
    print("   ✓ Works with OpenAI, Anthropic, and other vision models")
    print("   ✓ Bedrock Converse format: {'image': {'format': 'png', ...}}")
    print("   ✓ Multi-modal enables OCR, document analysis, visual QA")
    print("\n   Multi-modal message format:")
    print("   message = [")
    print("       {'text': 'Describe this image'},")
    print("       {'image': {'format': 'png', 'source': {'bytes': img_bytes}}}")
    print("   ]")


# ============================================================================
# Main Function
# ============================================================================


async def async_main():
    """Run all async lesson examples."""
    print("\n" + "=" * 70)
    print("LESSON 5: Async Streaming, Executors & Multi-modal")
    print("=" * 70)
    print("\nThis lesson demonstrates:")
    print("- Async tools with streaming progress (yield)")
    print("- ConcurrentToolExecutor for parallel execution")
    print("- SequentialToolExecutor for ordered execution")
    print("- Performance comparison: concurrent vs sequential")
    print("- Multi-modal content (images, PDFs)")

    # Load environment and check API keys
    load_environment()
    check_api_keys()

    # Run all parts
    await part1_async_streaming()
    await part2_concurrent_executor()
    await part3_sequential_executor()
    await part4_performance_comparison()
    await part5_multimodal_content()

    # Success criteria
    print("\n" + "=" * 70)
    print("SUCCESS CRITERIA")
    print("=" * 70)
    print("✓ Async tools stream progress in real-time via yield")
    print("✓ ConcurrentToolExecutor runs tools in parallel")
    print("✓ SequentialToolExecutor runs tools in order")
    print("✓ Async tools show measurable speedup vs sequential")
    print("✓ Stream events are properly formatted and received")
    print("✓ Agent processes images (PNG, JPEG) correctly")
    print("✓ Multi-modal agents invoked with real receipt image")
    print("✓ Document analyzer and receipt extractor demonstrated")

    # Experiments to try
    print("\n🧪 Experiments to Try:")
    print("   ")
    print("   Setup: Copy this lesson to experiments/ before tinkering:")
    print("      cp lesson_05_async_executors.py experiments/my_variant.py")
    print("      uv run python experiments/my_variant.py")
    print("   ")
    print("   Exercises:")
    print(
        "   1. Process multiple files simultaneously "
        "and measure speedup with ConcurrentToolExecutor"
    )
    print("   2. Stream progress for a long-running operation (10+ seconds)")
    print(
        "   3. Compare performance: ConcurrentToolExecutor vs "
        "SequentialToolExecutor with timing"
    )
    print("   4. Build a chain of dependent tasks with SequentialToolExecutor")
    print(
        "   5. Create a tool that simulates API calls with varying delays"
    )
    print("   6. Extract data from different receipt/invoice images")
    print(
        "   7. Analyze documents with multiple images in one message"
    )
    print(
        "   8. Build a document classification tool using "
        "multi-modal inputs"
    )


def main():
    """Entry point that runs the async main function."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
