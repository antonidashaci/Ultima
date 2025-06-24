"""
AI Agent - Local LLM integration with Ollama
Handles code generation, analysis, and intelligent automation
Optimized for RTX 3060 6GB + 16GB RAM systems
"""

import asyncio
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import re
import time

from .base_agent import BaseAgent, Task


class ModelConfig:
    """LLM model configuration for RTX 3060"""
    
    def __init__(self, name: str, max_tokens: int, temperature: float = 0.7, 
                 context_window: int = 4096, vram_usage_gb: float = 6.0):
        self.name = name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.context_window = context_window
        self.vram_usage_gb = vram_usage_gb


class AIAgent(BaseAgent):
    """
    Agent specialized in AI-powered tasks:
    - Code generation and analysis
    - Natural language to code conversion
    - Code review and optimization
    - Documentation generation
    - Intelligent task planning
    - Multi-step reasoning
    """
    
    def __init__(self, name: str, workspace_path: Path):
        super().__init__(name, workspace_path)
        self.ollama_base_url = "http://localhost:11434"
        self.models = {}
        self.current_model = None
        self._setup_models()
        self._setup_prompts()
    
    def get_capabilities(self) -> List[str]:
        """Return capabilities this agent provides"""
        return [
            "code_generation",
            "code_analysis", 
            "code_review",
            "documentation_gen",
            "task_planning",
            "nlp_to_code",
            "code_optimization",
            "bug_detection",
            "test_generation",
            "ai_reasoning"
        ]
    
    def _setup_models(self):
        """Setup available models optimized for RTX 3060"""
        
        # RTX 3060 6GB Optimized Models
        self.models = {
            "qwen2.5:14b-instruct-q4_0": ModelConfig(
                name="qwen2.5:14b-instruct-q4_0",
                max_tokens=4096,
                temperature=0.7,
                context_window=8192,  # RTX 3060 optimization
                vram_usage_gb=5.5  # Leaves 0.5GB for OS
            )
        }
        
        # Set default model
        self.current_model = "qwen2.5:14b-instruct-q4_0"
    
    def _setup_prompts(self):
        """Setup system prompts for different tasks"""
        
        self.system_prompts = {
            "code_generation": "You are ULTIMA AI Agent, an expert software developer optimized for RTX 3060 systems. Generate clean, efficient, and well-documented code following best practices.",
            
            "code_analysis": "You are ULTIMA AI Agent, a code analysis expert. Analyze code for performance, memory usage, security, and RTX 3060 optimizations.",
            
            "task_planning": "You are ULTIMA AI Agent, an intelligent task planner. Break down complex development tasks considering RTX 3060 hardware limitations."
        }
    
    async def execute_task(self, task: Task) -> Optional[Dict[str, Any]]:
        """Execute AI-powered task"""
        task_type = task.type
        metadata = task.metadata
        
        try:
            # Check if Ollama is running
            if not await self._check_ollama():
                return {"error": "Ollama service not available", "success": False}
            
            if task_type == "code_generation":
                return await self._generate_code(metadata)
            elif task_type == "code_analysis":
                return await self._analyze_code(metadata)
            elif task_type == "nlp_to_code":
                return await self._natural_language_to_code(metadata)
            elif task_type == "ai_reasoning":
                return await self._ai_reasoning(metadata)
            else:
                self.logger.error(f"Unknown AI task: {task_type}")
                return None
        
        except Exception as e:
            self.logger.error(f"Error executing {task_type}: {str(e)}")
            return {"error": str(e), "success": False}
    
    async def _check_ollama(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    async def _generate_llm_response(self, prompt: str, system_prompt: str = None, 
                                   max_tokens: int = None) -> Dict[str, Any]:
        """Generate response from local LLM"""
        
        model_name = self.current_model
        model_config = self.models.get(model_name)
        
        if not model_config:
            return {"error": f"Model {model_name} not configured", "success": False}
        
        # Prepare request
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": model_config.temperature,
                "num_predict": max_tokens or model_config.max_tokens,
                "num_ctx": 4096,  # RTX 3060 optimization
                "num_gpu": 1,  # Use RTX 3060
                "num_thread": 8,  # Optimize for 12-core CPU
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            start_time = time.time()
            
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json=payload,
                timeout=120  # 2 minute timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                inference_time = time.time() - start_time
                
                return {
                    "success": True,
                    "response": result.get("response", ""),
                    "model": model_name,
                    "inference_time": round(inference_time, 2),
                    "tokens_generated": len(result.get("response", "").split())
                }
            else:
                return {"error": f"LLM request failed: {response.status_code}", "success": False}
                
        except Exception as e:
            return {"error": f"LLM generation error: {str(e)}", "success": False}
    
    async def _generate_code(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code based on requirements"""
        
        language = metadata.get("language", "python")
        description = metadata.get("description", "")
        requirements = metadata.get("requirements", [])
        
        # Build comprehensive prompt
        prompt = f"""Generate {language} code for: {description}

Requirements:
{chr(10).join(f"- {req}" for req in requirements)}

RTX 3060 Considerations:
- Memory efficiency (6GB VRAM limit)
- Performance optimization

Provide complete, runnable code with comments."""

        result = await self._generate_llm_response(
            prompt, 
            self.system_prompts["code_generation"],
            max_tokens=3000
        )
        
        if result.get("success"):
            result.update({
                "language": language,
                "description": description,
                "rtx3060_optimized": True
            })
        
        return result
    
    async def _analyze_code(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code for quality and performance"""
        
        code = metadata.get("code", "")
        language = metadata.get("language", "python")
        
        prompt = f"""Analyze this {language} code for RTX 3060 system:

```{language}
{code}
```

Analyze for:
1. Performance issues
2. Memory usage
3. RTX 3060 optimizations
4. Code quality
5. Recommendations"""

        result = await self._generate_llm_response(
            prompt,
            self.system_prompts["code_analysis"],
            max_tokens=2000
        )
        
        if result.get("success"):
            result.update({
                "language": language,
                "rtx3060_specific": True
            })
        
        return result
    
    async def _natural_language_to_code(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Convert natural language to code"""
        
        description = metadata.get("description", "")
        language = metadata.get("language", "python")
        
        prompt = f"""Convert this description to {language} code:

"{description}"

Requirements:
- Memory efficient for RTX 3060
- Well-commented
- Error handling
- Example usage

Generate complete code:"""

        result = await self._generate_llm_response(
            prompt,
            self.system_prompts["code_generation"],
            max_tokens=3000
        )
        
        if result.get("success"):
            result.update({
                "original_description": description,
                "language": language,
                "conversion_type": "nlp_to_code"
            })
        
        return result
    
    async def _ai_reasoning(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Perform AI reasoning and problem solving"""
        
        problem = metadata.get("problem", "")
        context = metadata.get("context", "")
        
        prompt = f"""Solve this problem with reasoning:

Problem: {problem}
Context: {context}

System: RTX 3060 + 16GB RAM + 12-core CPU

Provide:
1. Problem analysis
2. Solution approaches
3. Recommended solution
4. Implementation steps
5. RTX 3060 considerations"""

        result = await self._generate_llm_response(
            prompt,
            self.system_prompts["task_planning"],
            max_tokens=2000
        )
        
        if result.get("success"):
            result.update({
                "problem": problem,
                "context": context,
                "system_optimized": True
            })
        
        return result
    
    async def get_model_status(self) -> Dict[str, Any]:
        """Get current model status"""
        
        try:
            ollama_running = await self._check_ollama()
            
            if not ollama_running:
                return {
                    "ollama_status": "offline",
                    "error": "Ollama service not running"
                }
            
            # Get available models
            response = requests.get(f"{self.ollama_base_url}/api/tags")
            available_models = []
            
            if response.status_code == 200:
                models_data = response.json()
                available_models = [model["name"] for model in models_data.get("models", [])]
            
            return {
                "ollama_status": "online",
                "available_models": available_models,
                "current_model": self.current_model,
                "rtx3060_optimized": True
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "ollama_status": "error"
            } 