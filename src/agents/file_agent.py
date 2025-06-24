"""
File Agent - Handles file system operations for ULTIMA framework
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional

from .base_agent import BaseAgent, Task


class FileAgent(BaseAgent):
    """
    Agent responsible for file system operations:
    - File/directory creation, deletion, copying
    - File content manipulation
    - Permission changes
    - Git operations
    """
    
    def __init__(self, name: str, workspace_path: Path):
        super().__init__(name, workspace_path)
        self.safe_zones = [
            workspace_path,
            Path.home() / "Documents",
            Path.home() / "Desktop",
            Path("/tmp")
        ]
    
    def get_capabilities(self) -> List[str]:
        """Return capabilities this agent provides"""
        return [
            "file_create",
            "file_read", 
            "file_write",
            "file_delete",
            "dir_create",
            "dir_delete",
            "file_copy",
            "file_move",
            "file_permissions",
            "git_init",
            "git_add",
            "git_commit",
            "git_push"
        ]
    
    def _is_safe_path(self, path: Path) -> bool:
        """Check if path is in safe zones"""
        try:
            path = path.resolve()
            for safe_zone in self.safe_zones:
                if path.is_relative_to(safe_zone.resolve()):
                    return True
            return False
        except (OSError, ValueError):
            return False
    
    async def execute_task(self, task: Task) -> Optional[Dict[str, Any]]:
        """Execute file system task"""
        task_type = task.type
        metadata = task.metadata
        
        try:
            if task_type == "file_create":
                return await self._create_file(metadata)
            elif task_type == "file_read":
                return await self._read_file(metadata)
            elif task_type == "file_write":
                return await self._write_file(metadata)
            elif task_type == "file_delete":
                return await self._delete_file(metadata)
            elif task_type == "dir_create":
                return await self._create_directory(metadata)
            elif task_type == "dir_delete":
                return await self._delete_directory(metadata)
            elif task_type == "file_copy":
                return await self._copy_file(metadata)
            elif task_type == "file_move":
                return await self._move_file(metadata)
            elif task_type == "file_permissions":
                return await self._change_permissions(metadata)
            elif task_type.startswith("git_"):
                return await self._git_operation(task_type, metadata)
            else:
                self.logger.error(f"Unknown task type: {task_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error executing {task_type}: {str(e)}")
            return None
    
    async def _create_file(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new file"""
        file_path = Path(metadata["path"])
        content = metadata.get("content", "")
        
        if not self._is_safe_path(file_path):
            raise ValueError(f"Path not in safe zone: {file_path}")
        
        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Created file: {file_path}")
        return {
            "path": str(file_path),
            "size": file_path.stat().st_size,
            "created": True
        }
    
    async def _read_file(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Read file content"""
        file_path = Path(metadata["path"])
        
        if not self._is_safe_path(file_path):
            raise ValueError(f"Path not in safe zone: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "path": str(file_path),
            "content": content,
            "size": len(content)
        }
    
    async def _write_file(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Write content to file"""
        file_path = Path(metadata["path"])
        content = metadata["content"]
        mode = metadata.get("mode", "w")  # 'w' for write, 'a' for append
        
        if not self._is_safe_path(file_path):
            raise ValueError(f"Path not in safe zone: {file_path}")
        
        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Updated file: {file_path}")
        return {
            "path": str(file_path),
            "size": file_path.stat().st_size,
            "written": True
        }
    
    async def _delete_file(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a file"""
        file_path = Path(metadata["path"])
        
        if not self._is_safe_path(file_path):
            raise ValueError(f"Path not in safe zone: {file_path}")
        
        if file_path.exists():
            file_path.unlink()
            self.logger.info(f"Deleted file: {file_path}")
            return {"path": str(file_path), "deleted": True}
        else:
            return {"path": str(file_path), "deleted": False, "reason": "not_found"}
    
    async def _create_directory(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create directory"""
        dir_path = Path(metadata["path"])
        
        if not self._is_safe_path(dir_path):
            raise ValueError(f"Path not in safe zone: {dir_path}")
        
        dir_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Created directory: {dir_path}")
        
        return {
            "path": str(dir_path),
            "created": True
        }
    
    async def _delete_directory(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Delete directory"""
        dir_path = Path(metadata["path"])
        
        if not self._is_safe_path(dir_path):
            raise ValueError(f"Path not in safe zone: {dir_path}")
        
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)
            self.logger.info(f"Deleted directory: {dir_path}")
            return {"path": str(dir_path), "deleted": True}
        else:
            return {"path": str(dir_path), "deleted": False, "reason": "not_found"}
    
    async def _copy_file(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Copy file from source to destination"""
        src_path = Path(metadata["source"])
        dst_path = Path(metadata["destination"])
        
        if not self._is_safe_path(src_path) or not self._is_safe_path(dst_path):
            raise ValueError("Source or destination not in safe zone")
        
        # Create destination parent directories
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(src_path, dst_path)
        self.logger.info(f"Copied {src_path} to {dst_path}")
        
        return {
            "source": str(src_path),
            "destination": str(dst_path),
            "copied": True
        }
    
    async def _move_file(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Move file from source to destination"""
        src_path = Path(metadata["source"])
        dst_path = Path(metadata["destination"])
        
        if not self._is_safe_path(src_path) or not self._is_safe_path(dst_path):
            raise ValueError("Source or destination not in safe zone")
        
        # Create destination parent directories
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.move(str(src_path), str(dst_path))
        self.logger.info(f"Moved {src_path} to {dst_path}")
        
        return {
            "source": str(src_path),
            "destination": str(dst_path),
            "moved": True
        }
    
    async def _change_permissions(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Change file permissions"""
        file_path = Path(metadata["path"])
        permissions = metadata["permissions"]  # e.g., 0o755
        
        if not self._is_safe_path(file_path):
            raise ValueError(f"Path not in safe zone: {file_path}")
        
        file_path.chmod(permissions)
        self.logger.info(f"Changed permissions of {file_path} to {oct(permissions)}")
        
        return {
            "path": str(file_path),
            "permissions": oct(permissions),
            "changed": True
        }
    
    async def _git_operation(self, operation: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Handle git operations"""
        repo_path = Path(metadata.get("repo_path", self.workspace_path))
        
        if not self._is_safe_path(repo_path):
            raise ValueError(f"Repository path not in safe zone: {repo_path}")
        
        # Change to repository directory
        original_cwd = os.getcwd()
        os.chdir(repo_path)
        
        try:
            if operation == "git_init":
                result = subprocess.run(["git", "init"], capture_output=True, text=True)
            elif operation == "git_add":
                files = metadata.get("files", ["."])
                cmd = ["git", "add"] + files
                result = subprocess.run(cmd, capture_output=True, text=True)
            elif operation == "git_commit":
                message = metadata.get("message", "Automated commit")
                result = subprocess.run(
                    ["git", "commit", "-m", message], 
                    capture_output=True, text=True
                )
            elif operation == "git_push":
                remote = metadata.get("remote", "origin")
                branch = metadata.get("branch", "main")
                result = subprocess.run(
                    ["git", "push", remote, branch], 
                    capture_output=True, text=True
                )
            else:
                raise ValueError(f"Unknown git operation: {operation}")
            
            self.logger.info(f"Git operation {operation} completed")
            
            return {
                "operation": operation,
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        finally:
            os.chdir(original_cwd) 