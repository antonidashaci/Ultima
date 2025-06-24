"""
NeoAI Orchestrator - Central coordination system for ULTIMA agents
Manages task routing, agent coordination, and system-wide state.
"""

import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Type
from dataclasses import dataclass

from .base_agent import BaseAgent, Task, TaskStatus


@dataclass
class AgentCapability:
    """Represents an agent's capability"""
    agent_name: str
    capability: str
    priority: int
    load_factor: float  # Current load (0.0 to 1.0)


class NeoOrchestrator:
    """
    Central orchestrator for ULTIMA framework.
    Manages agent lifecycle, task routing, and system coordination.
    """
    
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_classes: Dict[str, Type[BaseAgent]] = {}
        self.task_history: List[Task] = []
        self.system_state = {
            "started_at": datetime.now(),
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0
        }
        
        # Setup directories
        self.orchestrator_dir = workspace_path / "orchestrator"
        self.state_file = self.orchestrator_dir / "system_state.json"
        self.orchestrator_dir.mkdir(parents=True, exist_ok=True)
        
        # Capability registry
        self.capabilities: Dict[str, List[AgentCapability]] = {}
        
    def register_agent_class(self, agent_type: str, agent_class: Type[BaseAgent]):
        """Register an agent class for dynamic instantiation"""
        self.agent_classes[agent_type] = agent_class
        
    async def spawn_agent(self, agent_type: str, agent_name: str) -> BaseAgent:
        """Spawn a new agent instance"""
        if agent_type not in self.agent_classes:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_class = self.agent_classes[agent_type]
        agent = agent_class(agent_name, self.workspace_path)
        
        self.agents[agent_name] = agent
        
        # Register agent capabilities
        for capability in agent.get_capabilities():
            if capability not in self.capabilities:
                self.capabilities[capability] = []
            
            self.capabilities[capability].append(AgentCapability(
                agent_name=agent_name,
                capability=capability,
                priority=1,
                load_factor=0.0
            ))
        
        return agent
    
    async def start_agent(self, agent_name: str) -> None:
        """Start an agent's main loop"""
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            # Start agent in background task
            asyncio.create_task(agent.start())
    
    async def stop_agent(self, agent_name: str) -> None:
        """Stop an agent"""
        if agent_name in self.agents:
            await self.agents[agent_name].stop()
    
    async def stop_all_agents(self) -> None:
        """Stop all agents"""
        for agent in self.agents.values():
            await agent.stop()
    
    def create_task(self, task_type: str, description: str, 
                   metadata: Optional[Dict[str, Any]] = None) -> Task:
        """Create a new task"""
        task_id = str(uuid.uuid4())
        now = datetime.now()
        
        task = Task(
            id=task_id,
            type=task_type,
            description=description,
            priority=1,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
            metadata=metadata or {},
            dependencies=[]
        )
        
        self.task_history.append(task)
        self.system_state["total_tasks"] += 1
        
        return task
    
    async def route_task(self, task: Task) -> Optional[str]:
        """
        Route a task to the most appropriate agent.
        Returns agent name if successful, None if no capable agent found.
        """
        # Find agents capable of handling this task type
        capable_agents = []
        
        for capability, agent_caps in self.capabilities.items():
            if capability == task.type or task.type.startswith(capability):
                capable_agents.extend(agent_caps)
        
        if not capable_agents:
            return None
        
        # Sort by priority and load factor
        capable_agents.sort(key=lambda x: (x.priority, x.load_factor))
        
        # Route to best available agent
        best_agent = capable_agents[0]
        agent = self.agents[best_agent.agent_name]
        
        await agent.add_task(task)
        
        # Update load factor (simple queue-based calculation)
        best_agent.load_factor = agent.task_queue.qsize() / 10.0
        
        return best_agent.agent_name
    
    async def execute_task(self, task_type: str, description: str, 
                          metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Create and execute a task.
        Returns the agent name that handled the task, or None if failed.
        """
        task = self.create_task(task_type, description, metadata)
        agent_name = await self.route_task(task)
        
        if agent_name:
            print(f"Task {task.id} routed to agent {agent_name}")
            return agent_name
        else:
            print(f"No capable agent found for task type: {task_type}")
            return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        agent_statuses = {}
        for name, agent in self.agents.items():
            agent_statuses[name] = agent.get_status()
        
        return {
            "system_state": self.system_state,
            "agents": agent_statuses,
            "capabilities": {
                cap: [ac.agent_name for ac in agents] 
                for cap, agents in self.capabilities.items()
            },
            "uptime": (datetime.now() - self.system_state["started_at"]).total_seconds()
        }
    
    async def save_state(self) -> None:
        """Save system state to disk"""
        state_data = {
            "system_state": {
                **self.system_state,
                "started_at": self.system_state["started_at"].isoformat()
            },
            "agents": list(self.agents.keys()),
            "capabilities": {
                cap: [{"agent": ac.agent_name, "priority": ac.priority} 
                     for ac in agents]
                for cap, agents in self.capabilities.items()
            }
        }
        
        with open(self.state_file, 'w') as f:
            json.dump(state_data, f, indent=2)
    
    async def load_state(self) -> None:
        """Load system state from disk"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state_data = json.load(f)
                
            # Restore system state
            if "system_state" in state_data:
                self.system_state.update(state_data["system_state"])
                if "started_at" in self.system_state:
                    self.system_state["started_at"] = datetime.fromisoformat(
                        self.system_state["started_at"]
                    )
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform system health check"""
        health_status = {
            "overall": "healthy",
            "agents": {},
            "issues": []
        }
        
        for name, agent in self.agents.items():
            agent_health = {
                "running": agent.is_running,
                "queue_size": agent.task_queue.qsize(),
                "active_tasks": len(agent.active_tasks)
            }
            
            # Check for potential issues
            if agent.task_queue.qsize() > 50:
                health_status["issues"].append(f"Agent {name} has high queue size")
            
            if len(agent.active_tasks) > 10:
                health_status["issues"].append(f"Agent {name} has many active tasks")
            
            health_status["agents"][name] = agent_health
        
        if health_status["issues"]:
            health_status["overall"] = "degraded"
        
        return health_status 