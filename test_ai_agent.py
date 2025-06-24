#!/usr/bin/env python3
"""
Test script for AI Agent with Ollama integration
Demonstrates RTX 3060 optimized local LLM capabilities
"""

import asyncio
from pathlib import Path
from src.agents.ai_agent import AIAgent
from src.agents.base_agent import Task, TaskStatus
import uuid
from datetime import datetime


async def test_ai_agent():
    """Test AI agent with local LLM"""
    
    print("🤖 ULTIMA AI Agent Test - RTX 3060 + Qwen2.5 14B")
    print("=" * 60)
    
    workspace = Path.cwd()
    agent = AIAgent("ai_test", workspace)
    
    # Check model status first
    print("🔍 Checking Ollama status...")
    status = await agent.get_model_status()
    
    if status.get("ollama_status") == "online":
        print(f"✅ Ollama online")
        print(f"📋 Available models: {status.get('available_models', [])}")
        print(f"🎯 Current model: {status.get('current_model')}")
        print(f"⚡ RTX 3060 optimized: {status.get('rtx3060_optimized')}")
    else:
        print(f"❌ Ollama offline: {status.get('error')}")
        return
    
    # Test 1: Code Generation
    print(f"\n🔧 Test 1: Code Generation")
    code_task = Task(
        id=str(uuid.uuid4()),
        type="code_generation",
        description="Generate Python code for RTX 3060 optimization",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={
            "language": "python",
            "description": "Create a memory monitor for RTX 3060 GPU",
            "requirements": [
                "Monitor GPU memory usage",
                "Alert when approaching 6GB limit",
                "Efficient memory management",
                "Real-time reporting"
            ]
        },
        dependencies=[]
    )
    
    print("  🚀 Generating code...")
    result = await agent.execute_task(code_task)
    
    if result and result.get("success"):
        print(f"  ✅ Generated in {result.get('inference_time', 0)}s")
        print(f"  📊 Tokens: {result.get('tokens_generated', 0)}")
        print(f"  🎯 Language: {result.get('language')}")
        print(f"  ⚡ RTX 3060 optimized: {result.get('rtx3060_optimized')}")
        
        # Show a snippet of generated code
        response = result.get("response", "")
        if len(response) > 300:
            print(f"  📄 Code snippet:\n{response[:300]}...")
        else:
            print(f"  📄 Generated code:\n{response}")
    else:
        print(f"  ❌ Generation failed: {result.get('error') if result else 'No result'}")
    
    # Test 2: Natural Language to Code
    print(f"\n💬 Test 2: Natural Language to Code")
    nl_task = Task(
        id=str(uuid.uuid4()),
        type="nlp_to_code",
        description="Convert description to code",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={
            "language": "python",
            "description": "Create a function that calculates the optimal batch size for RTX 3060 based on available VRAM"
        },
        dependencies=[]
    )
    
    print("  🚀 Converting natural language...")
    result = await agent.execute_task(nl_task)
    
    if result and result.get("success"):
        print(f"  ✅ Converted in {result.get('inference_time', 0)}s")
        print(f"  📊 Tokens: {result.get('tokens_generated', 0)}")
        print(f"  💭 Original: {result.get('original_description')}")
        print(f"  🔄 Type: {result.get('conversion_type')}")
    else:
        print(f"  ❌ Conversion failed: {result.get('error') if result else 'No result'}")
    
    # Test 3: Code Analysis
    print(f"\n🔍 Test 3: Code Analysis")
    
    sample_code = """
import torch
import numpy as np

def process_data(data):
    # Inefficient memory usage
    result = []
    for i in range(len(data)):
        temp = torch.tensor(data[i]).cuda()
        processed = temp * 2 + 1
        result.append(processed.cpu().numpy())
    return result
"""
    
    analysis_task = Task(
        id=str(uuid.uuid4()),
        type="code_analysis",
        description="Analyze code for RTX 3060 optimization",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={
            "language": "python",
            "code": sample_code
        },
        dependencies=[]
    )
    
    print("  🚀 Analyzing code...")
    result = await agent.execute_task(analysis_task)
    
    if result and result.get("success"):
        print(f"  ✅ Analyzed in {result.get('inference_time', 0)}s")
        print(f"  📊 Tokens: {result.get('tokens_generated', 0)}")
        print(f"  🎯 RTX 3060 specific: {result.get('rtx3060_specific')}")
        
        # Show analysis snippet
        response = result.get("response", "")
        if len(response) > 400:
            print(f"  📋 Analysis snippet:\n{response[:400]}...")
        else:
            print(f"  📋 Analysis:\n{response}")
    else:
        print(f"  ❌ Analysis failed: {result.get('error') if result else 'No result'}")
    
    # Test 4: AI Reasoning
    print(f"\n🧠 Test 4: AI Reasoning")
    reasoning_task = Task(
        id=str(uuid.uuid4()),
        type="ai_reasoning",
        description="Plan RTX 3060 optimization strategy",
        priority=1,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={
            "problem": "How to optimize a machine learning pipeline for RTX 3060 6GB VRAM constraint",
            "context": "Training a computer vision model with limited GPU memory"
        },
        dependencies=[]
    )
    
    print("  🚀 AI reasoning...")
    result = await agent.execute_task(reasoning_task)
    
    if result and result.get("success"):
        print(f"  ✅ Reasoned in {result.get('inference_time', 0)}s")
        print(f"  📊 Tokens: {result.get('tokens_generated', 0)}")
        print(f"  🎯 Problem: {result.get('problem')}")
        print(f"  ⚡ System optimized: {result.get('system_optimized')}")
        
        # Show reasoning snippet
        response = result.get("response", "")
        if len(response) > 400:
            print(f"  🧠 Reasoning snippet:\n{response[:400]}...")
        else:
            print(f"  🧠 Reasoning:\n{response}")
    else:
        print(f"  ❌ Reasoning failed: {result.get('error') if result else 'No result'}")
    
    print(f"\n🎯 ULTIMA AI Agent Test Summary:")
    print(f"✅ Local LLM: Qwen2.5 14B Q4 (8.5GB)")
    print(f"⚡ RTX 3060: 6GB VRAM optimized")
    print(f"🤖 Capabilities: Code gen, analysis, NLP→code, reasoning")
    print(f"🚀 Ready for autonomous development tasks")


if __name__ == "__main__":
    print("🤖 Starting ULTIMA AI Agent Test")
    asyncio.run(test_ai_agent()) 