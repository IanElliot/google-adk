#!/usr/bin/env python3
"""
Zoom Support Agent Test Launcher
Test launcher script to run comprehensive demonstrations of the Zoom support agent system.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from zoom_support_agent.test_demo import main

if __name__ == "__main__":
    asyncio.run(main()) 