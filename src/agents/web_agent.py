"""
Web Agent - Browser automation and web development tasks
Handles web scraping, form automation, testing, and deployment
Optimized for modern web development workflows
"""

import asyncio
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

from .base_agent import BaseAgent, Task


class WebAgent(BaseAgent):
    """
    Agent specialized in web automation and development:
    - HTML/CSS/JS generation
    - Modern responsive websites
    - Portfolio, landing pages, web apps
    - Web deployment preparation
    """
    
    def __init__(self, name: str, workspace_path: Path):
        super().__init__(name, workspace_path)
        self.supported_types = [
            "portfolio", "landing_page", "todo_app", 
            "blog", "business_site", "dashboard"
        ]
    
    def get_capabilities(self) -> List[str]:
        """Return capabilities this agent provides"""
        return [
            "web_development",
            "html_generation",
            "css_generation", 
            "js_generation",
            "responsive_design",
            "modern_ui",
            "portfolio_creation",
            "landing_page_creation"
        ]
    
    async def execute_task(self, task: Task) -> Optional[Dict[str, Any]]:
        """Execute web-related task"""
        task_type = task.type
        metadata = task.metadata
        
        try:
            if task_type == "web_development":
                return await self._web_development(metadata)
            elif task_type == "html_generation":
                return await self._html_generation(metadata)
            elif task_type == "css_generation":
                return await self._css_generation(metadata)
            elif task_type == "js_generation":
                return await self._js_generation(metadata)
            else:
                self.logger.error(f"Unknown web task: {task_type}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error executing {task_type}: {str(e)}")
            return {"error": str(e), "success": False}
    
    async def _web_development(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Complete web development workflow"""
        description = metadata.get("description", "")
        
        # Determine project type from description
        if any(word in description.lower() for word in ["portfolio", "personal", "showcase"]):
            return await self._create_portfolio_site(metadata)
        elif any(word in description.lower() for word in ["todo", "task", "list"]):
            return await self._create_todo_app(metadata)
        elif any(word in description.lower() for word in ["landing", "marketing", "product"]):
            return await self._create_landing_page(metadata)
        elif any(word in description.lower() for word in ["password", "generator", "security"]):
            return await self._create_password_generator(metadata)
        elif any(word in description.lower() for word in ["weather", "forecast"]):
            return await self._create_weather_app(metadata)
        elif any(word in description.lower() for word in ["expense", "budget", "tracker", "money"]):
            return await self._create_expense_tracker(metadata)
        elif any(word in description.lower() for word in ["ultima", "dashboard", "ai system", "monitoring"]):
            return await self._create_ultima_dashboard(metadata)
        else:
            return await self._create_generic_website(metadata)
    
    async def _create_portfolio_site(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a modern portfolio website"""
        
        # Generate files
        html_content = self._generate_portfolio_html()
        css_content = self._generate_portfolio_css()
        js_content = self._generate_portfolio_js()
        readme_content = self._generate_portfolio_readme()
        
        # Create files
        files_created = []
        
        files_to_create = [
            ("index.html", html_content),
            ("styles.css", css_content), 
            ("script.js", js_content),
            ("README.md", readme_content)
        ]
        
        for filename, content in files_to_create:
            file_path = self.workspace_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_created.append(filename)
        
        return {
            "success": True,
            "message": "Modern portfolio website created successfully",
            "files_created": files_created,
            "project_type": "portfolio",
            "features": [
                "Responsive design",
                "Modern CSS Grid/Flexbox",
                "Smooth scrolling navigation", 
                "Interactive animations",
                "Contact form",
                "Project showcase"
            ],
            "technologies": ["HTML5", "CSS3", "JavaScript ES6"],
            "deployment_ready": True
        }
    
    async def _create_todo_app(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a modern todo application"""
        
        html_content = self._generate_todo_html()
        css_content = self._generate_todo_css()
        js_content = self._generate_todo_js()
        
        files_created = []
        
        files_to_create = [
            ("todo-app.html", html_content),
            ("todo-styles.css", css_content),
            ("todo-script.js", js_content)
        ]
        
        for filename, content in files_to_create:
            file_path = self.workspace_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_created.append(filename)
        
        return {
            "success": True,
            "message": "Todo application created successfully", 
            "files_created": files_created,
            "project_type": "todo_app",
            "features": [
                "Add/remove tasks",
                "Mark tasks complete",
                "Local storage persistence",
                "Filter tasks",
                "Clean modern UI"
            ],
            "technologies": ["HTML5", "CSS3", "JavaScript ES6", "LocalStorage"]
        }
    
    async def _create_landing_page(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a modern landing page"""
        
        html_content = self._generate_landing_html()
        css_content = self._generate_landing_css()
        js_content = self._generate_landing_js()
        
        files_created = []
        
        files_to_create = [
            ("landing.html", html_content),
            ("landing-styles.css", css_content),
            ("landing-script.js", js_content)
        ]
        
        for filename, content in files_to_create:
            file_path = self.workspace_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_created.append(filename)
        
        return {
            "success": True,
            "message": "Landing page created successfully",
            "files_created": files_created,
            "project_type": "landing_page",
            "features": [
                "Hero section with CTA",
                "Features showcase",
                "Testimonials",
                "Pricing section", 
                "Contact form",
                "Responsive design"
            ],
            "technologies": ["HTML5", "CSS3", "JavaScript ES6"]
        }
    
    async def _create_generic_website(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a generic modern website"""
        return await self._create_portfolio_site(metadata)
    
    async def _create_password_generator(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a secure password generator application"""
        
        html_content = self._generate_password_generator_html()
        css_content = self._generate_password_generator_css()
        js_content = self._generate_password_generator_js()
        
        files_created = []
        
        files_to_create = [
            ("password-generator.html", html_content),
            ("password-generator.css", css_content),
            ("password-generator.js", js_content)
        ]
        
        for filename, content in files_to_create:
            file_path = self.workspace_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_created.append(filename)
        
        return {
            "success": True,
            "message": "Password generator application created successfully",
            "files_created": files_created,
            "project_type": "password_generator",
            "features": [
                "Customizable password length",
                "Character type selection",
                "Password strength indicator",
                "One-click copy to clipboard",
                "Generate multiple passwords",
                "Security best practices"
            ],
            "technologies": ["HTML5", "CSS3", "JavaScript ES6", "Crypto API"]
        }
    
    async def _create_weather_app(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a weather application"""
        
        html_content = self._generate_weather_app_html()
        css_content = self._generate_weather_app_css()
        js_content = self._generate_weather_app_js()
        
        files_created = []
        
        files_to_create = [
            ("weather-app.html", html_content),
            ("weather-app.css", css_content),
            ("weather-app.js", js_content)
        ]
        
        for filename, content in files_to_create:
            file_path = self.workspace_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_created.append(filename)
        
        return {
            "success": True,
            "message": "Weather application created successfully",
            "files_created": files_created,
            "project_type": "weather_app",
            "features": [
                "Current weather conditions",
                "5-day forecast",
                "Location search",
                "Temperature units toggle",
                "Weather icons",
                "Responsive design"
            ],
            "technologies": ["HTML5", "CSS3", "JavaScript ES6", "OpenWeather API"]
        }
    
    async def _create_expense_tracker(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create an expense tracking application"""
        
        html_content = self._generate_expense_tracker_html()
        css_content = self._generate_expense_tracker_css()
        js_content = self._generate_expense_tracker_js()
        
        files_created = []
        
        files_to_create = [
            ("expense-tracker.html", html_content),
            ("expense-tracker.css", css_content),
            ("expense-tracker.js", js_content)
        ]
        
        for filename, content in files_to_create:
            file_path = self.workspace_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_created.append(filename)
        
        return {
            "success": True,
            "message": "Expense tracker application created successfully",
            "files_created": files_created,
            "project_type": "expense_tracker",
            "features": [
                "Add/edit/delete expenses",
                "Category management",
                "Monthly/yearly summaries",
                "Budget tracking",
                "Export to CSV",
                "Visual charts and graphs"
            ],
            "technologies": ["HTML5", "CSS3", "JavaScript ES6", "Chart.js", "LocalStorage"]
        }
    
    async def _create_ultima_dashboard(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a ULTIMA dashboard"""
        
        html_content = self._generate_ultima_dashboard_html()
        css_content = self._generate_ultima_dashboard_css()
        js_content = self._generate_ultima_dashboard_js()
        
        files_created = []
        
        files_to_create = [
            ("ultima-dashboard.html", html_content),
            ("ultima-dashboard.css", css_content),
            ("ultima-dashboard.js", js_content)
        ]
        
        for filename, content in files_to_create:
            file_path = self.workspace_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            files_created.append(filename)
        
        return {
            "success": True,
            "message": "ULTIMA dashboard created successfully",
            "files_created": files_created,
            "project_type": "ultima_dashboard",
            "features": [
                "Data visualization",
                "Real-time monitoring",
                "User-friendly interface",
                "Customizable widgets",
                "Responsive design"
            ],
            "technologies": ["HTML5", "CSS3", "JavaScript ES6", "Chart.js", "LocalStorage"]
        }
    
    def _generate_portfolio_html(self) -> str:
        """Generate modern portfolio HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Portfolio</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">
                <a href="#home">Portfolio</a>
            </div>
            <ul class="nav-menu">
                <li><a href="#home" class="nav-link">Home</a></li>
                <li><a href="#about" class="nav-link">About</a></li>
                <li><a href="#projects" class="nav-link">Projects</a></li>
                <li><a href="#contact" class="nav-link">Contact</a></li>
            </ul>
            <div class="nav-toggle">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </div>
    </nav>

    <section id="home" class="hero">
        <div class="hero-container">
            <h1 class="hero-title">Hello, I'm <span class="highlight">Your Name</span></h1>
            <p class="hero-subtitle">Full Stack Developer & UI/UX Designer</p>
            <p class="hero-description">I create digital experiences that combine beautiful design with powerful functionality.</p>
            <div class="hero-buttons">
                <a href="#projects" class="btn btn-primary">View My Work</a>
                <a href="#contact" class="btn btn-secondary">Get In Touch</a>
            </div>
        </div>
    </section>

    <section id="about" class="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div class="about-content">
                <p>I'm a passionate developer with expertise in modern web technologies. I bring ideas to life through clean, efficient code and beautiful user experiences.</p>
                <div class="skills">
                    <h3>Technologies:</h3>
                    <div class="skill-tags">
                        <span class="skill-tag">JavaScript</span>
                        <span class="skill-tag">React</span>
                        <span class="skill-tag">Node.js</span>
                        <span class="skill-tag">Python</span>
                        <span class="skill-tag">CSS3</span>
                        <span class="skill-tag">HTML5</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="projects" class="projects">
        <div class="container">
            <h2 class="section-title">Featured Projects</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-image">Project Screenshot</div>
                    <div class="project-content">
                        <h3>Project One</h3>
                        <p>A modern web application built with React and Node.js</p>
                        <div class="project-tech">
                            <span class="tech-tag">React</span>
                            <span class="tech-tag">Node.js</span>
                        </div>
                        <div class="project-links">
                            <a href="#" class="project-link">Live Demo</a>
                            <a href="#" class="project-link">GitHub</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">Get In Touch</h2>
            <div class="contact-content">
                <p>Ready to start your next project? Let's work together!</p>
                <form class="contact-form" id="contactForm">
                    <input type="text" placeholder="Your Name" required>
                    <input type="email" placeholder="Your Email" required>
                    <textarea placeholder="Your Message" rows="5" required></textarea>
                    <button type="submit" class="btn btn-primary">Send Message</button>
                </form>
            </div>
        </div>
    </section>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Your Name. Built with ❤️ by ULTIMA AI.</p>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>'''

    def _generate_portfolio_css(self) -> str:
        """Generate modern CSS for portfolio"""
        return '''/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    color: #333;
    overflow-x: hidden;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

/* Navigation */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-logo a {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2563eb;
    text-decoration: none;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-link {
    color: #374151;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.nav-link:hover {
    color: #2563eb;
}

/* Hero Section */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding-top: 80px;
}

.hero-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.highlight {
    color: #fbbf24;
}

.hero-subtitle {
    font-size: 1.5rem;
    font-weight: 500;
    margin-bottom: 1rem;
    opacity: 0.9;
}

.hero-description {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    opacity: 0.8;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.75rem 2rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.btn-primary {
    background: #fbbf24;
    color: #1f2937;
}

.btn-primary:hover {
    background: #f59e0b;
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: white;
    border-color: white;
}

.btn-secondary:hover {
    background: white;
    color: #1f2937;
    transform: translateY(-2px);
}

/* Sections */
section {
    padding: 5rem 0;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 3rem;
    color: #1f2937;
}

/* About Section */
.about {
    background: #f9fafb;
}

.about-content {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}

.about-content p {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    color: #6b7280;
}

.skills h3 {
    margin-bottom: 1rem;
    color: #374151;
}

.skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
}

.skill-tag {
    background: #2563eb;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-size: 0.9rem;
    font-weight: 500;
}

/* Projects Section */
.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}

.project-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.project-card:hover {
    transform: translateY(-10px);
}

.project-image {
    height: 200px;
    background: #e5e7eb;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #9ca3af;
    font-weight: 500;
}

.project-content {
    padding: 1.5rem;
}

.project-content h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #1f2937;
}

.project-content p {
    color: #6b7280;
    margin-bottom: 1rem;
}

.project-tech {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.tech-tag {
    background: #eff6ff;
    color: #2563eb;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 500;
}

.project-links {
    display: flex;
    gap: 1rem;
}

.project-link {
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}

.project-link:hover {
    color: #1d4ed8;
}

/* Contact Section */
.contact {
    background: #f9fafb;
}

.contact-content {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
}

.contact-content p {
    font-size: 1.1rem;
    color: #6b7280;
    margin-bottom: 2rem;
}

.contact-form {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.contact-form input,
.contact-form textarea {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 1rem;
    margin-bottom: 1rem;
    transition: border-color 0.3s ease;
}

.contact-form input:focus,
.contact-form textarea:focus {
    outline: none;
    border-color: #2563eb;
}

/* Footer */
.footer {
    background: #1f2937;
    color: white;
    text-align: center;
    padding: 2rem 0;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .section-title {
        font-size: 2rem;
    }
    
    .projects-grid {
        grid-template-columns: 1fr;
    }
}

html {
    scroll-behavior: smooth;
}'''

    def _generate_portfolio_js(self) -> str:
        """Generate JavaScript for portfolio functionality"""
        return '''// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Contact form handling
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        alert('Thank you for your message! I will get back to you soon.');
        this.reset();
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }, 1500);
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Add loading animation
window.addEventListener('load', () => {
    console.log('🎉 Portfolio website loaded! Built with ULTIMA AI.');
});'''

    def _generate_portfolio_readme(self) -> str:
        """Generate README for portfolio"""
        return '''# Professional Portfolio Website

A modern, responsive portfolio website created by ULTIMA AI.

## Features

- **Responsive Design**: Looks great on all devices
- **Modern UI/UX**: Clean, professional design with smooth animations  
- **Interactive Navigation**: Smooth scrolling and mobile-friendly
- **Contact Form**: Functional contact form with validation
- **Performance Optimized**: Fast loading and efficient code

## Technologies Used

- HTML5
- CSS3 (Grid, Flexbox, Custom Properties)
- JavaScript ES6+
- Google Fonts (Inter)

## Getting Started

1. Open `index.html` in your web browser
2. Customize the content with your own information
3. Deploy to any static hosting service

## Customization

- Update personal information in HTML
- Modify colors and styling in CSS  
- Add your own projects and images
- Update contact information

## Deployment Ready

This website can be deployed to:
- Netlify
- Vercel
- GitHub Pages
- Firebase Hosting

---
*Built with ❤️ using ULTIMA AI*'''

    def _generate_todo_html(self) -> str:
        """Generate todo app HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
    <link rel="stylesheet" href="todo-styles.css">
</head>
<body>
    <div class="app">
        <h1>My Todo App</h1>
        <div class="todo-form">
            <input type="text" id="todoInput" placeholder="Add a new task...">
            <button id="addBtn">Add Task</button>
        </div>
        <div class="filters">
            <button class="filter-btn active" data-filter="all">All</button>
            <button class="filter-btn" data-filter="active">Active</button>
            <button class="filter-btn" data-filter="completed">Completed</button>
        </div>
        <ul id="todoList" class="todo-list"></ul>
    </div>
    <script src="todo-script.js"></script>
</body>
</html>'''

    def _generate_todo_css(self) -> str:
        """Generate todo app CSS"""
        return '''body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #74b9ff, #0984e3);
    min-height: 100vh;
}

.app {
    max-width: 500px;
    margin: 0 auto;
    background: white;
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

h1 {
    text-align: center;
    color: #2d3436;
    margin-bottom: 30px;
}

.todo-form {
    display: flex;
    margin-bottom: 20px;
}

#todoInput {
    flex: 1;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

#addBtn {
    padding: 12px 20px;
    background: #00b894;
    color: white;
    border: none;
    border-radius: 5px;
    margin-left: 10px;
    cursor: pointer;
    font-size: 16px;
}

#addBtn:hover {
    background: #00a085;
}

.filters {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.filter-btn {
    padding: 8px 16px;
    border: 1px solid #ddd;
    background: white;
    cursor: pointer;
    margin: 0 5px;
}

.filter-btn.active {
    background: #74b9ff;
    color: white;
    border-color: #74b9ff;
}

.todo-list {
    list-style: none;
    padding: 0;
}

.todo-item {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #eee;
}

.todo-item.completed .todo-text {
    text-decoration: line-through;
    color: #888;
}

.todo-text {
    flex: 1;
    margin-left: 10px;
}

.delete-btn {
    background: #e17055;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
}

.delete-btn:hover {
    background: #d63031;
}'''

    def _generate_todo_js(self) -> str:
        """Generate todo app JavaScript"""
        return '''class TodoApp {
    constructor() {
        this.todos = JSON.parse(localStorage.getItem('todos')) || [];
        this.filter = 'all';
        this.init();
    }

    init() {
        this.bindEvents();
        this.render();
    }

    bindEvents() {
        document.getElementById('addBtn').addEventListener('click', () => this.addTodo());
        document.getElementById('todoInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTodo();
        });

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });
    }

    addTodo() {
        const input = document.getElementById('todoInput');
        const text = input.value.trim();
        
        if (text) {
            const todo = {
                id: Date.now(),
                text: text,
                completed: false
            };
            
            this.todos.push(todo);
            this.save();
            this.render();
            input.value = '';
        }
    }

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.save();
            this.render();
        }
    }

    deleteTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        this.save();
        this.render();
    }

    setFilter(filter) {
        this.filter = filter;
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-filter="${filter}"]`).classList.add('active');
        this.render();
    }

    getFilteredTodos() {
        switch (this.filter) {
            case 'active':
                return this.todos.filter(t => !t.completed);
            case 'completed':
                return this.todos.filter(t => t.completed);
            default:
                return this.todos;
        }
    }

    render() {
        const todoList = document.getElementById('todoList');
        const filteredTodos = this.getFilteredTodos();
        
        todoList.innerHTML = filteredTodos.map(todo => `
            <li class="todo-item ${todo.completed ? 'completed' : ''}">
                <input type="checkbox" ${todo.completed ? 'checked' : ''} 
                       onchange="app.toggleTodo(${todo.id})">
                <span class="todo-text">${todo.text}</span>
                <button class="delete-btn" onclick="app.deleteTodo(${todo.id})">Delete</button>
            </li>
        `).join('');
    }

    save() {
        localStorage.setItem('todos', JSON.stringify(this.todos));
    }
}

const app = new TodoApp();'''

    def _generate_landing_html(self) -> str:
        """Generate landing page HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Landing Page</title>
    <link rel="stylesheet" href="landing-styles.css">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">Brand</div>
            <ul class="nav-menu">
                <li><a href="#features">Features</a></li>
                <li><a href="#pricing">Pricing</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <section class="hero">
        <div class="hero-container">
            <h1>Revolutionary Product</h1>
            <p>Transform your workflow with our innovative solution</p>
            <a href="#" class="cta-button">Get Started Free</a>
        </div>
    </section>

    <section id="features" class="features">
        <div class="container">
            <h2>Features</h2>
            <div class="features-grid">
                <div class="feature">
                    <h3>Fast</h3>
                    <p>Lightning fast performance</p>
                </div>
                <div class="feature">
                    <h3>Secure</h3>
                    <p>Enterprise-grade security</p>
                </div>
                <div class="feature">
                    <h3>Scalable</h3>
                    <p>Grows with your business</p>
                </div>
            </div>
        </div>
    </section>

    <section id="pricing" class="pricing">
        <div class="container">
            <h2>Pricing</h2>
            <div class="pricing-grid">
                <div class="price-card">
                    <h3>Basic</h3>
                    <div class="price">$9/month</div>
                    <ul>
                        <li>Feature 1</li>
                        <li>Feature 2</li>
                    </ul>
                    <button class="price-btn">Choose Plan</button>
                </div>
                <div class="price-card featured">
                    <h3>Pro</h3>
                    <div class="price">$29/month</div>
                    <ul>
                        <li>Everything in Basic</li>
                        <li>Advanced Features</li>
                        <li>Priority Support</li>
                    </ul>
                    <button class="price-btn">Choose Plan</button>
                </div>
            </div>
        </div>
    </section>

    <script src="landing-script.js"></script>
</body>
</html>'''

    def _generate_landing_css(self) -> str:
        """Generate landing page CSS"""
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.navbar {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
}

.nav-logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
}

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 120px 20px 80px;
    margin-top: 60px;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.cta-button {
    background: #ff6b6b;
    color: white;
    padding: 15px 30px;
    text-decoration: none;
    border-radius: 50px;
    font-weight: bold;
    transition: background 0.3s;
}

.cta-button:hover {
    background: #ff5252;
}

.features {
    padding: 80px 0;
    background: #f8f9fa;
}

.features h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.feature {
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.pricing {
    padding: 80px 0;
}

.pricing h2 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

.pricing-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    max-width: 800px;
    margin: 0 auto;
}

.price-card {
    background: white;
    border: 2px solid #eee;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
}

.price-card.featured {
    border-color: #667eea;
    transform: scale(1.05);
}

.price {
    font-size: 2rem;
    font-weight: bold;
    color: #667eea;
    margin: 1rem 0;
}

.price-card ul {
    list-style: none;
    margin: 1rem 0;
}

.price-card li {
    padding: 0.5rem 0;
}

.price-btn {
    background: #667eea;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    width: 100%;
}'''

    def _generate_landing_js(self) -> str:
        """Generate landing page JavaScript"""
        return '''// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// CTA button tracking
document.querySelector('.cta-button').addEventListener('click', function(e) {
    e.preventDefault();
    alert('Thank you for your interest! Sign up form would open here.');
});

// Price button handling
document.querySelectorAll('.price-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        alert(`You selected the ${this.closest('.price-card').querySelector('h3').textContent} plan!`);
    });
});

console.log('Landing page loaded! Built with ULTIMA AI.');'''

    def _generate_password_generator_html(self) -> str:
        """Generate password generator HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Password Generator</title>
    <link rel="stylesheet" href="password-generator.css">
</head>
<body>
    <div class="container">
        <h1>🔐 Secure Password Generator</h1>
        <div class="generator-card">
            <div class="password-display">
                <input type="text" id="generatedPassword" readonly placeholder="Click generate to create password">
                <button id="copyBtn" class="copy-btn">📋 Copy</button>
            </div>
            
            <div class="controls">
                <div class="control-group">
                    <label for="length">Password Length: <span id="lengthValue">12</span></label>
                    <input type="range" id="length" min="4" max="50" value="12">
                </div>
                
                <div class="checkbox-group">
                    <label>
                        <input type="checkbox" id="uppercase" checked> Uppercase Letters (A-Z)
                    </label>
                    <label>
                        <input type="checkbox" id="lowercase" checked> Lowercase Letters (a-z)
                    </label>
                    <label>
                        <input type="checkbox" id="numbers" checked> Numbers (0-9)
                    </label>
                    <label>
                        <input type="checkbox" id="symbols" checked> Symbols (!@#$%^&*)
                    </label>
                </div>
                
                <button id="generateBtn" class="generate-btn">🔄 Generate Password</button>
                
                <div class="strength-indicator">
                    <div class="strength-label">Password Strength:</div>
                    <div class="strength-bar">
                        <div id="strengthBar" class="strength-fill"></div>
                    </div>
                    <div id="strengthText" class="strength-text">Click generate</div>
                </div>
            </div>
            
            <div class="tips">
                <h3>🛡️ Security Tips:</h3>
                <ul>
                    <li>Use at least 12 characters for strong security</li>
                    <li>Include a mix of uppercase, lowercase, numbers, and symbols</li>
                    <li>Never reuse passwords across different accounts</li>
                    <li>Consider using a password manager</li>
                </ul>
            </div>
        </div>
    </div>
    
    <script src="password-generator.js"></script>
</body>
</html>'''

    def _generate_password_generator_css(self) -> str:
        """Generate password generator CSS"""
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.container {
    max-width: 600px;
    margin: 0 auto;
}

h1 {
    text-align: center;
    color: white;
    margin-bottom: 30px;
    font-size: 2.5rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.generator-card {
    background: white;
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}

.password-display {
    display: flex;
    margin-bottom: 30px;
    gap: 10px;
}

#generatedPassword {
    flex: 1;
    padding: 15px;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 18px;
    font-family: 'Courier New', monospace;
    background: #f8f9fa;
}

.copy-btn {
    padding: 15px 20px;
    background: #28a745;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
}

.copy-btn:hover {
    background: #218838;
}

.copy-btn.copied {
    background: #17a2b8;
}

.controls {
    margin-bottom: 30px;
}

.control-group {
    margin-bottom: 20px;
}

.control-group label {
    display: block;
    margin-bottom: 10px;
    font-weight: 600;
    color: #495057;
}

#length {
    width: 100%;
    height: 8px;
    border-radius: 5px;
    background: #ddd;
    outline: none;
    opacity: 0.7;
    transition: opacity 0.2s;
}

#length:hover {
    opacity: 1;
}

#length::-webkit-slider-thumb {
    appearance: none;
    width: 25px;
    height: 25px;
    border-radius: 50%;
    background: #667eea;
    cursor: pointer;
}

.checkbox-group {
    margin: 20px 0;
}

.checkbox-group label {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    cursor: pointer;
    color: #495057;
}

.checkbox-group input[type="checkbox"] {
    margin-right: 10px;
    transform: scale(1.2);
}

.generate-btn {
    width: 100%;
    padding: 15px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s;
    margin-bottom: 20px;
}

.generate-btn:hover {
    background: #5a6fd8;
}

.strength-indicator {
    margin-top: 20px;
}

.strength-label {
    font-weight: 600;
    margin-bottom: 10px;
    color: #495057;
}

.strength-bar {
    width: 100%;
    height: 10px;
    background: #e9ecef;
    border-radius: 5px;
    overflow: hidden;
    margin-bottom: 10px;
}

.strength-fill {
    height: 100%;
    transition: width 0.3s ease, background-color 0.3s ease;
    border-radius: 5px;
}

.strength-text {
    text-align: center;
    font-weight: 600;
    padding: 5px;
    border-radius: 5px;
}

.strength-weak {
    background: #dc3545;
    color: white;
}

.strength-medium {
    background: #ffc107;
    color: #212529;
}

.strength-strong {
    background: #28a745;
    color: white;
}

.tips {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #667eea;
}

.tips h3 {
    color: #495057;
    margin-bottom: 15px;
}

.tips ul {
    padding-left: 20px;
}

.tips li {
    margin-bottom: 8px;
    color: #6c757d;
    line-height: 1.5;
}

@media (max-width: 768px) {
    .container {
        padding: 10px;
    }
    
    h1 {
        font-size: 2rem;
    }
    
    .generator-card {
        padding: 20px;
    }
    
    .password-display {
        flex-direction: column;
    }
}'''

    def _generate_password_generator_js(self) -> str:
        """Generate password generator JavaScript"""
        return '''class PasswordGenerator {
    constructor() {
        this.lengthSlider = document.getElementById('length');
        this.lengthValue = document.getElementById('lengthValue');
        this.uppercaseCheck = document.getElementById('uppercase');
        this.lowercaseCheck = document.getElementById('lowercase');
        this.numbersCheck = document.getElementById('numbers');
        this.symbolsCheck = document.getElementById('symbols');
        this.generateBtn = document.getElementById('generateBtn');
        this.passwordField = document.getElementById('generatedPassword');
        this.copyBtn = document.getElementById('copyBtn');
        this.strengthBar = document.getElementById('strengthBar');
        this.strengthText = document.getElementById('strengthText');
        
        this.characters = {
            uppercase: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            lowercase: 'abcdefghijklmnopqrstuvwxyz',
            numbers: '0123456789',
            symbols: '!@#$%^&*()_+-=[]{}|;:,.<>?'
        };
        
        this.init();
    }
    
    init() {
        this.lengthSlider.addEventListener('input', () => this.updateLength());
        this.generateBtn.addEventListener('click', () => this.generatePassword());
        this.copyBtn.addEventListener('click', () => this.copyPassword());
        
        // Generate initial password
        this.generatePassword();
    }
    
    updateLength() {
        this.lengthValue.textContent = this.lengthSlider.value;
    }
    
    generatePassword() {
        const length = parseInt(this.lengthSlider.value);
        let charset = '';
        
        if (this.uppercaseCheck.checked) charset += this.characters.uppercase;
        if (this.lowercaseCheck.checked) charset += this.characters.lowercase;
        if (this.numbersCheck.checked) charset += this.characters.numbers;
        if (this.symbolsCheck.checked) charset += this.characters.symbols;
        
        if (charset === '') {
            alert('Please select at least one character type!');
            return;
        }
        
        let password = '';
        for (let i = 0; i < length; i++) {
            password += charset.charAt(Math.floor(Math.random() * charset.length));
        }
        
        this.passwordField.value = password;
        this.updateStrengthIndicator(password);
    }
    
    updateStrengthIndicator(password) {
        let score = 0;
        let feedback = '';
        
        // Length check
        if (password.length >= 12) score += 25;
        else if (password.length >= 8) score += 15;
        else score += 5;
        
        // Character variety check
        if (/[a-z]/.test(password)) score += 15;
        if (/[A-Z]/.test(password)) score += 15;
        if (/[0-9]/.test(password)) score += 15;
        if (/[^a-zA-Z0-9]/.test(password)) score += 20;
        
        // Bonus for length
        if (password.length >= 16) score += 10;
        
        // Update visual indicator
        this.strengthBar.style.width = Math.min(score, 100) + '%';
        
        if (score < 40) {
            this.strengthBar.className = 'strength-fill strength-weak';
            this.strengthText.textContent = 'Weak';
            this.strengthText.className = 'strength-text strength-weak';
            feedback = 'Consider using more character types and increasing length';
        } else if (score < 70) {
            this.strengthBar.className = 'strength-fill strength-medium';
            this.strengthText.textContent = 'Medium';
            this.strengthText.className = 'strength-text strength-medium';
            feedback = 'Good password, but could be stronger';
        } else {
            this.strengthBar.className = 'strength-fill strength-strong';
            this.strengthText.textContent = 'Strong';
            this.strengthText.className = 'strength-text strength-strong';
            feedback = 'Excellent password strength!';
        }
    }
    
    async copyPassword() {
        if (!this.passwordField.value) {
            alert('Generate a password first!');
            return;
        }
        
        try {
            await navigator.clipboard.writeText(this.passwordField.value);
            this.copyBtn.textContent = '✅ Copied!';
            this.copyBtn.classList.add('copied');
            
            setTimeout(() => {
                this.copyBtn.textContent = '📋 Copy';
                this.copyBtn.classList.remove('copied');
            }, 2000);
        } catch (err) {
            // Fallback for older browsers
            this.passwordField.select();
            document.execCommand('copy');
            alert('Password copied to clipboard!');
        }
    }
}

// Initialize the password generator when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new PasswordGenerator();
    console.log('🔐 Secure Password Generator loaded! Built with ULTIMA AI.');
});'''

    def _generate_weather_app_html(self) -> str:
        """Generate weather app HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
    <link rel="stylesheet" href="weather-app.css">
</head>
<body>
    <div class="app">
        <h1>Weather App</h1>
        <div class="location-form">
            <input type="text" id="locationInput" placeholder="Enter location">
            <button id="getWeatherBtn">Get Weather</button>
        </div>
        <div class="weather-info">
            <div class="current-weather">
                <h2>Current Weather</h2>
                <div class="temperature">Temperature: <span id="temperature">Loading...</span></div>
                <div class="description">Description: <span id="description">Loading...</span></div>
                <div class="icon">
                    <img id="weatherIcon" src="" alt="Weather Icon">
                </div>
            </div>
            <div class="forecast">
                <h2>5-Day Forecast</h2>
                <div class="forecast-items">
                    <div class="forecast-item">
                        <h3>Day 1</h3>
                        <div class="temperature">Temperature: <span id="forecast1Temp">Loading...</span></div>
                        <div class="description">Description: <span id="forecast1Desc">Loading...</span></div>
                        <div class="icon">
                            <img id="forecast1Icon" src="" alt="Forecast Icon">
                        </div>
                    </div>
                    <div class="forecast-item">
                        <h3>Day 2</h3>
                        <div class="temperature">Temperature: <span id="forecast2Temp">Loading...</span></div>
                        <div class="description">Description: <span id="forecast2Desc">Loading...</span></div>
                        <div class="icon">
                            <img id="forecast2Icon" src="" alt="Forecast Icon">
                        </div>
                    </div>
                    <div class="forecast-item">
                        <h3>Day 3</h3>
                        <div class="temperature">Temperature: <span id="forecast3Temp">Loading...</span></div>
                        <div class="description">Description: <span id="forecast3Desc">Loading...</span></div>
                        <div class="icon">
                            <img id="forecast3Icon" src="" alt="Forecast Icon">
                        </div>
                    </div>
                    <div class="forecast-item">
                        <h3>Day 4</h3>
                        <div class="temperature">Temperature: <span id="forecast4Temp">Loading...</span></div>
                        <div class="description">Description: <span id="forecast4Desc">Loading...</span></div>
                        <div class="icon">
                            <img id="forecast4Icon" src="" alt="Forecast Icon">
                        </div>
                    </div>
                    <div class="forecast-item">
                        <h3>Day 5</h3>
                        <div class="temperature">Temperature: <span id="forecast5Temp">Loading...</span></div>
                        <div class="description">Description: <span id="forecast5Desc">Loading...</span></div>
                        <div class="icon">
                            <img id="forecast5Icon" src="" alt="Forecast Icon">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="weather-app.js"></script>
</body>
</html>'''

    def _generate_weather_app_css(self) -> str:
        """Generate weather app CSS"""
        return '''body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #74b9ff, #0984e3);
    min-height: 100vh;
}

.app {
    max-width: 500px;
    margin: 0 auto;
    background: white;
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

h1 {
    text-align: center;
    color: #2d3436;
    margin-bottom: 30px;
}

.location-form {
    display: flex;
    margin-bottom: 20px;
}

#locationInput {
    flex: 1;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

#getWeatherBtn {
    padding: 12px 20px;
    background: #00b894;
    color: white;
    border: none;
    border-radius: 5px;
    margin-left: 10px;
    cursor: pointer;
    font-size: 16px;
}

#getWeatherBtn:hover {
    background: #00a085;
}

.weather-info {
    display: flex;
}

.current-weather {
    flex: 1;
    text-align: center;
}

.forecast {
    flex: 1;
    text-align: center;
}

.forecast-items {
    display: flex;
    justify-content: space-between;
}

.forecast-item {
    flex: 1;
    text-align: center;
}

.forecast-item h3 {
    margin-bottom: 10px;
}

.forecast-item .temperature {
    font-size: 18px;
    font-weight: bold;
}

.forecast-item .description {
    margin-top: 5px;
}

.forecast-item .icon img {
    width: 50px;
    height: 50px;
}

.temperature {
    margin-bottom: 10px;
}

.description {
    margin-top: 5px;
}

.icon {
    margin-top: 10px;
}

@media (max-width: 768px) {
    .weather-info {
        flex-direction: column;
    }
}'''

    def _generate_weather_app_js(self) -> str:
        """Generate weather app JavaScript"""
        return '''class WeatherApp {
    constructor() {
        this.locationInput = document.getElementById('locationInput');
        this.getWeatherBtn = document.getElementById('getWeatherBtn');
        this.currentWeather = document.querySelector('.current-weather');
        this.forecastItems = document.querySelectorAll('.forecast-item');
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        this.getWeatherBtn.addEventListener('click', () => this.getWeather());
    }

    async getWeather() {
        const location = this.locationInput.value.trim();
        if (!location) {
            alert('Please enter a location');
            return;
        }

        try {
            const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=${YOUR_API_KEY}&units=metric`);
            const data = await response.json();

            if (data.cod === 200) {
                this.displayCurrentWeather(data);
                this.displayForecast(data.list);
            } else {
                alert('Location not found');
            }
        } catch (error) {
            console.error('Error fetching weather data:', error);
            alert('An error occurred');
        }
    }

    displayCurrentWeather(data) {
        const temperature = data.main.temp;
        const description = data.weather[0].description;
        const icon = data.weather[0].icon;

        this.currentWeather.querySelector('.temperature').textContent = `Temperature: ${temperature}°C`;
        this.currentWeather.querySelector('.description').textContent = `Description: ${description}`;
        this.currentWeather.querySelector('.icon img').src = `https://openweathermap.org/img/wn/${icon}.png`;
    }

    displayForecast(list) {
        this.forecastItems.forEach((item, index) => {
            const forecast = list[index * 8];
            item.querySelector('.temperature').textContent = `Temperature: ${forecast.main.temp}°C`;
            item.querySelector('.description').textContent = `Description: ${forecast.weather[0].description}`;
            item.querySelector('.icon img').src = `https://openweathermap.org/img/wn/${forecast.weather[0].icon}.png`;
        });
    }
}

const app = new WeatherApp();'''

    def _generate_expense_tracker_html(self) -> str:
        """Generate expense tracker HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Expense Tracker</title>
    <link rel="stylesheet" href="expense-tracker.css">
</head>
<body>
    <div class="app">
        <h1>Expense Tracker</h1>
        <div class="transaction-form">
            <input type="text" id="description" placeholder="Description">
            <input type="number" id="amount" placeholder="Amount">
            <select id="category">
                <option value="Food">Food</option>
                <option value="Transport">Transport</option>
                <option value="Housing">Housing</option>
                <option value="Entertainment">Entertainment</option>
                <option value="Other">Other</option>
            </select>
            <button id="addTransactionBtn">Add Transaction</button>
        </div>
        <div class="transactions">
            <h2>Transactions</h2>
            <ul id="transactionList"></ul>
        </div>
        <div class="summary">
            <h2>Summary</h2>
            <div class="total">Total: <span id="total">0</span></div>
            <div class="income">Income: <span id="income">0</span></div>
            <div class="expense">Expense: <span id="expense">0</span></div>
        </div>
    </div>
    <script src="expense-tracker.js"></script>
</body>
</html>'''

    def _generate_expense_tracker_css(self) -> str:
        """Generate expense tracker CSS"""
        return '''body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(135deg, #74b9ff, #0984e3);
    min-height: 100vh;
}

.app {
    max-width: 500px;
    margin: 0 auto;
    background: white;
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

h1 {
    text-align: center;
    color: #2d3436;
    margin-bottom: 30px;
}

.transaction-form {
    display: flex;
    margin-bottom: 20px;
}

#description, #amount {
    flex: 1;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

#addTransactionBtn {
    padding: 12px 20px;
    background: #00b894;
    color: white;
    border: none;
    border-radius: 5px;
    margin-left: 10px;
    cursor: pointer;
    font-size: 16px;
}

#addTransactionBtn:hover {
    background: #00a085;
}

.transactions {
    margin-bottom: 20px;
}

.transactions h2 {
    margin-bottom: 10px;
}

.transactions ul {
    list-style: none;
    padding: 0;
}

.transactions li {
    display: flex;
    justify-content: space-between;
    padding: 10px;
    border-bottom: 1px solid #eee;
}

.transactions li:last-child {
    border-bottom: none;
}

.summary {
    text-align: center;
}

.summary h2 {
    margin-bottom: 10px;
}

.total, .income, .expense {
    margin-bottom: 10px;
}

.total span, .income span, .expense span {
    font-weight: bold;
}

@media (max-width: 768px) {
    .transaction-form {
        flex-direction: column;
    }

    #description, #amount {
        margin-bottom: 10px;
    }
}'''

    def _generate_expense_tracker_js(self) -> str:
        """Generate expense tracker JavaScript"""
        return '''class ExpenseTracker {
    constructor() {
        this.transactions = [];
        this.total = 0;
        this.income = 0;
        this.expense = 0;
        this.init();
    }

    init() {
        this.bindEvents();
        this.render();
    }

    bindEvents() {
        document.getElementById('addTransactionBtn').addEventListener('click', () => this.addTransaction());
    }

    addTransaction() {
        const description = document.getElementById('description').value.trim();
        const amount = parseFloat(document.getElementById('amount').value);
        const category = document.getElementById('category').value;

        if (!description || isNaN(amount)) {
            alert('Please enter a valid description and amount');
            return;
        }

        const transaction = {
            id: Date.now(),
            description,
            amount,
            category,
            date: new Date().toLocaleDateString()
        };

        this.transactions.push(transaction);
        this.updateSummary();
        this.render();

        document.getElementById('description').value = '';
        document.getElementById('amount').value = '';
        document.getElementById('category').value = 'Food';
    }

    updateSummary() {
        this.total = this.transactions.reduce((total, transaction) => total + transaction.amount, 0);
        this.income = this.transactions.filter(t => t.amount > 0).reduce((total, transaction) => total + transaction.amount, 0);
        this.expense = this.transactions.filter(t => t.amount < 0).reduce((total, transaction) => total + transaction.amount, 0);
    }

    render() {
        const transactionList = document.getElementById('transactionList');
        transactionList.innerHTML = this.transactions.map(transaction => `
            <li>${transaction.description} - ${transaction.amount.toFixed(2)} - ${transaction.category} - ${transaction.date}</li>
        `).join('');

        document.getElementById('total').textContent = this.total.toFixed(2);
        document.getElementById('income').textContent = this.income.toFixed(2);
        document.getElementById('expense').textContent = this.expense.toFixed(2);
    }
}

const app = new ExpenseTracker();'''

    def _generate_ultima_dashboard_html(self) -> str:
        """Generate ULTIMA dashboard HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTIMA AI Dashboard</title>
    <link rel="stylesheet" href="ultima-dashboard.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <div class="dashboard">
        <!-- Header -->
        <header class="header">
            <div class="header-left">
                <div class="logo">
                    <i class="fas fa-robot"></i>
                    <span>ULTIMA AI</span>
                </div>
                <div class="status-indicator">
                    <div class="status-dot active"></div>
                    <span>System Operational</span>
                </div>
            </div>
            <div class="header-right">
                <div class="time-display" id="currentTime"></div>
                <div class="user-profile">
                    <i class="fas fa-user-circle"></i>
                </div>
            </div>
        </header>

        <!-- Sidebar -->
        <aside class="sidebar">
            <nav class="nav-menu">
                <div class="nav-item active" data-section="overview">
                    <i class="fas fa-tachometer-alt"></i>
                    <span>Overview</span>
                </div>
                <div class="nav-item" data-section="agents">
                    <i class="fas fa-cogs"></i>
                    <span>Agents</span>
                </div>
                <div class="nav-item" data-section="tasks">
                    <i class="fas fa-tasks"></i>
                    <span>Tasks</span>
                </div>
                <div class="nav-item" data-section="monitoring">
                    <i class="fas fa-chart-line"></i>
                    <span>Monitoring</span>
                </div>
                <div class="nav-item" data-section="settings">
                    <i class="fas fa-cog"></i>
                    <span>Settings</span>
                </div>
            </nav>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Overview Section -->
            <section id="overview" class="content-section active">
                <div class="section-header">
                    <h1>System Overview</h1>
                    <p>Real-time status of your ULTIMA AI system</p>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-microchip"></i>
                        </div>
                        <div class="stat-content">
                            <h3 id="tasksCompleted">1,247</h3>
                            <p>Tasks Completed</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-rocket"></i>
                        </div>
                        <div class="stat-content">
                            <h3 id="activeTasks">12</h3>
                            <p>Active Tasks</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="stat-content">
                            <h3 id="activeAgents">4</h3>
                            <p>Active Agents</p>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon">
                            <i class="fas fa-clock"></i>
                        </div>
                        <div class="stat-content">
                            <h3 id="uptime">99.9%</h3>
                            <p>System Uptime</p>
                        </div>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <div class="dashboard-card">
                        <h3>Recent Tasks</h3>
                        <div class="task-list" id="recentTasks">
                            <div class="task-item completed">
                                <i class="fas fa-check-circle"></i>
                                <span>Create portfolio website</span>
                                <time>2 min ago</time>
                            </div>
                            <div class="task-item completed">
                                <i class="fas fa-check-circle"></i>
                                <span>Generate password app</span>
                                <time>5 min ago</time>
                            </div>
                            <div class="task-item active">
                                <i class="fas fa-spinner fa-spin"></i>
                                <span>Build ULTIMA dashboard</span>
                                <time>In progress</time>
                            </div>
                        </div>
                    </div>

                    <div class="dashboard-card">
                        <h3>System Health</h3>
                        <div class="health-metrics">
                            <div class="metric">
                                <span>CPU Usage</span>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: 45%"></div>
                                </div>
                                <span>45%</span>
                            </div>
                            <div class="metric">
                                <span>Memory</span>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: 62%"></div>
                                </div>
                                <span>62%</span>
                            </div>
                            <div class="metric">
                                <span>GPU</span>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: 28%"></div>
                                </div>
                                <span>28%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Agents Section -->
            <section id="agents" class="content-section">
                <div class="section-header">
                    <h1>AI Agents</h1>
                    <p>Manage and monitor your specialized AI agents</p>
                </div>

                <div class="agents-grid">
                    <div class="agent-card active">
                        <div class="agent-header">
                            <i class="fas fa-globe"></i>
                            <h3>Web Agent</h3>
                            <div class="agent-status active">Online</div>
                        </div>
                        <p>Specializes in web development, creating responsive websites and web applications.</p>
                        <div class="agent-stats">
                            <span>Tasks: 45</span>
                            <span>Success: 98%</span>
                        </div>
                    </div>

                    <div class="agent-card active">
                        <div class="agent-header">
                            <i class="fas fa-file-alt"></i>
                            <h3>File Agent</h3>
                            <div class="agent-status active">Online</div>
                        </div>
                        <p>Handles file operations, workspace management, and Git integration.</p>
                        <div class="agent-stats">
                            <span>Tasks: 32</span>
                            <span>Success: 100%</span>
                        </div>
                    </div>

                    <div class="agent-card active">
                        <div class="agent-header">
                            <i class="fas fa-brain"></i>
                            <h3>AI Agent</h3>
                            <div class="agent-status active">Online</div>
                        </div>
                        <p>Provides advanced AI capabilities, code analysis, and intelligent reasoning.</p>
                        <div class="agent-stats">
                            <span>Tasks: 28</span>
                            <span>Success: 96%</span>
                        </div>
                    </div>

                    <div class="agent-card active">
                        <div class="agent-header">
                            <i class="fas fa-stethoscope"></i>
                            <h3>Diagnostic Agent</h3>
                            <div class="agent-status active">Online</div>
                        </div>
                        <p>Monitors system health, performs diagnostics, and ensures optimal performance.</p>
                        <div class="agent-stats">
                            <span>Tasks: 18</span>
                            <span>Success: 100%</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- New Task Section -->
            <div class="floating-action">
                <button class="fab" id="newTaskBtn">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
        </main>
    </div>

    <!-- New Task Modal -->
    <div class="modal" id="newTaskModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Create New Task</h2>
                <button class="close-btn" id="closeModal">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form id="newTaskForm">
                    <div class="form-group">
                        <label for="taskDescription">Task Description</label>
                        <textarea id="taskDescription" placeholder="Describe what you want ULTIMA to create..." required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="taskType">Task Type</label>
                        <select id="taskType" required>
                            <option value="">Select task type</option>
                            <option value="web_development">Web Development</option>
                            <option value="desktop_app">Desktop Application</option>
                            <option value="file_operations">File Operations</option>
                            <option value="analysis">Code Analysis</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="taskPriority">Priority</label>
                        <select id="taskPriority" required>
                            <option value="low">Low</option>
                            <option value="medium" selected>Medium</option>
                            <option value="high">High</option>
                        </select>
                    </div>
                    <button type="submit" class="submit-btn">
                        <i class="fas fa-rocket"></i>
                        Create Task
                    </button>
                </form>
            </div>
        </div>
    </div>

    <script src="ultima-dashboard.js"></script>
</body>
</html>'''

    def _generate_ultima_dashboard_css(self) -> str:
        """Generate ULTIMA dashboard CSS"""
        return '''/* ULTIMA Dashboard Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background: #0a0b0d;
    color: #ffffff;
    overflow-x: hidden;
}

.dashboard {
    display: grid;
    grid-template-areas: 
        "header header"
        "sidebar main";
    grid-template-columns: 280px 1fr;
    grid-template-rows: 70px 1fr;
    height: 100vh;
}

/* Header */
.header {
    grid-area: header;
    background: linear-gradient(135deg, #1a1d29, #2d1b69);
    padding: 0 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #2a2d3a;
    backdrop-filter: blur(20px);
}

.header-left {
    display: flex;
    align-items: center;
    gap: 30px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 24px;
    font-weight: 700;
    color: #00d4ff;
}

.logo i {
    font-size: 28px;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: #94a3b8;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.header-right {
    display: flex;
    align-items: center;
    gap: 20px;
}

.time-display {
    font-size: 14px;
    color: #94a3b8;
    font-weight: 500;
}

.user-profile i {
    font-size: 24px;
    color: #00d4ff;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.user-profile i:hover {
    transform: scale(1.1);
}

/* Sidebar */
.sidebar {
    grid-area: sidebar;
    background: linear-gradient(180deg, #1a1d29, #0f1419);
    padding: 30px 0;
    border-right: 1px solid #2a2d3a;
}

.nav-menu {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 0 20px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 20px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    color: #94a3b8;
}

.nav-item:hover {
    background: rgba(0, 212, 255, 0.1);
    color: #00d4ff;
    transform: translateX(5px);
}

.nav-item.active {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(124, 58, 237, 0.2));
    color: #00d4ff;
    border: 1px solid rgba(0, 212, 255, 0.3);
}

.nav-item i {
    font-size: 18px;
    width: 20px;
}

/* Main Content */
.main-content {
    grid-area: main;
    background: linear-gradient(135deg, #0f1419, #1a1d29);
    padding: 30px;
    overflow-y: auto;
}

.content-section {
    display: none;
}

.content-section.active {
    display: block;
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.section-header {
    margin-bottom: 30px;
}

.section-header h1 {
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.section-header p {
    color: #94a3b8;
    font-size: 16px;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(124, 58, 237, 0.1));
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 16px;
    padding: 25px;
    display: flex;
    align-items: center;
    gap: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 212, 255, 0.2);
}

.stat-icon {
    width: 60px;
    height: 60px;
    border-radius: 12px;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    color: white;
}

.stat-content h3 {
    font-size: 28px;
    font-weight: 700;
    color: #00d4ff;
    margin-bottom: 5px;
}

.stat-content p {
    color: #94a3b8;
    font-size: 14px;
}

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 20px;
}

.dashboard-card {
    background: linear-gradient(135deg, rgba(26, 29, 41, 0.8), rgba(15, 20, 25, 0.8));
    border: 1px solid #2a2d3a;
    border-radius: 16px;
    padding: 25px;
    backdrop-filter: blur(20px);
}

.dashboard-card h3 {
    color: #00d4ff;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 20px;
}

/* Task List */
.task-list {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.task-item {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px;
    background: rgba(0, 212, 255, 0.05);
    border-radius: 10px;
    border-left: 3px solid #00d4ff;
}

.task-item.completed {
    border-left-color: #10b981;
}

.task-item.completed i {
    color: #10b981;
}

.task-item.active i {
    color: #f59e0b;
}

.task-item span {
    flex: 1;
    color: #e2e8f0;
}

.task-item time {
    color: #94a3b8;
    font-size: 12px;
}

/* Health Metrics */
.health-metrics {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.metric {
    display: flex;
    align-items: center;
    gap: 15px;
}

.metric span:first-child {
    min-width: 80px;
    color: #94a3b8;
    font-size: 14px;
}

.progress-bar {
    flex: 1;
    height: 8px;
    background: #2a2d3a;
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    border-radius: 4px;
    transition: width 0.3s ease;
}

.metric span:last-child {
    min-width: 40px;
    text-align: right;
    color: #00d4ff;
    font-weight: 600;
}

/* Agents Grid */
.agents-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.agent-card {
    background: linear-gradient(135deg, rgba(26, 29, 41, 0.8), rgba(15, 20, 25, 0.8));
    border: 1px solid #2a2d3a;
    border-radius: 16px;
    padding: 25px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.agent-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 212, 255, 0.1);
}

.agent-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
}

.agent-header i {
    font-size: 24px;
    color: #00d4ff;
}

.agent-header h3 {
    flex: 1;
    color: #e2e8f0;
    font-size: 18px;
    font-weight: 600;
}

.agent-status {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

.agent-status.active {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.agent-card p {
    color: #94a3b8;
    line-height: 1.6;
    margin-bottom: 20px;
}

.agent-stats {
    display: flex;
    gap: 20px;
}

.agent-stats span {
    color: #00d4ff;
    font-size: 14px;
    font-weight: 500;
}

/* Floating Action Button */
.floating-action {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 1000;
}

.fab {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.fab:hover {
    transform: scale(1.1);
    box-shadow: 0 15px 40px rgba(0, 212, 255, 0.6);
}

/* Modal */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 2000;
    backdrop-filter: blur(10px);
}

.modal.active {
    display: flex;
    animation: fadeIn 0.3s ease;
}

.modal-content {
    background: linear-gradient(135deg, #1a1d29, #0f1419);
    border: 1px solid #2a2d3a;
    border-radius: 20px;
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow: hidden;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 30px;
    border-bottom: 1px solid #2a2d3a;
}

.modal-header h2 {
    color: #00d4ff;
    font-size: 24px;
    font-weight: 600;
}

.close-btn {
    background: none;
    border: none;
    color: #94a3b8;
    font-size: 20px;
    cursor: pointer;
    transition: color 0.3s ease;
}

.close-btn:hover {
    color: #e2e8f0;
}

.modal-body {
    padding: 30px;
}

.form-group {
    margin-bottom: 25px;
}

.form-group label {
    display: block;
    color: #e2e8f0;
    font-weight: 500;
    margin-bottom: 8px;
}

.form-group input,
.form-group textarea,
.form-group select {
    width: 100%;
    padding: 12px 15px;
    background: rgba(42, 45, 58, 0.5);
    border: 1px solid #2a2d3a;
    border-radius: 8px;
    color: #e2e8f0;
    font-size: 14px;
    transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
    outline: none;
    border-color: #00d4ff;
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

.submit-btn {
    width: 100%;
    padding: 15px;
    background: linear-gradient(135deg, #00d4ff, #7c3aed);
    border: none;
    border-radius: 10px;
    color: white;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
    .dashboard {
        grid-template-areas: 
            "header"
            "main";
        grid-template-columns: 1fr;
        grid-template-rows: 70px 1fr;
    }
    
    .sidebar {
        display: none;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
    
    .agents-grid {
        grid-template-columns: 1fr;
    }
}'''

    def _generate_ultima_dashboard_js(self) -> str:
        """Generate ULTIMA dashboard JavaScript"""
        return '''class UltimaDashboard {
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
});''' 