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

"""Zoom Customer Specialist Agent: Handles warranty, registration, and purchase verification."""

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from typing import Dict, Optional
from datetime import datetime, timedelta
import random

from .. import prompt

MODEL = "gemini-2.0-flash"

# Mock customer database
MOCK_CUSTOMERS = {
    "john.doe@email.com": {
        "name": "John Doe",
        "purchases": [
            {
                "product": "Zoom H6",
                "serial_number": "H6-2024-001234",
                "purchase_date": "2024-01-15",
                "warranty_expires": "2027-01-15",
                "retailer": "Sweetwater",
                "order_number": "SW-12345"
            }
        ]
    },
    "jane.smith@email.com": {
        "name": "Jane Smith", 
        "purchases": [
            {
                "product": "Zoom PodTrak P4",
                "serial_number": "P4-2024-005678",
                "purchase_date": "2024-03-20",
                "warranty_expires": "2027-03-20",
                "retailer": "Amazon",
                "order_number": "AMZ-67890"
            }
        ]
    },
    "bob.wilson@email.com": {
        "name": "Bob Wilson",
        "purchases": [
            {
                "product": "Zoom H4n Pro",
                "serial_number": "H4N-2023-009876",
                "purchase_date": "2023-11-10",
                "warranty_expires": "2026-11-10",
                "retailer": "B&H Photo",
                "order_number": "BH-54321"
            }
        ]
    }
}

