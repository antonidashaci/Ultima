#!/usr/bin/env python3
"""
ULTIMA Real-time Monitor
Shows current status, active tasks, and system health
"""

import os
import json
import time
import glob
from datetime import datetime
from pathlib import Path
import argparse

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_latest_tasks(limit=10):
    """Get latest tasks from all agents"""
    tasks = []
    task_dirs = glob.glob("tasks/*/")
    
    for task_dir in task_dirs:
        agent_name = os.path.basename(task_dir.rstrip('/'))
        task_files = glob.glob(f"{task_dir}*.json")
        
        for task_file in task_files:
            try:
                with open(task_file, 'r') as f:
                    task_data = json.load(f)
                    task_data['agent'] = agent_name
                    tasks.append(task_data)
            except:
                continue
    
    # Sort by created_at timestamp
    tasks.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return tasks[:limit]

def get_system_status():
    """Get current system status"""
    # Check if ULTIMA is running
    import subprocess
    try:
        result = subprocess.run(['pgrep', '-f', 'ultima_runner'], 
                              capture_output=True, text=True)
        is_running = bool(result.stdout.strip())
        pid = result.stdout.strip() if is_running else None
    except:
        is_running = False
        pid = None
    
    # Count tasks by status
    tasks = get_latest_tasks(100)  # Get more for counting
    status_counts = {}
    agent_counts = {}
    
    for task in tasks:
        status = task.get('status', 'unknown')
        agent = task.get('agent', 'unknown')
        
        status_counts[status] = status_counts.get(status, 0) + 1
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
    
    return {
        'is_running': is_running,
        'pid': pid,
        'total_tasks': len(tasks),
        'status_counts': status_counts,
        'agent_counts': agent_counts
    }

def format_timestamp(timestamp_str):
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%H:%M:%S')
    except:
        return timestamp_str

def display_status():
    """Display current ULTIMA status"""
    clear_screen()
    
    print("=" * 80)
    print("🚀 ULTIMA Real-time Monitor")
    print("=" * 80)
    print(f"⏰ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # System Status
    status = get_system_status()
    
    if status['is_running']:
        print(f"🟢 ULTIMA Status: RUNNING (PID: {status['pid']})")
    else:
        print("🔴 ULTIMA Status: STOPPED")
    
    print(f"📊 Total Tasks: {status['total_tasks']}")
    print()
    
    # Status breakdown
    if status['status_counts']:
        print("📈 Task Status Breakdown:")
        for status_name, count in status['status_counts'].items():
            emoji = {
                'completed': '✅',
                'in_progress': '⏳',
                'pending': '⏸️',
                'failed': '❌'
            }.get(status_name, '❓')
            print(f"   {emoji} {status_name.title()}: {count}")
        print()
    
    # Agent breakdown
    if status['agent_counts']:
        print("🤖 Active Agents:")
        for agent_name, count in status['agent_counts'].items():
            print(f"   🔧 {agent_name}: {count} tasks")
        print()
    
    # Recent tasks
    print("📋 Recent Tasks (Last 10):")
    print("-" * 80)
    tasks = get_latest_tasks(10)
    
    if not tasks:
        print("   No tasks found")
    else:
        for i, task in enumerate(tasks, 1):
            status_emoji = {
                'completed': '✅',
                'in_progress': '⏳',
                'pending': '⏸️',
                'failed': '❌'
            }.get(task.get('status'), '❓')
            
            time_str = format_timestamp(task.get('created_at', ''))
            agent_name = task.get('agent', 'unknown')
            description = task.get('description', 'No description')[:50]
            
            print(f"   {i:2d}. {status_emoji} [{time_str}] {agent_name}: {description}")
    
    print()
    print("=" * 80)
    print("Press Ctrl+C to exit | Refreshes every 3 seconds")

def main():
    """Main monitoring loop"""
    parser = argparse.ArgumentParser(description="ULTIMA real-time monitor")
    parser.add_argument("--once", action="store_true", help="Print one snapshot and exit")
    args = parser.parse_args()

    try:
        while True:
            display_status()
            if args.once:
                break
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped")

if __name__ == "__main__":
    main() 