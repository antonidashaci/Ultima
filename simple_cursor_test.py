#!/usr/bin/env python3
"""
Simple Cursor Task Detection Test
"""

import sys
sys.path.append('.')

from pathlib import Path
from src.cursor_bridge.task_detector import CursorTaskDetector, TaskDefinition

def test_task_parsing():
    """Test the task parsing directly"""
    
    print("🧪 Testing Task Parsing...")
    
    # Test cases
    test_cases = [
        "# #AI_TASK: Create a simple website",
        "// #AI_TASK: Build Android game [priority:high]",
        "# #AI_TASK: Create REST API for todo management [type:api_development] [priority:medium]"
    ]
    
    for i, test_line in enumerate(test_cases):
        print(f"\n📝 Test {i+1}: {test_line}")
        
        task_def = TaskDefinition(test_line, Path("test.py"), i+1)
        
        if task_def.parsed_data:
            print(f"   ✅ Parsed successfully")
            print(f"   📋 Description: {task_def.parsed_data['description']}")
            print(f"   🏷️  Type: {task_def.parsed_data['type']}")
            print(f"   ⚡ Priority: {task_def.parsed_data['priority']}")
        else:
            print(f"   ❌ Failed to parse")

def test_file_detection():
    """Test file-based detection"""
    
    print("\n🔍 Testing File Detection...")
    
    # Create test file
    test_file = Path("test_cursor_task.py")
    test_content = '''#!/usr/bin/env python3
"""
Test file for cursor task detection
"""

# #AI_TASK: Create a file manager utility [priority:medium] [type:file_operations]

def main():
    print("Test file")

if __name__ == "__main__":
    main()
'''
    
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    print(f"✅ Created test file: {test_file}")
    
    # Test detection
    workspace = Path.cwd()
    output_dir = workspace / "detected_tasks"
    
    detector = CursorTaskDetector(workspace, output_dir)
    tasks = detector._scan_file(test_file)
    
    print(f"📊 Found {len(tasks)} tasks")
    
    for task in tasks:
        print(f"   📋 Task: {task.parsed_data.get('description', 'No description')}")
        print(f"   🏷️  Type: {task.parsed_data.get('type', 'No type')}")
        print(f"   🆔 ID: {task.task_id}")
    
    # Cleanup
    if test_file.exists():
        test_file.unlink()
    
    return len(tasks) > 0

if __name__ == "__main__":
    print("🚀 Simple Cursor Task Detection Test")
    print("=" * 40)
    
    test_task_parsing()
    success = test_file_detection()
    
    if success:
        print("\n🎉 Task detection is WORKING!")
    else:
        print("\n❌ Task detection FAILED!") 