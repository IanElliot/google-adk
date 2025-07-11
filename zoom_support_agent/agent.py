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

"""Zoom Support Agent: Customer service coordination for Zoom product support."""

import os
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.zoom_product_search import zoom_product_search_agent
from .sub_agents.third_party_websearch import third_party_websearch_agent
from .sub_agents.zoom_customer_specialist import zoom_customer_specialist_agent

# Configure Vertex AI
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
os.environ["GOOGLE_CLOUD_PROJECT"] = "adk-tutorial-464514"  # Replace with your project ID
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

MODEL = "gemini-2.0-flash"

# Main Zoom support coordinator agent
zoom_support_agent = Agent(
    name="zoom_support_agent",
    model=MODEL,
    description=(
        "analyzing customer service requests for Zoom products, "
        "diagnosing user needs and problems, routing requests "
        "to appropriate specialists, and coordinating responses "
        "from product search, third-party research, and customer support"
    ),
    instruction=prompt.ZOOM_SUPPORT_PROMPT,
    output_key="support_response",
    tools=[
        AgentTool(agent=zoom_product_search_agent),
        AgentTool(agent=third_party_websearch_agent),
        AgentTool(agent=zoom_customer_specialist_agent),
    ],
)

root_agent = zoom_support_agent 