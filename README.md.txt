# 🚀 Enterprise AI Data Engineering & MLOps Portfolio

Welcome to my centralized AI Data Operations portfolio. This repository showcases production-grade data factories, programmatic human-in-the-loop (HITL) data annotation pipelines, and real-time operational intelligence frameworks. 

Instead of relying on manual configurations or basic automation scripts, these projects focus on building robust system architectures that connect local intelligence models with production interfaces to solve real-world business challenges efficiently.

---

## 📂 Repository Architecture

This repository is organized as a monorepo containing distinct specialized data operations platforms:

```text
├── project-omnidrone/      # Multi-Modal Programmatic Data Labeling Stack
│   ├── nlp_prelabel.py     # Local LLM text token entity extraction pipeline
│   ├── vision_prelabel.py  # Spatial coordinate transformation engine
│   ├── sensor_prelabel.py  # High-frequency multi-variate telemetry validator
│   └── README.md           # Technical documentation for OmniDrone
│
├── project-smartqueue/     # Enterprise Support Triage & Insights Platform
│   ├── triage_pipe.py      # Structured JSON LLM extraction node
│   ├── simulate_stream.py  # Bulk processing streaming utility script
│   ├── dashboard.py        # Streamlit analytic executive control panel
│   └── README.md           # Technical documentation for SmartQueue
│
└── .gitignore              # Standard global Python & data protection rules