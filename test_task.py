#!/usr/bin/env python3
"""
Test task creator for ULTIMA
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

def create_test_task():
    """Create a test task for ULTIMA"""
    
    # Create detected_tasks directory if it doesn't exist
    detected_tasks_dir = Path("detected_tasks")
    detected_tasks_dir.mkdir(exist_ok=True)
    
    # Create a test task
    task_id = str(uuid.uuid4())
    task_data = {
        'id': task_id,
        'description': 'Create a simple Python calculator script',
        'task_type': 'file_create',
        'priority': 'high',
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'source': 'test_script'
    }
    
    # Save task file
    task_file = detected_tasks_dir / f"task_{task_id[:12]}.json"
    with open(task_file, 'w') as f:
        json.dump(task_data, f, indent=2)
    
    print(f"✅ Test task created: {task_file}")
    print(f"📋 Task ID: {task_id}")
    print(f"📝 Description: {task_data['description']}")
    
    return task_data

if __name__ == "__main__":
    create_test_task() 