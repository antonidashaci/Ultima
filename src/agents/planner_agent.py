#!/usr/bin/env python3
"""PlannerAgent – first step of multi-agent pipeline.
Takes a high-level task and decomposes it into one or more concrete tasks which
it sends back to the orchestrator.
For now decomposition is heuristic (no LLM call) to keep demo offline.
"""

import asyncio
from typing import Optional, Dict, List
from pathlib import Path
from .base_agent import BaseAgent, Task
from bus import bus
from llm import chat
import json as _json
from datetime import datetime

class PlannerAgent(BaseAgent):
    def get_capabilities(self):
        return ["planning"]

    async def execute_task(self, task: Task) -> Optional[Dict]:
        prompt = (
            "Analyse the following high-level goal, then propose a plan. "
            "Return a SINGLE JSON object with keys:\n"
            "  analysis: string (detailed reasoning)\n"
            "  tasks: list of objects with keys 'type', 'description', 'priority', optional 'metadata'\n\n"
            f"Goal: {task.description}"
        )

        analysis_text = None
        subtasks: List[Dict] = []
        try:
            llm_response = await chat(prompt)
            parsed = _json.loads(llm_response.strip())
            analysis_text = parsed.get("analysis")
            subtasks = parsed.get("tasks", [])
        except Exception:
            # fallback analysis & task
            analysis_text = "Heuristic analysis: create a desktop application as first step."
            subtasks = [{
                "type": "desktop_application",
                "description": task.description,
                "priority": 1,
                "metadata": {}
            }]

        # Save analysis to file
        analysis_dir = self.workspace_path / "workspace" / "output" / "reasoning"
        analysis_dir.mkdir(parents=True, exist_ok=True)
        analysis_path = analysis_dir / f"{task.id[:8]}_analysis.md"
        timestamp = datetime.now().isoformat()
        analysis_path.write_text(f"# Analysis for task {task.id}\n\n" +
                                f"**Timestamp**: {timestamp}\n\n" +
                                (analysis_text or "(no analysis)") + "\n")

        # publish subtasks
        for st in subtasks:
            await bus.publish(st)

        await asyncio.sleep(0.1)
        return {"analysis_path": str(analysis_path), "generated_subtasks": len(subtasks)} 