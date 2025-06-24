"""
Base Agent Class for ULTIMA Framework
All specialized agents inherit from this class.
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NEEDS_APPROVAL = "needs_approval"


@dataclass
class Task:
    """Basic task structure for agent communication"""
    id: str
    type: str
    description: str
    priority: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]
    dependencies: List[str] = None
    output_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization"""
        data = asdict(self)
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Create task from dictionary"""
        data['status'] = TaskStatus(data['status'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


class BaseAgent(ABC):
    """
    Base class for all ULTIMA agents.
    Provides common functionality for task management, logging, and orchestration.
    """
    
    def __init__(self, name: str, workspace_path: Path):
        self.name = name
        self.workspace_path = workspace_path
        self.task_queue = asyncio.Queue()
        self.active_tasks: Dict[str, Task] = {}
        self.logger = self._setup_logger()
        self.is_running = False
        
        # Create agent-specific directories
        self.agent_dir = workspace_path / "agents" / name
        self.logs_dir = workspace_path / "logs" / name
        self.tasks_dir = workspace_path / "tasks" / name
        
        for dir_path in [self.agent_dir, self.logs_dir, self.tasks_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _setup_logger(self) -> logging.Logger:
        """Setup agent-specific logger"""
        logger = logging.getLogger(f"ultima.{self.name}")
        logger.setLevel(logging.INFO)
        
        # Prevent duplicate handlers
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    async def add_task(self, task: Task) -> None:
        """Add a task to the agent's queue"""
        await self.task_queue.put(task)
        self.logger.info(f"Task {task.id} added to queue: {task.description}")
    
    async def get_task(self) -> Optional[Task]:
        """Get next task from queue"""
        try:
            task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
            return task
        except asyncio.TimeoutError:
            return None
    
    async def update_task_status(self, task_id: str, status: TaskStatus, 
                               metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update task status and metadata"""
        if task_id in self.active_tasks:
            task = self.active_tasks[task_id]
            task.status = status
            task.updated_at = datetime.now()
            
            if metadata:
                task.metadata.update(metadata)
            
            # Save task state
            await self._save_task_state(task)
            self.logger.info(f"Task {task_id} status updated to {status.value}")
    
    async def _save_task_state(self, task: Task) -> None:
        """Save task state to file"""
        task_file = self.tasks_dir / f"{task.id}.json"
        with open(task_file, 'w') as f:
            json.dump(task.to_dict(), f, indent=2)
    
    async def _load_task_state(self, task_id: str) -> Optional[Task]:
        """Load task state from file"""
        task_file = self.tasks_dir / f"{task_id}.json"
        if task_file.exists():
            with open(task_file, 'r') as f:
                data = json.load(f)
                return Task.from_dict(data)
        return None
    
    async def start(self) -> None:
        """Start the agent's main loop"""
        self.is_running = True
        self.logger.info(f"Agent {self.name} started")
        
        try:
            while self.is_running:
                task = await self.get_task()
                if task:
                    await self._process_task(task)
                else:
                    await asyncio.sleep(0.1)  # Small delay when no tasks
        finally:
            self.logger.info(f"Agent {self.name} stopped")
    
    async def stop(self) -> None:
        """Stop the agent"""
        self.is_running = False
        self.logger.info(f"Agent {self.name} stopping...")
    
    async def _process_task(self, task: Task) -> None:
        """Process a single task"""
        self.active_tasks[task.id] = task
        
        try:
            await self.update_task_status(task.id, TaskStatus.IN_PROGRESS)
            
            # Execute the task
            result = await self.execute_task(task)
            
            # Update task with result
            if result:
                await self.update_task_status(
                    task.id, 
                    TaskStatus.COMPLETED,
                    {"result": result}
                )
            else:
                await self.update_task_status(task.id, TaskStatus.FAILED)
            
        except Exception as e:
            self.logger.error(f"Task {task.id} failed: {str(e)}")
            await self.update_task_status(
                task.id, 
                TaskStatus.FAILED,
                {"error": str(e)}
            )
        finally:
            # Remove from active tasks
            self.active_tasks.pop(task.id, None)
    
    @abstractmethod
    async def execute_task(self, task: Task) -> Optional[Dict[str, Any]]:
        """
        Execute a specific task. Must be implemented by subclasses.
        
        Args:
            task: The task to execute
            
        Returns:
            Dict containing task results, or None if failed
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return list of capabilities this agent provides.
        Used by orchestrator for task routing.
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "name": self.name,
            "is_running": self.is_running,
            "queue_size": self.task_queue.qsize(),
            "active_tasks": len(self.active_tasks),
            "capabilities": self.get_capabilities()
        } 