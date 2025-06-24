# ULTIMA Project Requirements Document (PRD)
*AI-Powered System Automation & MVP Generation Framework*

## 1. PROJECT VISION

### Mission Statement
Build a fully autonomous development orchestrator that transforms single natural language prompts into complete, deployable software products (MVPs) through intelligent agent coordination.

### Core Value Proposition
- **Input**: "Create an Android game" or "Build a landing page"  
- **Output**: Complete, tested, deployable product within hours
- **Method**: Cursor AI + Local LLM agents + Human checkpoints

## 2. SYSTEM ARCHITECTURE

### 2.1 Core Components
```
USER PROMPT → Cursor (Sonnet-4/o3) → NeoAI Orchestrator → Multi-Agents → MVP
```

#### Layer Breakdown:
1. **Cursor Interface Layer**
   - Receives natural language tasks
   - Uses Sonnet-4/o3 for task analysis & planning (zero-cost)
   - Outputs structured task definitions

2. **NeoAI Orchestrator**  
   - Task routing and agent coordination
   - Progress monitoring and checkpoint management
   - Resource allocation and conflict resolution

3. **Agent Execution Layer**
   - CoderAgent: Code generation & refactoring
   - FileAgent: File system operations
   - BrowserAgent: Web automation
   - PCControlAgent: GUI automation
   - TestAgent: Automated testing
   - DeployAgent: Package & deployment

4. **Feedback Loop**
   - Human approval at checkpoints
   - Self-diagnostics and error recovery
   - Continuous learning from outcomes

### 2.2 Technology Stack
- **Planning**: Cursor AI (Sonnet-4, o3-mini)
- **Orchestration**: Python + asyncio
- **Local LLM**: Ollama (14B Q4/Q5 models)
- **GUI Automation**: PyAutoGUI, xdotool
- **Web Automation**: Playwright
- **Containerization**: Docker (when needed)
- **Version Control**: Git with automated commits

## 3. CAPABILITIES MATRIX

### 3.1 Cursor-Provided Automations (C-series)
| ID | Capability | Provider | Type | Notes |
|----|------------|----------|------|-------|
| C-01 | Multi-file code editing | Cursor | Auto | All languages |
| C-02 | Code generation/completion | Cursor AI | Auto | Free tokens, 32k context |
| C-03 | Code explanation & documentation | Cursor AI | Auto | Inline comments |
| C-04 | VS Code features (search, refactor) | Cursor Core | Auto | Built-in |
| C-05 | Terminal execution | Cursor | Semi-Auto | Agent writes, user approves |
| C-06 | Git operations | Cursor | Auto | CLI wrapped |
| C-07 | Project scaffolding | NeoAI | Auto | New windows/folders |
| C-08 | Task file management | NeoAI | Auto | JSON task flow |

### 3.2 User-Provided Manual Abilities (H-series)  
| ID | Capability | Provider | Type | Notes |
|----|------------|----------|------|-------|
| H-01 | System administration | User | Manual | sudo/Admin rights |
| H-02 | OS installation/configuration | User | Manual | Ubuntu setup, dual boot |
| H-03 | Docker configuration | User | Manual | Env files, port mapping |
| H-04 | Advanced debugging | User | Manual | Segfaults, kernel issues |
| H-05 | API keys/credentials | User | Manual | .env.encrypted files |
| H-06 | Design decisions | User | Manual | UX/UI choices |
| H-07 | Hardware controls | User | Manual | USB, camera, etc. |
| H-08 | Final MVP approval | User | Manual | Go/no-go decisions |

## 4. CHECKPOINT SYSTEM

### 4.1 Human-in-the-Loop Gates
- **Planning Checkpoint**: Task breakdown approval
- **Midpoint Checkpoint**: Basic skeleton + dependencies ready
- **MVP Checkpoint**: Working prototype + test results
- **Final Checkpoint**: Complete product + deploy scripts

### 4.2 Approval Modes
- `interactive`: Requires human approval (initial months)
- `auto`: Autonomous operation (after system maturity)

## 5. TARGET USE CASES

