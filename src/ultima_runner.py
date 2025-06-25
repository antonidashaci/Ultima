#!/usr/bin/env python3
"""
ULTIMA Runner - Main entry point for the ULTIMA framework
Demonstrates the orchestrator and agent system.
"""

import asyncio
import signal
import sys
from pathlib import Path
import threading
import json

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agents.orchestrator import NeoOrchestrator
from agents.file_agent import FileAgent
from cursor_bridge.task_detector import CursorTaskDetector
from agents.desktop_agent import DesktopAgent
from agents.planner_agent import PlannerAgent
from agents.coder_agent import CoderAgent
from agents.tester_agent import TesterAgent


class UltimaRunner:
    """Main runner for ULTIMA framework"""
    
    def __init__(self):
        self.workspace_path = Path(__file__).parent.parent
        self.orchestrator = NeoOrchestrator(self.workspace_path)
        self.running = True
    
    async def setup(self):
        """Setup the ULTIMA system"""
        print("🚀 Starting ULTIMA Framework...")
        print(f"📁 Workspace: {self.workspace_path}")
        
        # Register agent classes
        self.orchestrator.register_agent_class("file", FileAgent)
        self.orchestrator.register_agent_class("desktop", DesktopAgent)
        self.orchestrator.register_agent_class("planning", PlannerAgent)
        self.orchestrator.register_agent_class("coder", CoderAgent)
        self.orchestrator.register_agent_class("tester", TesterAgent)
        
        # Spawn initial agents
        file_agent = await self.orchestrator.spawn_agent("file", "file_agent_01")
        desktop_agent = await self.orchestrator.spawn_agent("desktop", "desktop_agent_01")
        planner_agent = await self.orchestrator.spawn_agent("planning", "planner_agent_01")
        coder_agent = await self.orchestrator.spawn_agent("coder", "coder_agent_01")
        tester_agent = await self.orchestrator.spawn_agent("tester", "tester_agent_01")
        
        # Start agents
        await self.orchestrator.start_agent("file_agent_01")
        await self.orchestrator.start_agent("desktop_agent_01")
        await self.orchestrator.start_agent("planner_agent_01")
        await self.orchestrator.start_agent("coder_agent_01")
        await self.orchestrator.start_agent("tester_agent_01")
        
        print("✅ ULTIMA Framework initialized")
        print("📋 Available capabilities:", list(self.orchestrator.capabilities.keys()))
    
    def start_task_detector(self):
        """Starts the task detector to watch for new tasks."""
        print("👀 Starting Task Detector...")
        
        # The detector writes to detected_tasks, which the orchestrator will read from.
        detector = CursorTaskDetector(
            workspace_path=self.workspace_path,
            output_dir=self.workspace_path / "detected_tasks"
        )
        
        # start_monitoring is a blocking call, so run it in a separate thread.
        detector_thread = threading.Thread(target=detector.start_monitoring, daemon=True)
        detector_thread.start()
        
        print("✅ Task Detector is running in the background.")
        return detector_thread

    async def demo_tasks(self):
        """Run demonstration tasks"""
        print("\n🧪 Running demonstration tasks...")
        
        # Task 1: Create a demo file
        await self.orchestrator.execute_task(
            "file_create",
            "Create demo file with content",
            {
                "path": str(self.workspace_path / "workspace" / "demo.txt"),
                "content": "Hello from ULTIMA!\nThis file was created by FileAgent.\n"
            }
        )
        
        # Task 2: Read the file back
        await asyncio.sleep(1)  # Give task time to complete
        await self.orchestrator.execute_task(
            "file_read",
            "Read demo file content",
            {
                "path": str(self.workspace_path / "workspace" / "demo.txt")
            }
        )
        
        # Task 3: Create a directory structure
        await self.orchestrator.execute_task(
            "dir_create", 
            "Create demo directory structure",
            {
                "path": str(self.workspace_path / "workspace" / "demo_project" / "src")
            }
        )
        
        # Task 4: Copy file to new location
        await self.orchestrator.execute_task(
            "file_copy",
            "Copy demo file to project directory", 
            {
                "source": str(self.workspace_path / "workspace" / "demo.txt"),
                "destination": str(self.workspace_path / "workspace" / "demo_project" / "README.txt")
            }
        )
        
        print("✅ Demo tasks queued")
    
    async def status_monitor(self):
        """Monitor system status"""
        while self.running:
            await asyncio.sleep(5)
            
            status = self.orchestrator.get_system_status()
            health = await self.orchestrator.health_check()
            
            print(f"\n📊 System Status:")
            print(f"   Uptime: {status['uptime']:.1f}s")
            print(f"   Total Tasks: {status['system_state']['total_tasks']}")
            print(f"   Health: {health['overall']}")
            
            for agent_name, agent_status in status['agents'].items():
                print(f"   {agent_name}: {'🟢' if agent_status['is_running'] else '🔴'} "
                      f"Queue: {agent_status['queue_size']} "
                      f"Active: {agent_status['active_tasks']}")
            
            if health['issues']:
                print("⚠️ Issues:", health['issues'])
    
    async def shutdown(self):
        """Gracefully shutdown the system"""
        print("\n🛑 Shutting down ULTIMA...")
        self.running = False
        
        await self.orchestrator.save_state()
        await self.orchestrator.stop_all_agents()
        
        print("✅ ULTIMA shutdown complete")
    
    def handle_signal(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n📨 Received signal {signum}")
        asyncio.create_task(self.shutdown())
    
    async def ingest_detected_tasks(self):
        """Periodically scans detected_tasks directory and ingests new tasks."""
        processed_files = set()
        tasks_dir = self.workspace_path / "detected_tasks"
        tasks_dir.mkdir(exist_ok=True)
        
        while self.running:
            for file_path in tasks_dir.glob("task_*.json"):
                if file_path in processed_files:
                    continue
                try:
                    with open(file_path, 'r') as f:
                        task_json = json.load(f)
                    task_type = task_json.get('type') or task_json.get('task_type') or 'general'
                    description = task_json.get('description', 'No description')
                    metadata = task_json.get('metadata', {})
                    await self.orchestrator.execute_task(task_type, description, metadata)
                    processed_files.add(file_path)
                except Exception as e:
                    print(f"⚠️ Failed to ingest task file {file_path}: {e}")
            await asyncio.sleep(2)

    async def bus_listener(self):
        from bus import bus
        while self.running:
            async for msg in bus.subscribe():
                if not self.running:
                    break
                await self.orchestrator.execute_task(msg["type"], msg["description"], msg.get("metadata"))

    async def run(self):
        """Main run loop"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        
        try:
            # Initialize system
            await self.setup()
            
            # Run demo tasks
            await self.demo_tasks()
            
            # Start status monitoring and task detector
            monitor_task = asyncio.create_task(self.status_monitor())
            detector_thread = self.start_task_detector()
            ingest_task = asyncio.create_task(self.ingest_detected_tasks())
            bus_task = asyncio.create_task(self.bus_listener())
            
            # Run indefinitely until stopped
            print("\n🚀 ULTIMA is running. Press Ctrl+C to stop.")
            while self.running:
                await asyncio.sleep(1)

        finally:
            if 'monitor_task' in locals() and not monitor_task.done():
                monitor_task.cancel()
            if 'ingest_task' in locals() and not ingest_task.done():
                ingest_task.cancel()
            if 'bus_task' in locals() and not bus_task.done():
                bus_task.cancel()
            
            await self.shutdown()


async def main():
    """Main entry point"""
    runner = UltimaRunner()
    await runner.run()


if __name__ == "__main__":
    print("=" * 60)
    print("   ULTIMA Framework - MVP Generation System")
    print("   Version 0.1.0 - Foundation Release")
    print("=" * 60)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1) 