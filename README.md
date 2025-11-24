# wAgents - AI Agent Development Environment

![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-green.svg)
![CUDA](https://img.shields.io/badge/CUDA-12.0-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive Docker-based development environment specifically designed for AI agent development, equipped with GPU acceleration, security tools, code quality assurance, and a rich set of development utilities.

## 🎯 Project Overview

**wAgents** is a production-ready containerized environment that provides everything needed for modern AI agent development. Built on NVIDIA CUDA with GPU support, it includes pre-configured security scanning, code quality tools, data version control, and a sophisticated terminal experience with Zsh and numerous productivity tools.

### Key Features

- **🎯 GPU Acceleration**: Full NVIDIA CUDA 12.0 support for ML/AI workloads
- **🔒 Security-First**: Integrated vulnerability scanning (Bandit, Safety) and security analysis tools
- **✨ Code Quality**: Automated linting, formatting, and pre-commit hooks with Ruff
- **📊 Data Management**: DVC (Data Version Control) with S3 integration
- **🛠️ Development Tools**: Rich terminal experience with Zsh, Oh My Zsh, and 20+ productivity tools
- **🐳 Container Ready**: Optimized Docker setup with GPU passthrough and Docker-in-Docker
- **🤖 AI Agent Support**: Pre-configured for GitHub Copilot and Google Gemini CLI

## 📁 Project Structure

```
wAgents/
├── 📁 python/examples/                    # Example code for testing tools
│   ├── 📁 security/                       # Security vulnerability examples
│   │   ├── 📄 test_code_scan.py          # Code with security vulnerabilities
│   │   └── 📄 test_library_scan.py       # Dependencies with known CVEs
│   ├── 📁 quality/                        # Code quality issue examples
│   │   └── 📄 test_quality_check.py       # Code with quality issues
│   ├── 📁 yolo/                           # YOLO AI/ML examples
│   │   ├── 📁 person detection detection.v2i.yolov11/  # Person detection dataset
│   │   │   ├── 📁 train/               # Training images & labels
│   │   │   ├── 📁 valid/               # Validation images & labels
│   │   │   ├── 📁 test/                # Test images & labels
│   │   │   └── 📄 data.yaml            # Dataset configuration
│   │   ├── 📄 train_yolo.py              # YOLO training example
│   │   ├── 📄 validate_yolo.py           # YOLO validation example
│   │   ├── 📄 test_yolo.py               # YOLO testing example
│   │   └── 📄 inference_yolo.py          # YOLO inference example
│   └── 📁 other/                          # General development examples
│       └── 📄 test_other_tools.py         # Code with style issues
├── 📁 requirements/                        # Python dependencies
│   ├── 📄 base.txt                        # Core development tools
│   ├── 📄 dvc.txt                    # Data version control
│   ├── 📄 security.txt               # Security scanning tools
│   ├── 📄 yolo.txt                   # AI/ML object detection tools
│   └── 📄 see_image_terminal.txt     # Terminal image viewing
├── 📁 scripts/                             # Automation scripts
│   ├── 📁 executor/                       # Runtime execution scripts
│   │   ├── 📁 security/                  # Security scanning scripts
│   │   │   ├── 📄 scan_code_vulnerability.sh
│   │   │   └── 📄 scan_libraries_vulnerability.sh
│   │   ├── 📁 quality/                   # Code quality scripts
│   │   │   └── 📄 correct_quality_py.sh
│   │   ├── 📁 images/                    # Image viewing scripts
│   │   │   ├── 📄 see_image_with_clickimage.py
│   │   │   └── 📄 see_imagen_with_sixel.py
│   │   ├── 📁 other/                     # Utility scripts
│   │   │   └── 📄 new_curl.sh
│   │   └── 📄 auto_reload_py.sh          # Auto-reload Python apps
│   └── 📁 install/                        # Installation and setup scripts
│       ├── 📄 dvc_controller.sh           # DVC setup
│       ├── 📄 images_control.sh           # Image management
│       └── 📄 other_agents.sh             # AI agents installation
├── 📄 Dockerfile                          # Container definition
├── 📄 docker-compose.yml                  # Service orchestration
├── 📄 README.md                           # This documentation
└── 📄 William-1.jpg                       # Sample image
```

## 🔄 System Workflow

```mermaid
graph TB
    A[Developer] --> B[Docker Compose]
    B --> C[wAgents Container]
    C --> D[Zsh Shell]
    C --> E[GPU Support]
    C --> F[Python Environment]
    
    D --> G[Welcome Script]
    D --> H[Aliases & Plugins]
    
    F --> I[Security Tools]
    F --> J[Quality Tools]
    F --> K[Development Tools]
    F --> L[AI/ML Tools]
    
    I --> M[Bandit Scanner]
    I --> N[Safety Scanner]
    
    J --> O[Ruff Linter]
    J --> P[Pre-commit Hooks]
    
    K --> Q[DVC]
    K --> R[AI Agents]
    K --> S[Image Viewers]
    
    L --> T[Ultralytics YOLO]
    L --> U[PyTorch]
    L --> V[OpenCV]
    L --> W[Person Detection Dataset]
    
    M --> X[Security Reports]
    N --> X
    O --> Y[Quality Reports]
    P --> Y
    Q --> Z[Data Management]
    R --> AA[AI Assistant]
    S --> BB[Image Processing]
    T --> CC[Object Detection]
    U --> CC
    V --> CC
    W --> CC
    
    X --> DD[Fixed Code]
    Y --> DD
    Z --> EE[Versioned Data]
    AA --> DD
    BB --> DD
    CC --> FF[Trained Models]
    
    DD --> GG[Production Ready]
    EE --> GG
    FF --> GG
```

## 🚶‍♂️ Diagram Walkthrough

```mermaid
flowchart TD
    Start([Start]) --> Setup[Setup Environment]
    Setup --> Build[Build Container]
    Build --> Launch[Launch Container]
    Launch --> Welcome[Welcome Banner]
    
    Welcome --> Choice{What do you want to do?}
    
    Choice -->|Security| SecurityPath[Security Workflow]
    Choice -->|Quality| QualityPath[Quality Workflow]
    Choice -->|Development| DevPath[Development Workflow]
    Choice -->|Data| DataPath[Data Workflow]
    Choice -->|AI/ML| YoloPath[Person Detection Workflow]
    
    SecurityPath --> SecScan[Run Security Scan]
    SecScan --> SecReport[Review Security Report]
    SecReport --> SecFix[Fix Vulnerabilities]
    
    QualityPath --> QualCheck[Run Quality Check]
    QualCheck --> QualReport[Review Quality Report]
    QualReport --> QualFix[Fix Quality Issues]
    
    DevPath --> DevCode[Write Code]
    DevCode --> DevTest[Test Code]
    DevTest --> DevReload[Auto-reload Development]
    
    DataPath --> DVCInit[Initialize DVC]
    DVCInit --> DVCData[Manage Data]
    DVCData --> DVCPush[Push to Remote]
    
    YoloPath --> YoloDataset[Load Person Dataset]
    YoloDataset --> YoloTrain[Train Person Detection]
    YoloTrain --> YoloVal[Validate Model]
    YoloVal --> YoloTest[Test Performance]
    YoloTest --> YoloInf[Run Inference]
    YoloInf --> YoloReal[Real-time Detection]
    
    SecFix --> Review[Code Review]
    QualFix --> Review
    DevReload --> Review
    DVCPush --> Review
    YoloReal --> Review
    
    Review --> Deploy[Deploy to Production]
    Deploy --> End([End])
```

## 🏗️ Architecture Components

### 1. Container Foundation

**Dockerfile**: Multi-stage build with:
- NVIDIA CUDA 12.0 base image
- Ubuntu 22.04 LTS
- Python 3.x with optimizations
- Zsh shell with Oh My Zsh
- 20+ development tools

**docker-compose.yml**: Service orchestration with:
- GPU passthrough configuration
- Volume mounts for development
- Docker-in-Docker support

### 2. Python Environment

#### Core Dependencies (`requirements/base.txt`)
```
nvitop          # GPU process monitoring
watchdog        # File system monitoring  
ipython         # Enhanced Python REPL
ruff            # Fast Python linter and formatter
pre-commit      # Git hooks management
```

#### Security Tools (`requirements/security.txt`)
```
bandit          # Python security linter
safety          # Dependency vulnerability scanner
httpie          # Modern HTTP client
visidata        # Data analysis tool
scapy           # Packet manipulation
glances         # System monitoring
py-spy          # Python profiler
```

#### Data Management (`requirements/dvc.txt`)
```
pandas          # Data manipulation
dvc             # Data version control
boto3           # AWS SDK for Python
tqdm            # Progress bars
```

#### AI/ML Tools (`requirements/yolo.txt`)
```
ultralytics     # YOLO object detection framework
torch           # PyTorch deep learning framework
torchvision     # Computer vision utilities
opencv-python   # Computer vision library
Pillow          # Image processing
numpy           # Numerical computing
matplotlib      # Plotting and visualization
seaborn         # Statistical visualization
tensorboard     # ML experiment tracking
```

### 3. Script Categories

#### Security Scripts (`scripts/executor/security/`)
- **scan_code_vulnerability.sh**: `bandit -r .` - Scan Python code for security issues
- **scan_libraries_vulnerability.sh**: `safety check` - Check dependencies for CVEs

#### Quality Scripts (`scripts/executor/quality/`)
- **correct_quality_py.sh**: `ruff check --fix .` - Auto-fix code quality issues

#### Development Scripts (`scripts/executor/`)
- **auto_reload_py.sh**: `watchmedo auto-restart` - Auto-reload Python apps
- **new_curl.sh**: Enhanced curl wrapper

#### Installation Scripts (`scripts/install/`)
- **dvc_controller.sh**: Install DVC with S3 support
- **images_control.sh**: Manage Python environments
- **other_agents.sh**: Install AI agents (Copilot, Gemini)

## 📚 Usage Examples

### Quick Start

1. **Build and run the container**
   ```bash
   docker-compose up --build -d
   ```

2. **Access the container**
   ```bash
   docker-compose exec agent zsh
   ```

3. **View available tools**
   ```bash
   help  # Shows welcome banner
   ```

### Security Testing

```bash
# Test security scanning on vulnerable code
cd python/examples/security
../../../scripts/executor/security/scan_code_vulnerability.sh

# Expected output: Security vulnerabilities found in test_code_scan.py
# - SQL injection in vulnerable_function()
# - Dangerous eval() usage
# - Hardcoded passwords
# - Path traversal issues

# Test dependency scanning
../../../scripts/executor/security/scan_libraries_vulnerability.sh

# Expected output: Vulnerabilities found in test_library_scan.py
# - Outdated packages with known CVEs
```

### Code Quality Testing

```bash
# Test quality checking on problematic code
cd python/examples/quality
../../../scripts/executor/quality/correct_quality_py.sh

# Expected output: Quality issues found and fixed in test_quality_check.py
# - Line length violations
# - Unused variables
# - Import organization
# - Code formatting issues
```

### YOLO AI/ML Testing

```bash
# Install YOLO dependencies
pip install -r requirements/yolo.txt

# Test YOLO training on person detection dataset
cd python/examples/yolo
python train_yolo.py

# Test YOLO validation on trained model
python validate_yolo.py

# Test YOLO testing and benchmarking
python test_yolo.py

# Test YOLO inference (single image)
python inference_yolo.py --image "python/examples/yolo/person detection detection.v2i.yolov11/test/images/ektp30_jpeg.rf.d8df759f943f1b0edf4bf8829ff61533.jpg"

# Test YOLO inference (batch on dataset samples)
python inference_yolo.py --samples 10

# Test YOLO real-time inference
python inference_yolo.py --camera 0

# Dataset info:
# - Dataset: Person Detection v2 (YOLOv11 format)
# - Classes: ['Face'] (1 class)
# - Train/Val/Test split available
# - Real images with person annotations
```

### Development Workflow

```bash
# Auto-reload development server
cd /app
./scripts/executor/auto_reload_py.sh

# View images in terminal
./scripts/executor/images/see_imagen_with_sixel.py path/to/image.jpg

# Use productivity aliases
ls          # Enhanced listing with icons
ll          # Detailed listing
cd myproject # Smart directory jumping
grep "pattern" . # Fast search with ripgrep
```

### Development Workflow

```bash
# Auto-reload development server
cd /app
./scripts/executor/auto_reload_py.sh

# View images in terminal
./scripts/executor/images/see_imagen_with_sixel.py scripts/William-1.jpg

# Use productivity aliases
ls          # Enhanced listing with icons
ll          # Detailed listing
cd myproject # Smart directory jumping
grep "pattern" . # Fast search with ripgrep
```

## 📋 File-by-File Guide

### Configuration Files

| File | Purpose | Key Settings |
|------|---------|--------------|
| `Dockerfile` | Container definition | CUDA 12.0, Zsh, GPU tools |
| `docker-compose.yml` | Service orchestration | GPU passthrough, volumes |
| `requirements/base.txt` | Core Python packages | Development essentials |
| `requirements/security.txt` | Security tools | Bandit, Safety, Scapy |
| `requirements/dvc.txt` | Data management | DVC, Pandas, Boto3 |

### Script Files

| Category | Script | Function | Usage |
|----------|--------|----------|-------|
| Security | `scan_code_vulnerability.sh` | Bandit security scan | `./scripts/executor/security/scan_code_vulnerability.sh` |
| Security | `scan_libraries_vulnerability.sh` | Safety dependency scan | `./scripts/executor/security/scan_libraries_vulnerability.sh` |
| Quality | `correct_quality_py.sh` | Ruff quality check | `./scripts/executor/quality/correct_quality_py.sh` |
| Development | `auto_reload_py.sh` | Auto-reload Python | `./scripts/executor/auto_reload_py.sh` |
| Install | `dvc_controller.sh` | DVC setup | `./scripts/install/dvc_controller.sh` |
| Install | `other_agents.sh` | AI agents install | `./scripts/install/other_agents.sh` |

### Example Files

| File | Purpose | Issues Demonstrated |
|------|---------|-------------------|
| `python/examples/security/test_code_scan.py` | Security vulnerabilities | SQL injection, eval(), hardcoded passwords |
| `python/examples/security/test_library_scan.py` | Dependency vulnerabilities | Outdated packages with CVEs |
| `python/examples/quality/test_quality_check.py` | Code quality issues | Long lines, unused variables, formatting |
| `python/examples/other/test_other_tools.py` | Style issues | Trailing whitespace, mixed tabs/spaces |

## 🔧 Customization Guide

### Adding New Security Tools

1. **Add to requirements/security.txt**
   ```txt
   new-security-tool==1.0.0
   ```

2. **Create script in scripts/executor/security/**
   ```bash
   #!/bin/bash
   new-security-tool scan .
   ```

3. **Add example in python/examples/security/**
   ```python
   # Code with vulnerabilities for new tool to detect
   ```

### Adding New Quality Tools

1. **Add to requirements/base.txt**
   ```txt
   new-quality-tool==1.0.0
   ```

2. **Create script in scripts/executor/quality/**
   ```bash
   #!/bin/bash
   new-quality-tool check --fix .
   ```

3. **Add example in python/examples/quality/**
   ```python
   # Code with quality issues for new tool to detect
   ```

### Custom Aliases

Add to `Dockerfile` in the ZSH configuration section:
```dockerfile
RUN echo "alias mycommand='my-actual-command'" >> ~/.zshrc
```

## 🔄 Container Lifecycle

### Build Process

```mermaid
graph LR
    A[Host Files] --> B[COPY requirements]
    B --> C[/requirements/]
    A --> D[COPY scripts]
    D --> E[/scripts/]
    A --> F[COPY python]
    F --> G[/python_test/]
    C --> H[Install Python Packages]
    E --> I[Configure Scripts]
    G --> J[Setup Examples]
    H --> K[Install AI/ML Tools]
    I --> K
    J --> K
    K --> L[Final Container]
    
    subgraph "AI/ML Components"
        M[Ultralytics YOLO]
        N[PyTorch]
        O[OpenCV]
        P[Person Detection Dataset]
    end
    
    H --> M
    H --> N
    H --> O
    J --> P
```

### Runtime Process

```mermaid
graph TB
    A[Container Start] --> B[WORKDIR: /app]
    B --> C[Mount Host Volume]
    C --> D[Zsh Shell Ready]
    D --> E[Tools Available]
    E --> F[Scripts at /scripts/]
    E --> G[Examples at /python_test/]
    E --> H[Project at /app/]
    E --> I[AI/ML Environment]
    F --> J[Welcome Script]
    G --> J
    H --> J
    I --> J
    J --> K[Ready for Development]
    
    subgraph "AI/ML Runtime"
        L[Person Detection Dataset]
        M[GPU Acceleration]
        N[Model Training]
        O[Real-time Inference]
    end
    
    I --> L
    I --> M
    I --> N
    I --> O
```

## 🚀 Deployment

### Production Deployment

```bash
# Build production image
docker build -t wisrovi/agents:gpu-slim .

# Run with GPU support
docker run --gpus all -v $(pwd):/app wisrovi/agents:gpu-slim
```

### CI/CD Integration

```yaml
# .github/workflows/quality.yml
name: Quality and Security Checks
on: [push, pull_request]

jobs:
  checks:
    runs-on: ubuntu-latest
    container: wisrovi/agents:gpu-slim
    steps:
      - uses: actions/checkout@v3
      - name: Security Scan
        run: ./scripts/executor/security/scan_code_vulnerability.sh
      - name: Check Dependencies
        run: ./scripts/executor/security/scan_libraries_vulnerability.sh
      - name: Check Code Quality
        run: ./scripts/executor/quality/correct_quality_py.sh
      - name: Test YOLO Training
        run: cd python/examples/yolo && python train_yolo.py
```

## 📞 Support

- 📧 Email: wisrovi.rodriguez@gmail.com
- 💼 LinkedIn: [wisrovi-rodriguez](https://es.linkedin.com/in/wisrovi-rodriguez)
- 🐛 Issues: [GitHub Issues](https://github.com/wisrovi/wAgents/issues)

---

**Built with ❤️ for the AI Agent development community**