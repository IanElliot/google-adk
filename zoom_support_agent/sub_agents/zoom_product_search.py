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

"""Zoom Product Search Agent: Identifies and provides information about Zoom products."""

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from typing import Dict, Optional

from .. import prompt

MODEL = "gemini-2.0-flash"

def get_product_info(product_query: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Get detailed information about Zoom products.
    
    Args:
        product_query (str): User's description of the Zoom product
        tool_context (ToolContext): Provides access to session state
        
    Returns:
        Dict[str, str]: Product information and specifications
    """
    print(f"--- Tool: get_product_info called with query: '{product_query}' ---")
    
    # Track the product query in state
    tool_context.state["last_product_query"] = product_query
    print(f"--- Tool: Updated state 'last_product_query': {product_query} ---")
    
    query_lower = product_query.lower()
    
    # Zoom H6 - 6-track portable recorder
    if any(word in query_lower for word in ["h6", "6 track", "six track", "portable recorder"]):
        return {
            "status": "success",
            "product": "Zoom H6",
            "category": "Portable Recorder",
            "specifications": {
                "tracks": "6 simultaneous tracks",
                "inputs": "4 XLR/TRS combo inputs + 2 built-in mics",
                "sample_rate": "Up to 96kHz/24-bit",
                "battery": "AA batteries or USB power",
                "storage": "SD/SDHC cards up to 32GB",
                "weight": "0.6 lbs (270g)"
            },
            "features": [
                "Interchangeable mic capsules",
                "Built-in stereo mics",
                "USB audio interface mode",
                "Multi-track recording",
                "Phantom power (48V)"
            ],
            "price_range": "$399-499"
        }
    
    # Zoom H4n Pro - 4-track portable recorder
    elif any(word in query_lower for word in ["h4n", "h4n pro", "4 track", "four track"]):
        return {
            "status": "success",
            "product": "Zoom H4n Pro",
            "category": "Portable Recorder",
            "specifications": {
                "tracks": "4 simultaneous tracks",
                "inputs": "2 XLR/TRS combo inputs + 2 built-in mics",
                "sample_rate": "Up to 96kHz/24-bit",
                "battery": "AA batteries or USB power",
                "storage": "SD/SDHC cards up to 32GB",
                "weight": "0.5 lbs (230g)"
            },
            "features": [
                "Built-in stereo mics",
                "USB audio interface mode",
                "Multi-track recording",
                "Phantom power (48V)",
                "Compact design"
            ],
            "price_range": "$199-299"
        }
    
    # Zoom PodTrak P4 - Podcast recorder
    elif any(word in query_lower for word in ["podtrak", "p4", "podcast", "podcasting"]):
        return {
            "status": "success",
            "product": "Zoom PodTrak P4",
            "category": "Podcast Recorder",
            "specifications": {
                "tracks": "4 simultaneous tracks",
                "inputs": "4 XLR inputs",
                "sample_rate": "Up to 48kHz/24-bit",
                "battery": "AA batteries or USB power",
                "storage": "SD/SDHC cards up to 32GB",
                "weight": "0.7 lbs (320g)"
            },
            "features": [
                "Dedicated podcast features",
                "Sound pad for effects",
                "USB audio interface mode",
                "Multi-track recording",
                "Phantom power (48V)",
                "Headphone monitoring"
            ],
            "price_range": "$199-249"
        }
    
    # Zoom F8n - 8-track field recorder
    elif any(word in query_lower for word in ["f8n", "f8", "field recorder", "8 track"]):
        return {
            "status": "success",
            "product": "Zoom F8n",
            "category": "Field Recorder",
            "specifications": {
                "tracks": "8 simultaneous tracks",
                "inputs": "8 XLR/TRS combo inputs",
                "sample_rate": "Up to 192kHz/24-bit",
                "battery": "NP-F970 battery or DC power",
                "storage": "SD/SDHC/SDXC cards up to 512GB",
                "weight": "2.2 lbs (1kg)"
            },
            "features": [
                "Professional field recording",
                "Timecode support",
                "Dual SD card slots",
                "Advanced mixing features",
                "Phantom power (48V)",
                "Bluetooth control"
            ],
            "price_range": "$999-1299"
        }
    
    # Zoom Q2n - Video recorder
    elif any(word in query_lower for word in ["q2n", "video", "camera", "video recorder"]):
        return {
            "status": "success",
            "product": "Zoom Q2n",
            "category": "Video Recorder",
            "specifications": {
                "video": "1080p HD video",
                "audio": "2-channel audio recording",
                "inputs": "1 XLR input + built-in mics",
                "sample_rate": "Up to 96kHz/24-bit",
                "battery": "AA batteries or USB power",
                "storage": "SD/SDHC cards up to 32GB"
            },
            "features": [
                "HD video recording",
                "Built-in stereo mics",
                "USB audio interface mode",
                "Compact design",
                "Easy mounting options"
            ],
            "price_range": "$149-199"
        }
    
    # Zoom R8 - 8-track studio recorder
    elif any(word in query_lower for word in ["r8", "studio recorder", "8 track studio"]):
        return {
            "status": "success",
            "product": "Zoom R8",
            "category": "Studio Recorder",
            "specifications": {
                "tracks": "8 simultaneous tracks",
                "inputs": "2 XLR/TRS combo inputs + 6 virtual tracks",
                "sample_rate": "Up to 44.1kHz/16-bit",
                "power": "USB power or AC adapter",
                "storage": "SD/SDHC cards up to 32GB",
                "weight": "1.1 lbs (500g)"
            },
            "features": [
                "Built-in drum machine",
                "USB audio interface mode",
                "Multi-track recording",
                "Phantom power (48V)",
                "MIDI control",
                "Built-in effects"
            ],
            "price_range": "$299-399"
        }
    
    # Product not found
    else:
        return {
            "status": "error",
            "error_message": f"I couldn't identify a specific Zoom product from your description: '{product_query}'. Could you provide more details about the product you're referring to?",
            "suggestions": [
                "Zoom H6 (6-track portable recorder)",
                "Zoom H4n Pro (4-track portable recorder)", 
                "Zoom PodTrak P4 (podcast recorder)",
                "Zoom F8n (8-track field recorder)",
                "Zoom Q2n (video recorder)",
                "Zoom R8 (8-track studio recorder)"
            ]
        }

# Create the Zoom product search agent
zoom_product_search_agent = Agent(
    name="zoom_product_search",
    model=MODEL,
    description="Identifies Zoom products and provides detailed specifications and features.",
    instruction=prompt.ZOOM_PRODUCT_SEARCH_PROMPT,
    tools=[get_product_info]
) 