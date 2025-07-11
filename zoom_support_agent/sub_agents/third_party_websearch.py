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

"""Third Party Web Search Agent: Searches for compatible gear and accessories using Google Search."""

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import google_search
from typing import Dict, List

from .. import prompt

MODEL = "gemini-2.0-flash"

def search_compatible_gear(query: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Search for compatible gear and accessories using Google Search.
    
    Args:
        query (str): User's compatibility question or gear request
        tool_context (ToolContext): Provides access to session state
        
    Returns:
        Dict[str, str]: Compatibility information and recommendations from real web search
    """
    print(f"--- Tool: search_compatible_gear called with query: '{query}' ---")
    
    # Track the compatibility query in state
    tool_context.state["last_compatibility_query"] = query
    print(f"--- Tool: Updated state 'last_compatibility_query': {query} ---")
    
    # Enhance the search query for better results
    enhanced_query = f"{query} Zoom recorder compatibility reviews recommendations"
    
    try:
        # Use Google Search to find real information
        search_results = google_search(enhanced_query, tool_context)
        
        # Process and structure the search results
        if search_results and "results" in search_results:
            results = search_results["results"]
            
            # Extract key information from search results
            recommendations = []
            sources = []
            
            for result in results[:5]:  # Use top 5 results
                if "title" in result and "snippet" in result:
                    title = result["title"]
                    snippet = result["snippet"]
                    url = result.get("link", "")
                    
                    recommendations.append({
                        "title": title,
                        "summary": snippet,
                        "url": url
                    })
                    
                    # Extract domain for source tracking
                    if url:
                        domain = url.split("//")[-1].split("/")[0] if "//" in url else url
                        if domain not in sources:
                            sources.append(domain)
            
            return {
                "status": "success",
                "search_query": enhanced_query,
                "sources": sources,
                "recommendations": recommendations,
                "search_summary": f"Found {len(recommendations)} relevant results for '{query}'",
                "compatibility_notes": [
                    "Results are from real-time web search",
                    "Always verify compatibility with your specific Zoom model",
                    "Check manufacturer specifications for definitive answers"
                ]
            }
        else:
            return {
                "status": "error",
                "error_message": "No search results found",
                "search_query": enhanced_query,
                "suggestions": [
                    "Try a more specific search term",
                    "Check spelling and product names",
                    "Contact Zoom support for specific compatibility questions"
                ]
            }
            
    except Exception as e:
        print(f"--- Tool: Search error: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Search failed: {str(e)}",
            "search_query": enhanced_query,
            "fallback_info": {
                "general_compatibility": "Most professional audio gear is compatible with Zoom recorders",
                "connection_types": [
                    "XLR inputs accept most microphones",
                    "TRS inputs work with line-level sources",
                    "USB mode allows computer connection"
                ],
                "power_requirements": [
                    "Phantom power (48V) available on all inputs",
                    "Most gear works with Zoom's power output",
                    "Check power requirements for each device"
                ]
            },
            "suggestions": [
                "Try searching manually on Google",
                "Check manufacturer websites",
                "Contact Zoom support for assistance"
            ]
        }

# Create the third party web search agent
third_party_websearch_agent = Agent(
    name="third_party_websearch",
    model=MODEL,
    description="Searches for compatible gear and accessories using real-time web search.",
    instruction=prompt.THIRD_PARTY_WEBSEARCH_PROMPT,
    tools=[search_compatible_gear]
) 