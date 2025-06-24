# ULTIMA Phase 1 Roadmap - Core Agents Development

Based on chat history analysis and foundation completion, here's the prioritized development plan:

## 🎯 **Immediate Goals (Next 1-2 weeks)**

### **1. Cursor Integration Bridge** (Priority: CRITICAL)
**Goal**: Connect Cursor AI → NeoAI for "single prompt → MVP" workflow

#### Components to Build:
- [ ] `src/cursor_bridge/task_detector.py` 
  - Monitors Cursor workspace for task definitions
  - Parses `// #AI_TASK: Create Android game` comments
  - Converts to structured JSON task format

- [ ] `src/cursor_bridge/task_writer.py`
  - Writes processed tasks to `tasks/` directory
  - Triggers NeoAI orchestrator via file watcher

- [ ] `src/cursor_bridge/result_writer.py`
  - Takes completed task outputs
  - Writes results back to Cursor as files/comments

**Test Case**: Cursor comment → File creation → Result back to Cursor

### **2. Diagnostic Agent** (Priority: HIGH)
**Goal**: Self-diagnosis and dependency installation

#### Components:
- [ ] `src/agents/diagnostic_agent.py`
  - System requirements checking (RAM, GPU, disk space)
  - Missing package detection (apt, pip, npm, Docker)
  - Environment validation (Python version, Node.js, etc.)

- [ ] `src/agents/installer_agent.py`
  - Automated package installation with user approval
  - Snapshot creation before major changes
  - Rollback capability on failures

**Test Case**: "Create Python web app" → Detects missing Flask → Asks permission → Installs → Proceeds

### **3. Web Agent** (Priority: HIGH)
**Goal**: Browser automation for web development tasks

#### Components:
- [ ] `src/agents/web_agent.py`
  - Playwright integration for browser automation
  - Form filling, navigation, screenshot capture
  - Web scraping and data extraction

- [ ] `src/agents/deploy_agent.py`
  - Netlify/Vercel deployment automation
  - GitHub Pages publishing
  - Domain configuration assistance

**Test Case**: "Build landing page" → Creates HTML/CSS → Deploys to Netlify → Returns live URL

### **4. Coder Agent** (Priority: MEDIUM)
**Goal**: Advanced code generation beyond Cursor's capabilities

#### Components:
- [ ] `src/agents/coder_agent.py`
  - Local LLM (Ollama) integration for code generation
  - Template-based project scaffolding
  - Code quality checking and testing

- [ ] `src/llm/local_client.py`
  - Ollama client with 14B Q4/Q5 model support
  - Context management for long code generation
  - Model switching based on task complexity

**Test Case**: "Create REST API" → Generates FastAPI code → Creates tests → Sets up Docker

## 🏗️ **Technical Implementation Plan**

### **Week 1: Cursor Bridge + Diagnostics**
```bash
# Day 1-2: Cursor Bridge
src/cursor_bridge/
├── __init__.py
├── task_detector.py     # File watcher + comment parser
├── task_writer.py       # Task JSON generator  
└── result_writer.py     # Result feedback to Cursor

# Day 3-4: Diagnostic System
src/agents/diagnostic_agent.py    # System checker
src/agents/installer_agent.py     # Auto-installer

# Day 5: Integration Testing
tests/test_cursor_integration.py
```

### **Week 2: Web Agent + Local LLM**
```bash
# Day 1-3: Web Automation
src/agents/web_agent.py          # Playwright automation
src/agents/deploy_agent.py       # Deployment handlers

# Day 4-5: LLM Integration
src/llm/local_client.py          # Ollama integration
src/agents/coder_agent.py        # Code generation

# Integration with existing orchestrator
```

## 🧪 **Success Criteria**

### **End of Phase 1 Goals:**
1. **Cursor → ULTIMA → Result** complete workflow
2. **"Create a simple website"** → Full deployment in <30 minutes
3. **Self-diagnosis** catches 90% of missing dependencies
4. **3+ concurrent agents** working without conflicts
5. **Human checkpoints** working for critical decisions

### **Demo Scenarios:**
- **Web Dev**: `// #AI_TASK: Create portfolio website` → Live site
- **API Dev**: `// #AI_TASK: Build REST API for todo app` → Working API
- **Diagnostic**: System automatically installs missing Node.js

## 🔧 **Technical Considerations**

### **RTX 3060 6GB Optimization:**
- Use 14B Q4_K_M models maximum
- Implement model switching (local → API fallback)
- RAM monitoring and cleanup between tasks
- Context window management (4096 tokens max)

### **Concurrency Management:**
- File locking for shared resources
- Agent load balancing based on queue size
- Resource allocation per agent type
- Graceful degradation under high load

### **Safety & Rollback:**
- Timeshift snapshots before major operations
- Dry-run mode for testing
- User approval gates for system changes
- Kill switch for runaway processes

## 📈 **Future Phases Preview**

### **Phase 2**: Android Development Pipeline
- Android Studio automation
- APK building and testing
- Play Store preparation

### **Phase 3**: Desktop Applications
- Tauri/Electron project generation
- Cross-platform building
- Installer creation

### **Phase 4**: Self-Improvement Loop
- Success pattern learning
- Agent performance optimization
- Community sharing features

---

*This roadmap prioritizes immediate value delivery while building towards the ultimate goal of "single prompt → complete MVP" automation.* 