#!/usr/bin/env python3
"""
ULTIMA Runner - Main entry point for the ULTIMA framework
Demonstrates the orchestrator and agent system.
"""

import asyncio
import signal
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agents.orchestrator import NeoOrchestrator
from agents.file_agent import FileAgent


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
        
        # Spawn initial agents
        file_agent = await self.orchestrator.spawn_agent("file", "file_agent_01")
        
        # Start agents
        await self.orchestrator.start_agent("file_agent_01")
        
        print("✅ ULTIMA Framework initialized")
        print("📋 Available capabilities:", list(self.orchestrator.capabilities.keys()))
    
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
            
            # Start status monitoring
            monitor_task = asyncio.create_task(self.status_monitor())
            
            # Run for demo period
            print("\n⏰ Running for 30 seconds... Press Ctrl+C to stop early")
            try:
                await asyncio.sleep(30)
            except KeyboardInterrupt:
                pass
            
            # Cancel monitoring
            monitor_task.cancel()
            
        finally:
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