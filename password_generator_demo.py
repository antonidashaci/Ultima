#!/usr/bin/env python3
"""
Live Demo: ULTIMA builds a Password Generator App
Single comment → Complete working application
"""

# This is what a user would type in Cursor:
# #AI_TASK: Build a password generator with security options [type:web_development]

import asyncio
from pathlib import Path
from src.cursor_bridge.task_detector import TaskDefinition
from src.agents.web_agent import WebAgent
from src.agents.base_agent import Task, TaskStatus
from datetime import datetime

async def demo_password_generator():
    print("🔐 ULTIMA LIVE DEMO: Password Generator App")
    print("=" * 50)
    print("User request: Build a password generator with security options")
    print("=" * 50)
    
    # Step 1: Parse the request (simulating Cursor detection)
    cursor_comment = "# #AI_TASK: Build a password generator with security options [type:web_development]"
    task_def = TaskDefinition(cursor_comment, Path("demo.js"), 1)
    
    print(f"✅ Task detected: {task_def.parsed_data['description']}")
    
    # Step 2: Create specialized password generator
    workspace = Path.cwd()
    web_agent = WebAgent("password_demo", workspace)
    
    # Step 3: Execute task
    print("🚀 ULTIMA is building your password generator...")
    
    task = Task(
        id=task_def.task_id,
        type="web_development", 
        description="Build a password generator with security options",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={
            "description": "Create a secure password generator with customizable options",
            "app_type": "password_generator",
            "features": [
                "Length customization",
                "Character type selection",
                "Strength indicator", 
                "Copy to clipboard",
                "Generate multiple passwords",
                "Security recommendations"
            ]
        },
        dependencies=[]
    )
    
    result = await web_agent.execute_task(task)
    
    if result and result.get("success"):
        print("✅ Password Generator App Created Successfully!")
        print(f"📁 Files: {', '.join(result.get('files_created', []))}")
        print("🔐 Ready to generate secure passwords!")
        return True
    else:
        print("❌ Creation failed")
        return False

if __name__ == "__main__":
    asyncio.run(demo_password_generator()) 