### 5.1 Android Development
**Input**: "Create a simple Android game"
**Output**: 
- Android Studio project
- Kotlin game logic
- APK build + install instructions
- Basic Espresso tests
**Timeline**: 4-6 hours

### 5.2 Web Development  
**Input**: "Build a SaaS landing page"
**Output**:
- Static site (Astro/Next.js)
- Responsive design
- Deployed to Netlify/Vercel
- Lighthouse optimization
**Timeline**: 2-3 hours

### 5.3 Desktop Applications
**Input**: "Create a file organizer tool"
**Output**:
- Cross-platform app (Tauri/Electron)
- GUI interface
- Installer packages
- Unit tests
**Timeline**: 6-8 hours

## 6. HARDWARE REQUIREMENTS

### 6.1 Minimum Specs
- **GPU**: RTX 3060 6GB (for 14B Q4/Q5 models)
- **RAM**: 16GB (12-14GB usage expected)
- **CPU**: 6+ cores (i7-10750H adequate)
- **Storage**: 50GB+ NVMe SSD
- **OS**: Ubuntu 22.04+ (Windows compatible but slower)

### 6.2 Performance Expectations
- **Token Generation**: 2-4 tok/sec on RTX 3060
- **Concurrent Agents**: 2-3 without memory issues
- **Model Limitations**: Max 14B quantized models

## 7. RISK MITIGATION

### 7.1 Security & Safety
- **Kill Switch**: Global NEO_STOP file watcher
- **Rollback**: Timeshift snapshots before major operations  
- **Sandboxing**: Docker containers for risky operations
- **Permission Gates**: sudo operations require approval

### 7.2 Quality Assurance
- **Automated Testing**: Unit + integration templates
- **Smoke Tests**: Basic functionality verification
- **Human Validation**: Critical checkpoints
- **Error Recovery**: Self-diagnostic and retry logic

### 7.3 Resource Management
- **Memory Monitoring**: RAM/VRAM usage tracking
- **Process Isolation**: Agent subprocess management
- **Timeout Handling**: Graceful task termination
- **Cleanup Procedures**: Temporary file management

## 8. SUCCESS METRICS

### 8.1 Primary KPIs
- **Time to MVP**: Single prompt → working product
- **Success Rate**: % of tasks completed without human intervention
- **Quality Score**: Automated test pass rate
- **User Satisfaction**: Checkpoint approval rates

### 8.2 Performance Targets
- **Android App**: 4-6 hours prompt → APK
- **Web Site**: 2-3 hours prompt → deployed URL  
- **Desktop App**: 6-8 hours prompt → installer
- **Error Rate**: <10% fatal failures requiring restart

## 9. FUTURE ENHANCEMENTS

### 9.1 Self-Improvement Loop
- **Experience Database**: Success/failure pattern learning
- **Model Fine-tuning**: Task-specific optimization
- **Agent Evolution**: New capabilities through iteration
- **Performance Optimization**: Resource usage improvements

### 9.2 Ecosystem Expansion
- **Custom Agents**: User-defined specialized agents
- **Template Library**: Pre-built project scaffolds
- **Community Sharing**: Agent marketplace
- **Integration APIs**: Third-party tool connections

## 10. IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Weeks 1-2)
- [ ] Task detection and parsing system
- [ ] Basic Cursor ↔ NeoAI communication
- [ ] Single-agent proof of concept
- [ ] Checkpoint approval mechanism

### Phase 2: Multi-Agent Core (Weeks 3-6)  
- [ ] Agent orchestration framework
- [ ] File operations and Git integration
- [ ] Basic web and GUI automation
- [ ] Error handling and recovery

### Phase 3: Specialized Agents (Weeks 7-12)
- [ ] Android development pipeline
- [ ] Web development workflow  
- [ ] Desktop application creation
- [ ] Automated testing framework

### Phase 4: Production Ready (Months 4-6)
- [ ] Self-diagnostics and improvement
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Documentation and examples

---

*This PRD serves as the north star for ULTIMA development, balancing ambitious automation goals with practical implementation constraints.* 