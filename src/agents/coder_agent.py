#!/usr/bin/env python3
"""CoderAgent (stub) – placeholder that will later call LLM to write code.
Currently just logs the request and creates a dummy file to prove flow.
Capability: code_generation"""

import asyncio
from pathlib import Path
from typing import Optional, Dict
from .base_agent import BaseAgent, Task

class CoderAgent(BaseAgent):
    def get_capabilities(self):
        return ["code_generation"]

    async def execute_task(self, task: Task) -> Optional[Dict]:
        # Dummy implementation: write a file named output.txt with task description
        target_dir = self.workspace_path / "workspace" / "output" / "code"
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / f"{task.id[:8]}_output.txt"
        file_path.write_text(f"Placeholder for: {task.description}\n")
        await asyncio.sleep(0.1)
        return {"path": str(file_path), "created": True} 