class UltimaDashboard {
    constructor() {
        this.currentSection = 'overview';
        this.init();
    }
    
    init() {
        this.setupNavigation();
        this.setupModal();
        this.startRealTimeUpdates();
        this.updateTime();
        this.animateStats();
    }
    
    setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        const sections = document.querySelectorAll('.content-section');
        
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                const sectionId = item.dataset.section;
                this.switchSection(sectionId);
                
                // Update active nav item
                navItems.forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');
            });
        });
    }
    
    switchSection(sectionId) {
        const sections = document.querySelectorAll('.content-section');
        sections.forEach(section => {
            section.classList.remove('active');
        });
        
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
            this.currentSection = sectionId;
        }
    }
    
    setupModal() {
        const newTaskBtn = document.getElementById('newTaskBtn');
        const modal = document.getElementById('newTaskModal');
        const closeBtn = document.getElementById('closeModal');
        const form = document.getElementById('newTaskForm');
        
        newTaskBtn.addEventListener('click', () => {
            modal.classList.add('active');
        });
        
        closeBtn.addEventListener('click', () => {
            modal.classList.remove('active');
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
        
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.createNewTask();
        });
    }
    
    createNewTask() {
        const description = document.getElementById('taskDescription').value;
        const type = document.getElementById('taskType').value;
        const priority = document.getElementById('taskPriority').value;
        
        // Simulate task creation
        this.showNotification(`Task created: ${description}`, 'success');
        
        // Add to recent tasks
        this.addRecentTask(description, 'active');
        
        // Close modal and reset form
        document.getElementById('newTaskModal').classList.remove('active');
        document.getElementById('newTaskForm').reset();
        
        // Update stats
        this.updateTaskStats();
    }
    
    addRecentTask(description, status) {
        const taskList = document.getElementById('recentTasks');
        const taskItem = document.createElement('div');
        taskItem.className = `task-item ${status}`;
        
        const icon = status === 'completed' ? 'fas fa-check-circle' : 'fas fa-spinner fa-spin';
        const time = status === 'completed' ? 'Just now' : 'In progress';
        
        taskItem.innerHTML = `
            <i class="${icon}"></i>
            <span>${description}</span>
            <time>${time}</time>
        `;
        
        taskList.insertBefore(taskItem, taskList.firstChild);
        
        // Keep only last 5 tasks
        const tasks = taskList.children;
        if (tasks.length > 5) {
            taskList.removeChild(tasks[tasks.length - 1]);
        }
    }
    
    updateTime() {
        const timeDisplay = document.getElementById('currentTime');
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        timeDisplay.textContent = timeString;
    }
    
    startRealTimeUpdates() {
        // Update time every second
        setInterval(() => this.updateTime(), 1000);
        
        // Simulate real-time data updates
        setInterval(() => this.updateRealTimeData(), 5000);
        
        // Animate progress bars
        setInterval(() => this.animateProgressBars(), 3000);
    }
    
    updateRealTimeData() {
        // Simulate dynamic data updates
        const tasksCompleted = document.getElementById('tasksCompleted');
        const activeTasks = document.getElementById('activeTasks');
        const activeAgents = document.getElementById('activeAgents');
        
        if (tasksCompleted) {
            const current = parseInt(tasksCompleted.textContent.replace(/,/g, ''));
            tasksCompleted.textContent = (current + Math.floor(Math.random() * 3)).toLocaleString();
        }
        
        if (activeTasks) {
            const current = parseInt(activeTasks.textContent);
            const change = Math.floor(Math.random() * 5) - 2; // -2 to +2
            activeTasks.textContent = Math.max(0, current + change);
        }
    }
    
    animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-fill');
        progressBars.forEach(bar => {
            const currentWidth = parseInt(bar.style.width);
            const variation = Math.floor(Math.random() * 10) - 5; // -5% to +5%
            const newWidth = Math.max(10, Math.min(90, currentWidth + variation));
            bar.style.width = newWidth + '%';
            
            // Update the percentage text
            const metric = bar.closest('.metric');
            const percentText = metric.querySelector('span:last-child');
            if (percentText) {
                percentText.textContent = newWidth + '%';
            }
        });
    }
    
    animateStats() {
        const statCards = document.querySelectorAll('.stat-card');
        statCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }
    
    updateTaskStats() {
        const activeTasks = document.getElementById('activeTasks');
        if (activeTasks) {
            const current = parseInt(activeTasks.textContent);
            activeTasks.textContent = current + 1;
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : 'info'}-circle"></i>
            <span>${message}</span>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? 'rgba(16, 185, 129, 0.9)' : 'rgba(0, 212, 255, 0.9)'};
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 3000;
            backdrop-filter: blur(10px);
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Simulate ULTIMA system status
    simulateSystemActivity() {
        const activities = [
            'Processing web development task...',
            'Analyzing code structure...',
            'Generating responsive layout...',
            'Optimizing performance...',
            'Running system diagnostics...',
            'Updating agent configurations...'
        ];
        
        setInterval(() => {
            const activity = activities[Math.floor(Math.random() * activities.length)];
            console.log(`🤖 ULTIMA: ${activity}`);
        }, 8000);
    }
}

// Add custom CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new UltimaDashboard();
    dashboard.simulateSystemActivity();
    
    console.log('🤖 ULTIMA Dashboard initialized!');
    console.log('🎨 Beautiful UI created by ULTIMA for ULTIMA!');
    console.log('🚀 Self-aware AI designing its own interface!');
});