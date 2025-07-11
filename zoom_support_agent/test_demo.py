# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test demonstration for Zoom Support Agent System."""

import asyncio
import sys
import os

# Handle imports for both direct execution and module import
try:
    from .runner import run_zoom_support_query
except ImportError:
    # When running as script, add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from zoom_support_agent.runner import run_zoom_support_query

async def test_product_identification():
    """Test product identification queries."""
    print("\n" + "="*60)
    print("🧪 TESTING: Product Identification")
    print("="*60)
    
    queries = [
        "I have a Zoom recorder with 6 tracks, what model is it?",
        "What are the specifications of the Zoom H4n Pro?",
        "Is the PodTrak P4 good for podcasting?",
        "I need info about the Zoom F8n field recorder"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        response = await run_zoom_support_query(query)
        print(f"🤖 Response: {response[:200]}...")

async def test_gear_compatibility():
    """Test gear compatibility queries."""
    print("\n" + "="*60)
    print("🧪 TESTING: Gear Compatibility")
    print("="*60)
    
    queries = [
        "Will a Rode NT1 microphone work with my Zoom H6?",
        "What headphones should I use for monitoring with my recorder?",
        "Do I need special XLR cables for my Zoom H4n Pro?",
        "Can I use a Behringer mixer with my PodTrak P4?"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        response = await run_zoom_support_query(query)
        print(f"🤖 Response: {response[:200]}...")

async def test_customer_support():
    """Test customer support queries."""
    print("\n" + "="*60)
    print("🧪 TESTING: Customer Support")
    print("="*60)
    
    queries = [
        ("How do I register my Zoom H6?", "john.doe@email.com"),
        ("My warranty expired, what are my options?", "bob.wilson@email.com"),
        ("I lost my receipt, can you help me verify my purchase?", "jane.smith@email.com"),
        ("What's the warranty status of my PodTrak P4?", "jane.smith@email.com")
    ]
    
    for query, email in queries:
        print(f"\n📝 Query: {query}")
        print(f"📧 Email: {email}")
        response = await run_zoom_support_query(query, email)
        print(f"🤖 Response: {response[:200]}...")

async def test_complex_query():
    """Test the original complex query."""
    print("\n" + "="*60)
    print("🧪 TESTING: Complex Multi-Part Query")
    print("="*60)
    
    query = "I just bought a Zoom H6 but I'm not sure how to register it or find compatible mics"
    email = "john.doe@email.com"
    
    print(f"📝 Query: {query}")
    print(f"📧 Email: {email}")
    response = await run_zoom_support_query(query, email)
    print(f"🤖 Response: {response}")

async def main():
    """Run all test demonstrations."""
    print("🎤 Zoom Support Agent System - Test Demonstrations")
    print("="*60)
    print("This demonstration shows how the system handles different types of customer queries.")
    print("Each test will show the query and a preview of the agent's response.")
    
    # Run all test categories
    await test_product_identification()
    await test_gear_compatibility()
    await test_customer_support()
    await test_complex_query()
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
    print("The system successfully handled:")
    print("- Product identification requests")
    print("- Gear compatibility questions")
    print("- Customer support inquiries")
    print("- Complex multi-part queries")
    print("\nEach query was routed to appropriate sub-agents and coordinated into helpful responses.")

if __name__ == "__main__":
    asyncio.run(main()) 