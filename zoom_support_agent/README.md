# Zoom Support Agent System

A comprehensive customer service agent system for Zoom products using Google's Agent Development Kit (ADK). This system coordinates between specialized sub-agents to provide complete customer support for Zoom audio equipment.

## 🎯 Overview

The Zoom Support Agent System is designed to handle customer service requests by routing them to appropriate specialists:

- **Product Identification**: Identifies Zoom products and provides specifications
- **Gear Compatibility**: Searches for compatible third-party equipment and accessories  
- **Customer Support**: Handles warranty, registration, and purchase verification

## 🏗️ Architecture

```
zoom_support_agent/
├── __init__.py                 # Package initialization
├── agent.py                    # Main coordinator agent
├── prompt.py                   # Agent instructions and prompts
├── runner.py                   # Main orchestration runner
├── README.md                   # This documentation
└── sub_agents/                 # Specialized sub-agents
    ├── __init__.py
    ├── zoom_product_search.py      # Product identification
    ├── third_party_websearch.py    # Gear compatibility
    └── zoom_customer_specialist.py # Customer support
```

## 🤖 Agents

### Root Agent: `zoom_support_agent`
- **Purpose**: Analyzes customer requests and routes to appropriate specialists
- **Model**: Gemini 2.0 Flash
- **Tools**: Coordinates between all sub-agents

### Sub-Agent 1: `zoom_product_search`
- **Purpose**: Identifies Zoom products and provides detailed specifications
- **Tools**: `get_product_info()` - Returns product details and features
- **Supported Products**: H6, H4n Pro, PodTrak P4, F8n, Q2n, R8

### Sub-Agent 2: `third_party_websearch` 
- **Purpose**: Simulates searching for compatible gear and accessories
- **Tools**: `search_compatible_gear()` - Returns compatibility recommendations
- **Sources**: Gearspace, Reddit, Sweetwater (simulated)

### Sub-Agent 3: `zoom_customer_specialist`
- **Purpose**: Handles warranty, registration, and purchase verification
- **Tools**: 
  - `verify_purchase()` - Checks purchase records and warranty status
  - `handle_registration()` - Processes product registration
  - `check_warranty_status()` - Provides warranty information

## 🚀 Quick Start

### Prerequisites
- Google Cloud Project with Vertex AI enabled
- Google ADK installed: `pip install google-adk`
- Proper authentication configured

### Environment Setup
```bash
export GOOGLE_GENAI_USE_VERTEXAI="True"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
```

### Running the System
```python
import asyncio
from zoom_support_agent import run_zoom_support_query

# Sample customer query
query = "I just bought a Zoom H6 but I'm not sure how to register it or find compatible mics"
email = "customer@example.com"

# Run the query
response = await run_zoom_support_query(query, email)
print(response)
```

### Direct Execution
```bash
cd zoom_support_agent
python runner.py
```

## 📋 Sample Queries

The system handles various customer service scenarios:

### Product Identification
- "I have a Zoom recorder but don't know the model"
- "What are the specs of the H6?"
- "Is the PodTrak P4 good for podcasting?"

### Gear Compatibility
- "Will a Rode NT1 work with my H6?"
- "What headphones should I use for monitoring?"
- "Do I need special cables for my Zoom recorder?"

### Customer Support
- "How do I register my Zoom H6?"
- "My warranty expired, what are my options?"
- "I lost my receipt, can you help?"

## 🔧 Configuration

### Model Configuration
The system uses Gemini 2.0 Flash by default. To change models:

```python
# In agent.py
MODEL = "gemini-1.5-pro"  # Alternative model
```

### Mock Data
The system includes mock customer data for testing:

```python
# In zoom_customer_specialist.py
MOCK_CUSTOMERS = {
    "john.doe@email.com": {
        "name": "John Doe",
        "purchases": [...]
    }
}
```

## 🧪 Testing

### Unit Tests
```bash
# Run tests for individual agents
python -m pytest tests/test_product_search.py
python -m pytest tests/test_customer_specialist.py
```

### Integration Tests
```bash
# Test the full system
python -m pytest tests/test_integration.py
```

## 📊 State Management

The system maintains session state across agent interactions:

```python
session_state = {
    "customer_email": "customer@example.com",
    "conversation_history": [],
    "current_request": "user query",
    "last_product_query": "H6",
    "last_compatibility_query": "microphone compatibility",
    "last_verification_request": {...}
}
```

## 🔄 Workflow

1. **Customer Query**: User submits a question or request
2. **Analysis**: Root agent analyzes the request type
3. **Routing**: Request is routed to appropriate sub-agent(s)
4. **Processing**: Sub-agent(s) process the request using specialized tools
5. **Coordination**: Root agent combines responses from sub-agents
6. **Response**: Final coordinated response is returned to customer

## 🛠️ Extending the System

### Adding New Products
1. Update `get_product_info()` in `zoom_product_search.py`
2. Add product specifications and features
3. Update prompts in `prompt.py`

### Adding New Tools
1. Create new tool function in appropriate sub-agent
2. Add tool to agent's tools list
3. Update agent instructions if needed

### Adding New Sub-Agents
1. Create new agent file in `sub_agents/`
2. Define agent with tools and instructions
3. Add to root agent's tools list in `agent.py`

## 📝 License

Copyright 2025 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add proper error handling and logging
3. Include docstrings for all functions
4. Update tests for new functionality
5. Maintain backward compatibility

## 📞 Support

For technical support or questions about this system:
- Email: support@zoom-na.com
- Phone: 1-800-662-6266
- Hours: Monday-Friday, 9AM-6PM EST 