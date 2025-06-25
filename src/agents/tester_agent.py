#!/usr/bin/env python3
"""TesterAgent (stub) – executes pytest in a given directory.
Currently just returns success without running anything.
Capability: testing"""

import asyncio
from typing import Optional, Dict
from .base_agent import BaseAgent, Task

class TesterAgent(BaseAgent):
    def get_capabilities(self):
        return ["testing"]

    async def execute_task(self, task: Task) -> Optional[Dict]:
        # Dummy: pretend tests pass
        await asyncio.sleep(0.2)
        return {"result": "tests_passed"} 