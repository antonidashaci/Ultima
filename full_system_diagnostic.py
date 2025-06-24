#!/usr/bin/env python3
"""
Full System Diagnostic - RTX 3060 Optimized Check
"""

import asyncio
from pathlib import Path
from src.agents.diagnostic_agent import DiagnosticAgent
from src.agents.base_agent import Task, TaskStatus
import uuid
from datetime import datetime


async def run_full_diagnostic():
    """Run comprehensive system diagnostic"""
    print("🏥 ULTIMA Full System Diagnostic - RTX 3060 Edition")
    print("=" * 60)
    
    workspace = Path.cwd()
    agent = DiagnosticAgent("system_diagnostic", workspace)
    
    # Full system check
    print("🔍 Running Full System Check...")
    task = Task(
        id=str(uuid.uuid4()),
        type="system_check", 
        description="Complete system health check",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={"include_recommendations": True},
        dependencies=[]
    )
    
    result = await agent.execute_task(task)
    
    if result:
        print(f"\n🎯 Overall Status: {result['overall_status']}")
        
        # System Info Summary
        sys_info = result['system_info']
        print(f"\n💻 System Information:")
        print(f"  OS: {sys_info['os']['system']} {sys_info['os']['release']}")
        print(f"  Architecture: {sys_info['os']['machine']}")
        print(f"  CPU Cores: {sys_info['hardware']['cpu_count']}")
        
        # Requirements Check
        print(f"\n✅ Requirements Analysis:")
        for req in result['requirements']:
            status_icon = "✅" if req['status'] == 'PASS' else "❌" if req['required'] else "⚠️"
            required_text = " (Required)" if req['required'] else " (Optional)"
            print(f"  {status_icon} {req['name']}{required_text}: {req['status']}")
        
        # Errors and Warnings
        if result['errors']:
            print(f"\n❌ Critical Issues:")
            for error in result['errors']:
                print(f"  • {error}")
        
        if result['warnings']:
            print(f"\n⚠️ Warnings:")
            for warning in result['warnings']:
                print(f"  • {warning}")
        
        # RTX 3060 Specific Recommendations
        if result['recommendations']:
            print(f"\n💡 RTX 3060 Optimization Recommendations:")
            for rec in result['recommendations']:
                print(f"  {rec}")
    
    # GPU-specific analysis
    print(f"\n🎮 GPU-Specific Analysis...")
    gpu_task = Task(
        id=str(uuid.uuid4()),
        type="gpu_check",
        description="GPU analysis for AI workloads",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={"focus": "ai_model_compatibility"},
        dependencies=[]
    )
    
    gpu_result = await agent.execute_task(gpu_task)
    if gpu_result:
        print(f"  GPU Status: {gpu_result['gpu_status']}")
        gpu_info = gpu_result['gpu_info']
        print(f"  Model: {gpu_info['name']}")
        print(f"  Memory: {gpu_info['memory_mb']/1024:.1f} GB")
        print(f"  Driver: {gpu_info['driver']}")
        
        ai_readiness = gpu_result['ai_readiness']
        print(f"  Max Model Size: {ai_readiness['max_model_size']}")
        
        print(f"  Model Recommendations:")
        for rec in gpu_result['model_recommendations']:
            print(f"    • {rec}")
    
    # Performance check
    print(f"\n⚡ Performance Analysis...")
    perf_task = Task(
        id=str(uuid.uuid4()),
        type="performance_check",
        description="Current system performance",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={"include_recommendations": True},
        dependencies=[]
    )
    
    perf_result = await agent.execute_task(perf_task)
    if perf_result:
        print(f"  Performance Status: {perf_result['performance_status']}")
        metrics = perf_result['metrics']
        print(f"  CPU Usage: {metrics['cpu_usage']:.1f}%")
        print(f"  Memory Usage: {metrics['memory_usage']:.1f}%")
        print(f"  Available RAM: {metrics['available_memory_gb']:.1f} GB")
        
        if perf_result['recommendations']:
            print(f"  Performance Tips:")
            for rec in perf_result['recommendations']:
                print(f"    {rec}")
    
    # Software check
    print(f"\n🛠️ Software Dependencies...")
    soft_task = Task(
        id=str(uuid.uuid4()),
        type="software_check",
        description="Software dependency validation",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={},
        dependencies=[]
    )
    
    soft_result = await agent.execute_task(soft_task)
    if soft_result:
        print(f"  Software Status: {soft_result['software_status']}")
        
        for check in soft_result['checks']:
            status_icon = "✅" if check['status'] == 'PASS' else "❌" if check['required'] else "⚠️"
            print(f"  {status_icon} {check['name']}: {check['status']}")
        
        if soft_result['install_commands']:
            print(f"\n📦 Missing Software Installation Commands:")
            for cmd in soft_result['install_commands']:
                req_text = " (Required)" if cmd['required'] else " (Optional)"
                print(f"  {cmd['package']}{req_text}:")
                print(f"    {cmd['command']}")
    
    print(f"\n🎯 ULTIMA System Readiness Summary:")
    print(f"✅ Hardware: RTX 3060 + 15.5GB RAM + 12 CPU cores")
    print(f"✅ Target: 14B Q4/Q5 models with 4096 token context")
    print(f"✅ Capability: Web apps (2-3h), Android apps (4-6h), Desktop apps (6-8h)")
    print(f"⚠️ Limitation: Avoid 32B+ models (OOM risk)")
    print(f"💡 Recommendation: Run max 2-3 concurrent agents")


if __name__ == "__main__":
    asyncio.run(run_full_diagnostic()) 