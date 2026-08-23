# Real-Time Human Detection & Counting System

An executive, high-performance desktop application for real-time human detection, spatial density estimation, enumeration plotting, and automated PDF crowd report compilation using **Faster R-CNN Inception v2** and **CustomTkinter**.

---

## 📌 Project Overview
- **Team Number:** 23
- **Team Members:**
  - M ROHAN NAIDU (2023BCS0148)
  - VARSHITH KILLARI (2023BCS0157)
  - DEBAM DIAN (2023BCS0154)
  - GOPICHAND (2023BCS145)
- **Institute:** IIIT Kottayam

---

## ✨ Features & Key Highlights
- **Modern Executive Interface:** Deep navy theme (`#0F172A`), glassmorphism card components, responsive layouts, hover effects, and live metric badges.
- **Multi-Source Support:**
  - 🖼 **Image Mode:** Process static `.jpg`, `.png`, `.bmp` files.
  - 🎬 **Video Mode:** Frame-by-frame processing for `.mp4`, `.avi`, `.mov` streams.
  - 📷 **Camera Mode:** Real-time web camera inference.
- **Real-Time Bounding Box Visualization:** Green bounding boxes with person confidence labels (`score > 0.5`).
- **Dynamic Graphical Analytics:**
  - **Enumeration Plot:** Human Count vs. Time.
  - **Accuracy Plot:** Average Confidence Accuracy vs. Time.
- **Executive PDF Crowd Report:** Auto-generates `Crowd_Report.pdf` with peak density metrics, total frames analyzed, average confidence, and crowd status classification (High vs. Low Density).

---

## 🛠 Tech Stack
- **UI Framework:** CustomTkinter, Pillow
- **Deep Learning Model:** Faster R-CNN Inception v2 (`frozen_inference_graph.pb`)
- **Computer Vision:** OpenCV (`cv2`)
- **Plotting & Analytics:** Matplotlib
- **Document Generator:** FPDF

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

## 📄 Task Documents (Academic Deliverables)
All academic task documents are formatted and located in the `docs/` folder:
- [Task 1: Project Proposal](docs/Task1_Project_Proposal.md)
- [Task 2: Literature Survey](docs/Task2_Literature_Survey.md)
- [Task 3: System Architecture](docs/Task3_System_Architecture.md)
- [Task 4: Implementation Part 1 (25%)](docs/Task4_Implementation_Part1.md)
- [Task 5: Implementation Part 2 (50%)](docs/Task5_Implementation_Part2.md)