def verify_purchase(customer_email: str, product_query: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Verify customer purchase and provide registration/warranty information.
    
    Args:
        customer_email (str): Customer's email address
        product_query (str): Product description or serial number
        tool_context (ToolContext): Provides access to session state
        
    Returns:
        Dict[str, str]: Purchase verification and support information
    """
    print(f"--- Tool: verify_purchase called with email: '{customer_email}', product: '{product_query}' ---")
    
    # Track the verification request in state
    tool_context.state["last_verification_request"] = {
        "email": customer_email,
        "product": product_query
    }
    print(f"--- Tool: Updated state 'last_verification_request': {tool_context.state['last_verification_request']} ---")
    
    # Check if customer exists
    if customer_email not in MOCK_CUSTOMERS:
        return {
            "status": "error",
            "error_message": f"No purchase records found for email: {customer_email}",
            "suggestions": [
                "Please check your email address",
                "Contact support if you purchased with a different email",
                "Provide your order number for manual lookup"
            ],
            "contact_info": {
                "support_email": "support@zoom-na.com",
                "support_phone": "1-800-662-6266",
                "hours": "Monday-Friday, 9AM-6PM EST"
            }
        }
    
    customer = MOCK_CUSTOMERS[customer_email]
    product_query_lower = product_query.lower()
    
    # Find matching purchase
    matching_purchase = None
    for purchase in customer["purchases"]:
        if (product_query_lower in purchase["product"].lower() or 
            product_query_lower in purchase["serial_number"].lower()):
            matching_purchase = purchase
            break
    
    if not matching_purchase:
        return {
            "status": "error",
            "error_message": f"No matching product found for: {product_query}",
            "customer_products": [p["product"] for p in customer["purchases"]],
            "suggestions": [
                "Please provide the exact product name or serial number",
                "Check your purchase confirmation email",
                "Contact support for assistance"
            ]
        }
    
    # Check warranty status
    warranty_expires = datetime.strptime(matching_purchase["warranty_expires"], "%Y-%m-%d")
    warranty_status = "active" if warranty_expires > datetime.now() else "expired"
    days_remaining = (warranty_expires - datetime.now()).days if warranty_status == "active" else 0
    
    return {
        "status": "success",
        "customer_name": customer["name"],
        "purchase_details": matching_purchase,
        "warranty_status": {
            "status": warranty_status,
            "expires": matching_purchase["warranty_expires"],
            "days_remaining": days_remaining
        },
        "registration_info": {
            "registered": True,  # Mock: assume registered
            "registration_date": matching_purchase["purchase_date"],
            "next_steps": [
                "Product is already registered",
                "Warranty is active until " + matching_purchase["warranty_expires"],
                "Download latest firmware from zoom-na.com"
            ]
        },
        "support_options": {
            "warranty_service": "Available" if warranty_status == "active" else "Expired",
            "technical_support": "Available for all registered products",
            "contact_info": {
                "support_email": "support@zoom-na.com",
                "support_phone": "1-800-662-6266",
                "hours": "Monday-Friday, 9AM-6PM EST"
            }
        }
    }

def handle_registration(serial_number: str, customer_email: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Handle product registration requests.
    
    Args:
        serial_number (str): Product serial number
        customer_email (str): Customer's email address
        tool_context (ToolContext): Provides access to session state
        
    Returns:
        Dict[str, str]: Registration status and next steps
    """
    print(f"--- Tool: handle_registration called with serial: '{serial_number}', email: '{customer_email}' ---")
    
    # Track the registration request in state
    tool_context.state["last_registration_request"] = {
        "serial": serial_number,
        "email": customer_email
    }
    print(f"--- Tool: Updated state 'last_registration_request': {tool_context.state['last_registration_request']} ---")
    
    # Mock registration process
    registration_success = random.choice([True, True, True, False])  # 75% success rate
    
    if registration_success:
        return {
            "status": "success",
            "registration_status": "completed",
            "registration_date": datetime.now().strftime("%Y-%m-%d"),
            "next_steps": [
                "Product successfully registered",
                "Warranty activated for 3 years from purchase date",
                "Check your email for confirmation",
                "Download user manual and firmware from zoom-na.com"
            ],
            "benefits": [
                "Extended warranty coverage",
                "Priority technical support",
                "Firmware update notifications",
                "Product recall notifications"
            ],
            "contact_info": {
                "support_email": "support@zoom-na.com",
                "support_phone": "1-800-662-6266"
            }
        }
    else:
        return {
            "status": "error",
            "error_message": "Registration failed - serial number not found or already registered",
            "suggestions": [
                "Verify the serial number is correct",
                "Check if product was already registered",
                "Contact support for manual registration"
            ],
            "contact_info": {
                "support_email": "support@zoom-na.com",
                "support_phone": "1-800-662-6266"
            }
        }

def check_warranty_status(serial_number: str, tool_context: ToolContext) -> Dict[str, str]:
    """
    Check warranty status for a product.
    
    Args:
        serial_number (str): Product serial number
        tool_context (ToolContext): Provides access to session state
        
    Returns:
        Dict[str, str]: Warranty status and information
    """
    print(f"--- Tool: check_warranty_status called with serial: '{serial_number}' ---")
    
    # Track the warranty check in state
    tool_context.state["last_warranty_check"] = serial_number
    print(f"--- Tool: Updated state 'last_warranty_check': {serial_number} ---")
    
    # Mock warranty lookup
    warranty_data = {
        "H6-2024-001234": {
            "product": "Zoom H6",
            "purchase_date": "2024-01-15",
            "warranty_expires": "2027-01-15",
            "warranty_type": "3-year limited warranty",
            "coverage": "Parts and labor for manufacturing defects"
        },
        "P4-2024-005678": {
            "product": "Zoom PodTrak P4", 
            "purchase_date": "2024-03-20",
            "warranty_expires": "2027-03-20",
            "warranty_type": "3-year limited warranty",
            "coverage": "Parts and labor for manufacturing defects"
        },
        "H4N-2023-009876": {
            "product": "Zoom H4n Pro",
            "purchase_date": "2023-11-10", 
            "warranty_expires": "2026-11-10",
            "warranty_type": "3-year limited warranty",
            "coverage": "Parts and labor for manufacturing defects"
        }
    }
    
    if serial_number in warranty_data:
        warranty_info = warranty_data[serial_number]
        warranty_expires = datetime.strptime(warranty_info["warranty_expires"], "%Y-%m-%d")
        warranty_status = "active" if warranty_expires > datetime.now() else "expired"
        days_remaining = (warranty_expires - datetime.now()).days if warranty_status == "active" else 0
        
        return {
            "status": "success",
            "product": warranty_info["product"],
            "warranty_status": {
                "status": warranty_status,
                "type": warranty_info["warranty_type"],
                "purchase_date": warranty_info["purchase_date"],
                "expires": warranty_info["warranty_expires"],
                "days_remaining": days_remaining,
                "coverage": warranty_info["coverage"]
            },
            "next_steps": [
                "Warranty is " + warranty_status,
                "Contact support for service requests" if warranty_status == "active" else "Consider extended warranty options",
                "Keep original receipt for warranty claims"
            ],
            "contact_info": {
                "support_email": "support@zoom-na.com",
                "support_phone": "1-800-662-6266"
            }
        }
    else:
        return {
            "status": "error",
            "error_message": f"Serial number {serial_number} not found in warranty database",
            "suggestions": [
                "Verify the serial number is correct",
                "Contact support for manual warranty lookup",
                "Provide purchase receipt for verification"
            ],
            "contact_info": {
                "support_email": "support@zoom-na.com",
                "support_phone": "1-800-662-6266"
            }
        }

# Create the Zoom customer specialist agent
zoom_customer_specialist_agent = Agent(
    name="zoom_customer_specialist",
    model=MODEL,
    description="Handles warranty, registration, and purchase verification for Zoom products.",
    instruction=prompt.ZOOM_CUSTOMER_SPECIALIST_PROMPT,
    tools=[verify_purchase, handle_registration, check_warranty_status]
) 