#!/usr/bin/env python3
"""
ULTIMA Real-time Web Dashboard
Flask-based web interface for ULTIMA monitoring and task management
"""

import os
import json
import glob
import uuid
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory
from pathlib import Path
import subprocess
import threading
import time
import psutil

app = Flask(__name__)

# Configuration
ULTIMA_ROOT = Path(__file__).parent
TASKS_DIR = ULTIMA_ROOT / "tasks"
LOGS_DIR = ULTIMA_ROOT / "logs"
DETECTED_TASKS_DIR = ULTIMA_ROOT / "detected_tasks"

def get_ultima_status():
    """More reliable check if ULTIMA is running (uses psutil)."""
    for proc in psutil.process_iter(attrs=['pid', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info.get('cmdline') or [])
            if 'ultima_runner.py' in cmdline:
                return {'running': True, 'pid': proc.info['pid']}
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return {'running': False, 'pid': None}

def get_all_tasks():
    """Get all tasks from all agents"""
    tasks = []
    
    # Get tasks from task directories
    if TASKS_DIR.exists():
        for agent_dir in TASKS_DIR.iterdir():
            if agent_dir.is_dir():
                agent_name = agent_dir.name
                for task_file in agent_dir.glob("*.json"):
                    try:
                        with open(task_file, 'r') as f:
                            task_data = json.load(f)
                            task_data['agent'] = agent_name
                            task_data['source'] = 'executed'
                            tasks.append(task_data)
                    except:
                        continue
    
    # Get detected tasks (from cursor bridge)
    if DETECTED_TASKS_DIR.exists():
        for task_file in DETECTED_TASKS_DIR.glob("*.json"):
            try:
                with open(task_file, 'r') as f:
                    task_data = json.load(f)
                    task_data['source'] = 'detected'
                    task_data['agent'] = 'pending'
                    tasks.append(task_data)
            except:
                continue
    
    # Sort by timestamp (handle mixed string/float timestamps)
    def safe_timestamp(task):
        timestamp = task.get('created_at', task.get('timestamp', ''))
        if isinstance(timestamp, (int, float)):
            return timestamp
        elif isinstance(timestamp, str) and timestamp:
            try:
                from datetime import datetime
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00')).timestamp()
            except:
                return 0
        return 0
    
    tasks.sort(key=safe_timestamp, reverse=True)
    return tasks

def get_system_stats():
    """Get system statistics"""
    tasks = get_all_tasks()
    
    status_counts = {}
    agent_counts = {}
    type_counts = {}
    
    for task in tasks:
        # Status counts
        status = task.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Agent counts
        agent = task.get('agent', 'unknown')
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        # Type counts
        task_type = task.get('type', task.get('task_type', 'unknown'))
        type_counts[task_type] = type_counts.get(task_type, 0) + 1
    
    return {
        'total_tasks': len(tasks),
        'status_counts': status_counts,
        'agent_counts': agent_counts,
        'type_counts': type_counts,
        'ultima_status': get_ultima_status()
    }

def create_task_from_dashboard(description, task_type, priority):
    """Create a new task from dashboard input"""
    task_id = str(uuid.uuid4())
    task_data = {
        'id': task_id,
        'description': description,
        'task_type': task_type,
        'priority': priority,
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'source': 'dashboard'
    }
    
    # Save to detected_tasks for ULTIMA to pick up
    DETECTED_TASKS_DIR.mkdir(exist_ok=True)
    task_file = DETECTED_TASKS_DIR / f"task_{task_id[:12]}.json"
    
    with open(task_file, 'w') as f:
        json.dump(task_data, f, indent=2)
    
    return task_data

# Routes
@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify(get_system_stats())

@app.route('/api/tasks')
def api_tasks():
    """API endpoint for all tasks"""
    tasks = get_all_tasks()
    return jsonify(tasks)

@app.route('/api/tasks/create', methods=['POST'])
def api_create_task():
    """API endpoint to create new task"""
    data = request.json
    task = create_task_from_dashboard(
        data.get('description', ''),
        data.get('type', 'general'),
        data.get('priority', 'medium')
    )
    return jsonify(task)

@app.route('/api/ultima/start', methods=['POST'])
def api_start_ultima():
    """Start ULTIMA process"""
    try:
        # Start ULTIMA in background and capture logs
        logs_dir = LOGS_DIR
        logs_dir.mkdir(exist_ok=True)
        log_file = logs_dir / 'ultima_runner.log'

        with open(log_file, 'a') as lf:
            subprocess.Popen(
                ['python3', 'src/ultima_runner.py'],
                cwd=ULTIMA_ROOT,
                stdout=lf,
                stderr=subprocess.STDOUT,
                start_new_session=True  # prevent signal propagation
            )
        time.sleep(2)  # Give it time to start
        return jsonify({'success': True, 'message': 'ULTIMA started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/ultima/stop', methods=['POST'])
def api_stop_ultima():
    """Stop ULTIMA process"""
    try:
        subprocess.run(['pkill', '-f', 'ultima_runner'])
        return jsonify({'success': True, 'message': 'ULTIMA stopped'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/task/<task_id>')
def api_task_detail(task_id):
    """Return details for a single task"""
    for task in get_all_tasks():
        if task.get('id') == task_id:
            return jsonify(task)
    return jsonify({'error': 'task not found'}), 404

@app.route('/api/task/<task_id>/log')
def api_task_log(task_id):
    """Return last 100 lines of related agent log if available"""
    # find task and agent
    agent_name = None
    for task in get_all_tasks():
        if task.get('id') == task_id:
            agent_name = task.get('agent')
            break
    if not agent_name or agent_name == 'pending':
        return jsonify({'log': []})
    # log path heuristic
    possible_paths = [
        LOGS_DIR / f"{agent_name}.log",
        LOGS_DIR / agent_name / f"{agent_name}.log"
    ]
    log_lines = []
    for p in possible_paths:
        if p.exists():
            with open(p, 'r') as f:
                log_lines = f.readlines()[-100:]
            break
    # Fallback to global runner log if agent-specific log not found
    if not log_lines:
        global_log = LOGS_DIR / 'ultima_runner.log'
        if global_log.exists():
            with open(global_log, 'r') as f:
                log_lines = f.readlines()[-100:]
    return jsonify({'log': log_lines})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    
    print("🚀 Starting ULTIMA Web Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🔄 Real-time task monitoring enabled")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 