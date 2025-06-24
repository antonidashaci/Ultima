"""
Diagnostic Agent - System health check and dependency validation
Monitors system resources, detects missing packages, validates environment
"""

import os
import shutil
import subprocess
import platform
import psutil
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
import re

from .base_agent import BaseAgent, Task


class SystemRequirement:
    """Represents a system requirement check"""
    
    def __init__(self, name: str, check_func, required: bool = True, 
                 fix_command: Optional[str] = None):
        self.name = name
        self.check_func = check_func
        self.required = required
        self.fix_command = fix_command
        self.status = None
        self.details = {}


class DiagnosticAgent(BaseAgent):
    """
    Agent responsible for system diagnostics:
    - Hardware requirement validation (GPU, RAM, Disk)
    - Software dependency checking (Python, Node, Docker)
    - Environment validation (Ubuntu version, permissions)
    - Performance monitoring and recommendations
    """
    
    def __init__(self, name: str, workspace_path: Path):
        super().__init__(name, workspace_path)
        self.system_info = {}
        self.requirements = []
        self._setup_requirements()
        self._gather_system_info()
    
    def get_capabilities(self) -> List[str]:
        """Return capabilities this agent provides"""
        return [
            "system_check",
            "hardware_check", 
            "software_check",
            "dependency_check",
            "performance_check",
            "environment_validate",
            "gpu_check",
            "memory_check",
            "disk_check"
        ]
    
    def _setup_requirements(self):
        """Setup all system requirements to check"""
        
        # Hardware requirements
        self.requirements.extend([
            SystemRequirement("RAM >= 12GB", self._check_ram),
            SystemRequirement("GPU Memory >= 4GB", self._check_gpu_memory),
            SystemRequirement("Free Disk >= 50GB", self._check_disk_space),
            SystemRequirement("CPU Cores >= 4", self._check_cpu_cores),
        ])
        
        # Core software requirements
        self.requirements.extend([
            SystemRequirement("Python >= 3.8", self._check_python, 
                            fix_command="sudo apt install python3.11"),
            SystemRequirement("Git", self._check_git,
                            fix_command="sudo apt install git"),
            SystemRequirement("Curl", self._check_curl,
                            fix_command="sudo apt install curl"),
        ])
        
        # Development tools
        self.requirements.extend([
            SystemRequirement("Node.js", self._check_nodejs, required=False,
                            fix_command="curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt install nodejs"),
            SystemRequirement("Docker", self._check_docker, required=False,
                            fix_command="sudo apt install docker.io"),
            SystemRequirement("Build Tools", self._check_build_tools, required=False,
                            fix_command="sudo apt install build-essential"),
        ])
        
        # AI/ML specific
        self.requirements.extend([
            SystemRequirement("NVIDIA Driver", self._check_nvidia_driver, required=False,
                            fix_command="sudo apt install nvidia-driver-535"),
            SystemRequirement("CUDA Support", self._check_cuda, required=False),
        ])
    
    def _gather_system_info(self):
        """Gather comprehensive system information"""
        try:
            self.system_info = {
                "os": {
                    "system": platform.system(),
                    "release": platform.release(), 
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "processor": platform.processor()
                },
                "hardware": {
                    "cpu_count": psutil.cpu_count(),
                    "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
                    "memory": psutil.virtual_memory()._asdict(),
                    "disk": psutil.disk_usage('/')._asdict(),
                    "boot_time": psutil.boot_time()
                },
                "network": len(psutil.net_if_addrs()) > 0
            }
            
            # GPU information
            try:
                gpu_info = subprocess.run(
                    ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader,nounits"],
                    capture_output=True, text=True, timeout=5
                )
                if gpu_info.returncode == 0:
                    gpu_lines = gpu_info.stdout.strip().split('\n')
                    self.system_info["gpu"] = []
                    for line in gpu_lines:
                        parts = line.split(', ')
                        if len(parts) >= 3:
                            self.system_info["gpu"].append({
                                "name": parts[0],
                                "memory_mb": int(parts[1]),
                                "driver": parts[2]
                            })
                else:
                    self.system_info["gpu"] = []
            except (subprocess.TimeoutExpired, FileNotFoundError):
                self.system_info["gpu"] = []
                
        except Exception as e:
            self.logger.error(f"Error gathering system info: {e}")
    
    async def execute_task(self, task: Task) -> Optional[Dict[str, Any]]:
        """Execute diagnostic task"""
        task_type = task.type
        metadata = task.metadata
        
        try:
            if task_type == "system_check":
                return await self._full_system_check(metadata)
            elif task_type == "hardware_check":
                return await self._hardware_check(metadata)
            elif task_type == "software_check":
                return await self._software_check(metadata)
            elif task_type == "dependency_check":
                return await self._dependency_check(metadata)
            elif task_type == "performance_check":
                return await self._performance_check(metadata)
            elif task_type == "gpu_check":
                return await self._gpu_specific_check(metadata)
            elif task_type == "memory_check":
                return await self._memory_specific_check(metadata)
            else:
                self.logger.error(f"Unknown diagnostic task: {task_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error executing {task_type}: {str(e)}")
            return None
    
    async def _full_system_check(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive system check"""
        results = {
            "overall_status": "unknown",
            "system_info": self.system_info,
            "requirements": [],
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
        
        # Check all requirements
        passed = 0
        failed_required = 0
        
        for req in self.requirements:
            try:
                success, details = req.check_func()
                req.status = "PASS" if success else "FAIL"
                req.details = details
                
                req_result = {
                    "name": req.name,
                    "status": req.status,
                    "required": req.required,
                    "details": details,
                    "fix_command": req.fix_command
                }
                results["requirements"].append(req_result)
                
                if success:
                    passed += 1
                elif req.required:
                    failed_required += 1
                    results["errors"].append(f"Required: {req.name}")
                else:
                    results["warnings"].append(f"Optional: {req.name}")
                    
            except Exception as e:
                req.status = "ERROR"
                req.details = {"error": str(e)}
                results["errors"].append(f"Check failed for {req.name}: {e}")
        
        # Determine overall status
        if failed_required > 0:
            results["overall_status"] = "CRITICAL"
        elif len(results["warnings"]) > 3:
            results["overall_status"] = "WARNING"
        else:
            results["overall_status"] = "HEALTHY"
        
        # Add RTX 3060 specific recommendations
        self._add_rtx3060_recommendations(results)
        
        return results
    
    def _add_rtx3060_recommendations(self, results: Dict[str, Any]):
        """Add RTX 3060 6GB specific recommendations"""
        gpu_info = self.system_info.get("gpu", [])
        memory_mb = self.system_info["hardware"]["memory"]["total"] // (1024*1024)
        
        if gpu_info:
            gpu = gpu_info[0]
            if "RTX 3060" in gpu["name"] or gpu["memory_mb"] <= 6144:
                results["recommendations"].extend([
                    "✅ RTX 3060 detected - Use 14B Q4/Q5 quantized models maximum",
                    "⚠️ Avoid 32B+ models - will cause OOM errors",
                    "🔧 Set context length to 4096 tokens maximum",
                    "💾 Close other GPU applications during ULTIMA tasks"
                ])
        
        if memory_mb <= 16384:  # 16GB or less
            results["recommendations"].extend([
                "⚠️ 16GB RAM detected - Monitor usage during multi-agent tasks",
                "🔧 Consider increasing swap space for large operations",
                "💡 Run max 2-3 concurrent agents to avoid OOM"
            ])
    
    # Hardware check functions
    def _check_ram(self) -> Tuple[bool, Dict[str, Any]]:
        """Check if system has sufficient RAM"""
        memory = self.system_info["hardware"]["memory"]
        total_gb = memory["total"] / (1024**3)
        return total_gb >= 12, {
            "total_gb": round(total_gb, 1),
            "available_gb": round(memory["available"] / (1024**3), 1),
            "percent_used": memory["percent"]
        }
    
    def _check_gpu_memory(self) -> Tuple[bool, Dict[str, Any]]:
        """Check GPU memory availability"""
        gpu_info = self.system_info.get("gpu", [])
        if not gpu_info:
            return False, {"error": "No GPU detected"}
        
        gpu = gpu_info[0]
        memory_gb = gpu["memory_mb"] / 1024
        return memory_gb >= 4, {
            "name": gpu["name"],
            "memory_gb": round(memory_gb, 1),
            "driver": gpu["driver"]
        }
    
    def _check_disk_space(self) -> Tuple[bool, Dict[str, Any]]:
        """Check available disk space"""
        disk = self.system_info["hardware"]["disk"]
        free_gb = disk["free"] / (1024**3)
        return free_gb >= 50, {
            "free_gb": round(free_gb, 1),
            "total_gb": round(disk["total"] / (1024**3), 1),
            "percent_used": round((disk["used"] / disk["total"]) * 100, 1)
        }
    
    def _check_cpu_cores(self) -> Tuple[bool, Dict[str, Any]]:
        """Check CPU core count"""
        cores = self.system_info["hardware"]["cpu_count"]
        return cores >= 4, {
            "cores": cores,
            "logical_cores": psutil.cpu_count(logical=True)
        }
    
    # Software check functions
    def _check_python(self) -> Tuple[bool, Dict[str, Any]]:
        """Check Python version"""
        try:
            result = subprocess.run(["python3", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version_str = result.stdout.strip()
                # Extract version numbers
                match = re.search(r'Python (\d+)\.(\d+)\.(\d+)', version_str)
                if match:
                    major, minor, patch = map(int, match.groups())
                    is_valid = (major > 3) or (major == 3 and minor >= 8)
                    return is_valid, {
                        "version": f"{major}.{minor}.{patch}",
                        "path": shutil.which("python3")
                    }
            return False, {"error": "Python3 not found"}
        except Exception as e:
            return False, {"error": str(e)}
    
    def _check_git(self) -> Tuple[bool, Dict[str, Any]]:
        """Check Git installation"""
        git_path = shutil.which("git")
        if git_path:
            try:
                result = subprocess.run(["git", "--version"], 
                                      capture_output=True, text=True)
                return True, {
                    "version": result.stdout.strip(),
                    "path": git_path
                }
            except:
                pass
        return False, {"error": "Git not found"}
    
    def _check_curl(self) -> Tuple[bool, Dict[str, Any]]:
        """Check Curl installation"""
        curl_path = shutil.which("curl")
        return curl_path is not None, {"path": curl_path}
    
    def _check_nodejs(self) -> Tuple[bool, Dict[str, Any]]:
        """Check Node.js installation"""
        node_path = shutil.which("node")
        if node_path:
            try:
                result = subprocess.run(["node", "--version"], 
                                      capture_output=True, text=True)
                return True, {
                    "version": result.stdout.strip(),
                    "path": node_path
                }
            except:
                pass
        return False, {"error": "Node.js not found"}
    
    def _check_docker(self) -> Tuple[bool, Dict[str, Any]]:
        """Check Docker installation"""
        docker_path = shutil.which("docker")
        if docker_path:
            try:
                result = subprocess.run(["docker", "--version"], 
                                      capture_output=True, text=True, timeout=5)
                return True, {
                    "version": result.stdout.strip(),
                    "path": docker_path
                }
            except:
                pass
        return False, {"error": "Docker not found"}
    
    def _check_build_tools(self) -> Tuple[bool, Dict[str, Any]]:
        """Check build essential tools"""
        tools = ["gcc", "make", "g++"]
        found_tools = {}
        all_found = True
        
        for tool in tools:
            path = shutil.which(tool)
            found_tools[tool] = path
            if not path:
                all_found = False
        
        return all_found, found_tools
    
    def _check_nvidia_driver(self) -> Tuple[bool, Dict[str, Any]]:
        """Check NVIDIA driver installation"""
        try:
            result = subprocess.run(["nvidia-smi"], capture_output=True, 
                                  text=True, timeout=5)
            return result.returncode == 0, {
                "nvidia_smi_available": result.returncode == 0,
                "gpu_count": len(self.system_info.get("gpu", []))
            }
        except:
            return False, {"error": "nvidia-smi not found"}
    
    def _check_cuda(self) -> Tuple[bool, Dict[str, Any]]:
        """Check CUDA availability"""
        try:
            result = subprocess.run(["nvcc", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0, {
                "nvcc_available": result.returncode == 0,
                "version": result.stdout if result.returncode == 0 else None
            }
        except:
            return False, {"error": "CUDA toolkit not found"}
    
    # Additional check methods
    async def _hardware_check(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Hardware-only check"""
        hardware_reqs = [r for r in self.requirements if "GB" in r.name or "Cores" in r.name]
        results = {"hardware_status": "unknown", "checks": []}
        
        for req in hardware_reqs:
            success, details = req.check_func()
            results["checks"].append({
                "name": req.name,
                "status": "PASS" if success else "FAIL",
                "details": details
            })
        
        all_passed = all(check["status"] == "PASS" for check in results["checks"])
        results["hardware_status"] = "OPTIMAL" if all_passed else "INSUFFICIENT"
        
        return results
    
    async def _software_check(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Software-only check"""
        software_reqs = [r for r in self.requirements if r.name not in ["RAM >= 12GB", "GPU Memory >= 4GB", "Free Disk >= 50GB", "CPU Cores >= 4"]]
        results = {"software_status": "unknown", "checks": [], "install_commands": []}
        
        for req in software_reqs:
            success, details = req.check_func()
            check_result = {
                "name": req.name,
                "status": "PASS" if success else "FAIL",
                "details": details,
                "required": req.required
            }
            results["checks"].append(check_result)
            
            if not success and req.fix_command:
                results["install_commands"].append({
                    "package": req.name,
                    "command": req.fix_command,
                    "required": req.required
                })
        
        required_failed = any(
            check["status"] == "FAIL" and check["required"] 
            for check in results["checks"]
        )
        results["software_status"] = "READY" if not required_failed else "MISSING_REQUIRED"
        
        return results
    
    async def _dependency_check(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Check specific project dependencies"""
        project_type = metadata.get("project_type", "general")
        
        dependencies = {
            "web": ["nodejs", "npm", "git"],
            "mobile": ["java", "android-studio", "gradle"],
            "api": ["python3", "pip", "docker"],
            "general": ["python3", "git", "curl"]
        }
        
        required_deps = dependencies.get(project_type, dependencies["general"])
        
        results = {
            "project_type": project_type,
            "dependency_status": "unknown",
            "missing": [],
            "available": []
        }
        
        for dep in required_deps:
            if shutil.which(dep):
                results["available"].append(dep)
            else:
                results["missing"].append(dep)
        
        results["dependency_status"] = "READY" if not results["missing"] else "INCOMPLETE"
        
        return results
    
    async def _performance_check(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Check system performance metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        results = {
            "performance_status": "unknown",
            "metrics": {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "available_memory_gb": round(memory.available / (1024**3), 1),
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None
            },
            "recommendations": []
        }
        
        # Performance recommendations
        if cpu_percent > 80:
            results["recommendations"].append("⚠️ High CPU usage - consider closing background applications")
        
        if memory.percent > 85:
            results["recommendations"].append("⚠️ High memory usage - free up RAM before running ULTIMA")
        
        if memory.available < 4 * (1024**3):  # Less than 4GB available
            results["recommendations"].append("🔧 Low available memory - restart system or close applications")
        
        # Determine overall performance status
        if cpu_percent < 50 and memory.percent < 70:
            results["performance_status"] = "EXCELLENT"
        elif cpu_percent < 80 and memory.percent < 85:
            results["performance_status"] = "GOOD"
        else:
            results["performance_status"] = "POOR"
        
        return results
    
    async def _gpu_specific_check(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Detailed GPU check for AI workloads"""
        gpu_info = self.system_info.get("gpu", [])
        
        if not gpu_info:
            return {
                "gpu_status": "NOT_AVAILABLE",
                "error": "No NVIDIA GPU detected",
                "recommendations": ["Install NVIDIA drivers", "Check GPU hardware"]
            }
        
        gpu = gpu_info[0]
        memory_gb = gpu["memory_mb"] / 1024
        
        results = {
            "gpu_status": "unknown",
            "gpu_info": gpu,
            "ai_readiness": {},
            "model_recommendations": []
        }
        
        # AI model compatibility
        if memory_gb >= 24:
            results["ai_readiness"]["max_model_size"] = "70B"
            results["model_recommendations"] = ["70B models supported", "All model sizes compatible"]
        elif memory_gb >= 12:
            results["ai_readiness"]["max_model_size"] = "32B Q4"
            results["model_recommendations"] = ["32B Q4 models", "14B all quantizations"]
        elif memory_gb >= 6:
            results["ai_readiness"]["max_model_size"] = "14B Q4"
            results["model_recommendations"] = ["14B Q4/Q5 models only", "Avoid 32B+ models"]
            results["gpu_status"] = "LIMITED_BUT_USABLE"
        else:
            results["ai_readiness"]["max_model_size"] = "7B Q4"
            results["model_recommendations"] = ["7B models only", "Consider upgrading GPU"]
            results["gpu_status"] = "INSUFFICIENT"
        
        if results["gpu_status"] == "unknown":
            results["gpu_status"] = "OPTIMAL"
        
        return results
    
    async def _memory_specific_check(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Detailed memory analysis"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "memory_status": "OPTIMAL" if memory.percent < 70 else "HIGH_USAGE",
            "physical_memory": {
                "total_gb": round(memory.total / (1024**3), 1),
                "available_gb": round(memory.available / (1024**3), 1),
                "used_percent": memory.percent
            },
            "swap_memory": {
                "total_gb": round(swap.total / (1024**3), 1),
                "used_gb": round(swap.used / (1024**3), 1),
                "free_gb": round(swap.free / (1024**3), 1)
            },
            "recommendations": self._get_memory_recommendations(memory, swap)
        }
    
    def _get_memory_recommendations(self, memory, swap) -> List[str]:
        """Get memory-specific recommendations"""
        recommendations = []
        
        memory_gb = memory.total / (1024**3)
        available_gb = memory.available / (1024**3)
        
        if memory_gb <= 16:
            recommendations.append("⚠️ 16GB RAM detected - monitor usage during heavy operations")
        
        if available_gb < 4:
            recommendations.append("🔧 Less than 4GB available - close applications before ULTIMA")
        
        if swap.total == 0:
            recommendations.append("💿 No swap configured - consider adding swap space")
        
        if memory.percent > 80:
            recommendations.append("⚠️ High memory usage - restart or free up RAM")
        
        return recommendations 