"""
Cursor Task Detector - Monitors workspace for AI task definitions
Parses special comments like: // #AI_TASK: Create a simple website
"""

import re
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging


class TaskDefinition:
    """Represents a parsed task from Cursor comments"""
    
    def __init__(self, raw_text: str, file_path: Path, line_number: int):
        self.raw_text = raw_text
        self.file_path = file_path
        self.line_number = line_number
        self.task_id = self._generate_task_id()
        self.parsed_data = self._parse_task()
    
    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        import hashlib
        content = f"{self.file_path}:{self.line_number}:{self.raw_text}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _parse_task(self) -> Dict[str, Any]:
        """Parse task comment into structured data"""
        # Match patterns like:
        # // #AI_TASK: Create a simple website
        # // #AI_TASK: Build Android game [priority:high] [type:mobile]
        
        # Basic task extraction
        task_match = re.search(r'#AI_TASK:\s*([^[\n]+)', self.raw_text)
        if not task_match:
            return {}
        
        description = task_match.group(1).strip()
        
        # Extract optional parameters in brackets
        params = {}
        param_matches = re.findall(r'\[(\w+):([^\]]+)\]', self.raw_text)
        for key, value in param_matches:
            params[key] = value.strip()
        
        # Infer task type from description
        task_type = self._infer_task_type(description, params.get('type'))
        
        return {
            "description": description,
            "type": task_type,
            "priority": params.get('priority', 'medium'),
            "metadata": {
                "source_file": str(self.file_path),
                "source_line": self.line_number,
                "raw_comment": self.raw_text,
                **params
            }
        }
    
    def _infer_task_type(self, description: str, explicit_type: Optional[str]) -> str:
        """Infer task type from description"""
        if explicit_type:
            return explicit_type
        
        description_lower = description.lower()
        
        # Web development patterns
        if any(word in description_lower for word in ['website', 'webpage', 'landing', 'portfolio', 'html', 'css']):
            return 'web_development'
        
        # Mobile development patterns
        if any(word in description_lower for word in ['android', 'app', 'mobile', 'game', 'apk']):
            return 'mobile_development'
        
        # API development patterns
        if any(word in description_lower for word in ['api', 'rest', 'endpoint', 'server', 'backend']):
            return 'api_development'
        
        # Desktop application patterns
        if any(word in description_lower for word in ['desktop', 'gui', 'application', 'tool']):
            return 'desktop_development'
        
        # File operations
        if any(word in description_lower for word in ['file', 'folder', 'organize', 'backup']):
            return 'file_operations'
        
        # Default to general development
        return 'general_development'


class CursorTaskDetector(FileSystemEventHandler):
    """
    Monitors Cursor workspace for AI task definitions.
    Watches for file changes and scans for #AI_TASK comments.
    """
    
    def __init__(self, workspace_path: Path, output_dir: Path):
        self.workspace_path = workspace_path
        self.output_dir = output_dir
        self.logger = logging.getLogger("ultima.cursor_detector")
        
        # File patterns to monitor
        self.monitored_extensions = {'.py', '.js', '.ts', '.md', '.txt', '.java', '.kt', '.go', '.rs'}
        
        # Processed tasks to avoid duplicates
        self.processed_tasks: Set[str] = set()
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initial scan of existing files
        self._scan_existing_files()
    
    def _scan_existing_files(self):
        """Scan existing files for task definitions on startup"""
        self.logger.info("Scanning existing files for AI tasks...")
        
        for file_path in self.workspace_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.monitored_extensions:
                self._scan_file(file_path)
    
    def _scan_file(self, file_path: Path) -> List[TaskDefinition]:
        """Scan a single file for task definitions"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            found_tasks = []
            for line_num, line in enumerate(lines, 1):
                if '#AI_TASK:' in line:
                    task_def = TaskDefinition(line.strip(), file_path, line_num)
                    
                    # Skip if already processed
                    if task_def.task_id not in self.processed_tasks:
                        found_tasks.append(task_def)
                        self._write_task_file(task_def)
                        self.processed_tasks.add(task_def.task_id)
                        
                        self.logger.info(f"Found new AI task: {task_def.parsed_data['description']}")
            
            return found_tasks
            
        except Exception as e:
            self.logger.error(f"Error scanning file {file_path}: {e}")
            return []
    
    def _write_task_file(self, task_def: TaskDefinition):
        """Write task definition to output directory"""
        task_data = {
            "id": task_def.task_id,
            "status": "pending",
            "created_at": time.time(),
            **task_def.parsed_data
        }
        
        output_file = self.output_dir / f"task_{task_def.task_id}.json"
        with open(output_file, 'w') as f:
            json.dump(task_data, f, indent=2)
        
        self.logger.info(f"Created task file: {output_file}")
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix in self.monitored_extensions:
            self._scan_file(file_path)
    
    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix in self.monitored_extensions:
            self._scan_file(file_path)
    
    def start_monitoring(self):
        """Start monitoring the workspace"""
        observer = Observer()
        observer.schedule(self, str(self.workspace_path), recursive=True)
        observer.start()
        
        self.logger.info(f"Started monitoring {self.workspace_path} for AI tasks")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        
        observer.join()


def main():
    """Test the task detector"""
    workspace = Path.cwd()
    output_dir = workspace / "detected_tasks"
    
    detector = CursorTaskDetector(workspace, output_dir)
    detector.start_monitoring()


if __name__ == "__main__":
    main() 