#!/usr/bin/env python3
"""
Simple Diagnostic Test - Direct agent testing
"""

import asyncio
from pathlib import Path
from src.agents.diagnostic_agent import DiagnosticAgent


async def main():
    """Test diagnostic agent directly"""
    print("🔬 ULTIMA Diagnostic Agent - Direct Test")
    print("=" * 50)
    
    # Create diagnostic agent
    workspace = Path.cwd()
    agent = DiagnosticAgent("diagnostic_test", workspace)
    
    print(f"Agent capabilities: {agent.get_capabilities()}")
    print(f"System info gathered: {bool(agent.system_info)}")
    
    # Check GPU info
    gpu_info = agent.system_info.get("gpu", [])
    print(f"\n🎮 GPU Information:")
    if gpu_info:
        for i, gpu in enumerate(gpu_info):
            print(f"  GPU {i+1}: {gpu['name']}")
            print(f"    Memory: {gpu['memory_mb']/1024:.1f} GB")
            print(f"    Driver: {gpu['driver']}")
    else:
        print("  No NVIDIA GPU detected")
    
    # Check memory
    memory = agent.system_info["hardware"]["memory"]
    print(f"\n💾 Memory Information:")
    print(f"  Total: {memory['total']/1024**3:.1f} GB")
    print(f"  Available: {memory['available']/1024**3:.1f} GB")
    print(f"  Used: {memory['percent']:.1f}%")
    
    # Check disk
    disk = agent.system_info["hardware"]["disk"]
    print(f"\n💿 Disk Information:")
    print(f"  Total: {disk['total']/1024**3:.1f} GB")
    print(f"  Free: {disk['free']/1024**3:.1f} GB")
    print(f"  Used: {(disk['used']/disk['total'])*100:.1f}%")
    
    # Run a hardware check
    print(f"\n🔧 Hardware Check Results:")
    from src.agents.base_agent import Task, TaskStatus
    import uuid
    from datetime import datetime
    
    # Create test task
    task = Task(
        id=str(uuid.uuid4()),
        type="hardware_check",
        description="Test hardware check",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={},
        dependencies=[]
    )
    
    result = await agent.execute_task(task)
    
    if result:
        print(f"  Hardware Status: {result['hardware_status']}")
        for check in result['checks']:
            status_icon = "✅" if check['status'] == 'PASS' else "❌"
            print(f"  {status_icon} {check['name']}: {check['status']}")
            if check['details']:
                for key, value in check['details'].items():
                    if isinstance(value, (int, float)):
                        print(f"    {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main()) 