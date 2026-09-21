# 🎯 Real-Time Human Detection & Counting System

A TensorFlow-based **Faster R-CNN Inception v2** model to detect and count humans in real-time **images**, **videos**, and **live camera feeds** — with a modern, beautiful desktop GUI, analytics plots, and automated PDF crowd reports.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📌 Project Overview

This project is a **Computer Vision-based Human Detection and Counting System** that leverages a pre-trained **Faster R-CNN Inception v2** model from the TensorFlow Object Detection API. It provides a complete solution for detecting and counting humans in images, videos, and live camera feeds — with a modern, user-friendly GUI, visual analytics, and automated PDF reports.

### 🎯 Key Features

- ✅ **Multi-Input Support** — Image, Video, and Live Camera
- ✅ **Real-Time Detection** — Faster R-CNN Inception v2
- ✅ **Human Counting** — Count detected persons with confidence > 0.5
- ✅ **Bounding Box Visualization** — Green boxes with confidence labels
- ✅ **Beautiful Dark-Mode GUI** — Modern, responsive interface
- ✅ **Enumeration Plot** — Human Count vs Time
- ✅ **Accuracy Plot** — Average Accuracy vs Time
- ✅ **Automated PDF Report** — Crowd analysis with max count, accuracy, and crowd status
- ✅ **Preview Mode** — Preview selected files before detection
- ✅ **Stop Detection** — Manually halt ongoing detection

- **Dynamic Graphical Analytics:**
  - **Enumeration Plot:** Human Count vs. Time.
  - **Accuracy Plot:** Average Confidence Accuracy vs. Time.
- **Executive PDF Crowd Report:** Auto-generates `Crowd_Report.pdf` with peak density metrics, total frames analyzed, average confidence, and crowd status classification (High vs. Low Density).

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **GUI** | Tkinter / CustomTkinter, PIL |
| **Image Processing** | OpenCV (cv2) |
| **Deep Learning** | TensorFlow, Faster R-CNN Inception v2 |
| **Visualization** | Matplotlib |
| **Report Generation** | FPDF |
| **Language** | Python 3.8+ |

---

## 📁 Repository Structure
```
Real-Time-Human-Detection-Counting/
├── main.py                      # Main entry point & application controller
├── ui/
│   ├── theme.py                 # Color scheme (#0F172A) & fonts
│   ├── widgets.py               # Custom cards & stat badges
│   ├── start_screen.py          # Modern animated splash screen
│   ├── dashboard.py             # Main control panel & live video canvas
│   └── results_screen.py        # Analytics & PDF preview view
├── core/
│   ├── detector.py              # TensorFlow Faster R-CNN graph loader
│   ├── preprocessing.py         # BGR to RGB frame scaler
│   ├── postprocessing.py        # Bounding box drawing & score filter
│   └── counting.py              # Crowd density classifier
├── reports/
│   ├── plot_generator.py        # Matplotlib enumeration & accuracy curves
│   └── pdf_generator.py         # FPDF executive report compiler
├── docs/
│   ├── Task1_Project_Proposal.md
│   ├── Task2_Literature_Survey.md
│   ├── Task3_System_Architecture.md
│   ├── Task4_Implementation_Part1.md
│   └── Task5_Implementation_Part2.md
├── frozen_inference_graph.pb    # Pre-trained model weights
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.9 - 3.11 installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python main.py
```

---

## 📄 Task Documents 
All  task documents are formatted and located in the `docs/` folder:
- [Task 1: Project Proposal](docs/Task1_Project_Proposal.md)
- [Task 2: Literature Survey](docs/Task2_Literature_Survey.md)
- [Task 3: System Architecture](docs/Task3_System_Architecture.md)
- [Task 4: Implementation Part 1 (25%)](docs/Task4_Implementation_Part1.md)
- [Task 5: Implementation Part 2 (50%)](docs/Task5_Implementation_Part2.md)
