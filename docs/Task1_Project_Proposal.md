# Project Proposal
## Real-Time Human Detection & Counting System

**Team Number:** 23  
**Team Members:**
- M ROHAN NAIDU (2023BCS0148)
- VARSHITH KILLARI (2023BCS0157)
- DEBAM DIAN (2023BCS0154)
- GOPICHAND (2023BCS145)

**Institute:** IIIT Kottayam  

---

### 1. Abstract
Crowd management and automated spatial auditing are essential in modern public safety, event monitoring, retail analytics, and smart city infrastructure. Manual human counting is inherently error-prone, highly labor-intensive, and inadequate for real-time decision-making. This project proposes a **Real-Time Human Detection & Counting System** utilizing a deep-learning-based object detection model—specifically **Faster R-CNN with an Inception v2 backbone** trained on the COCO dataset—coupled with a modern, high-performance desktop application interface built using `CustomTkinter`. The system processes multi-source visual inputs (single images, recorded video streams, and live camera feeds), performs high-accuracy person detection (filtering confidence > 0.5), extracts frame-by-frame temporal density trends, generates real-time analytical plots (enumeration and accuracy over time), and automatically compiles executive PDF crowd monitoring reports.

---

### 2. Problem Statement
In high-density gathering areas such as transit hubs, religious venues, shopping malls, and academic campuses, dynamic crowd monitoring is crucial to prevent overcrowding, stampedes, and unauthorized access. Existing solutions suffer from:
1. **Manual Inefficiency:** Human-operated tallies are subjective, non-scalable, and prone to fatigue.
2. **Input Rigidity:** Conventional systems often restrict monitoring to specific file formats or lack real-time camera streaming support.
3. **Lack of Executive Reporting:** Most object detection prototypes output raw annotated videos without structured analytic summaries or PDF reporting for decision-makers.
4. **Poor UI/UX:** Traditional academic implementations rely on raw command-line tools or basic legacy Tkinter GUIs that lack visual feedback, modern dark-mode themes, and status dashboards.

---

### 3. Objectives
- **Real-Time Detection Engine:** Implement a robust detection framework leveraging Faster R-CNN Inception v2 capable of identifying human class (`class_id = 1`) with high confidence.
- **Multi-Source Input Support:** Seamlessly integrate static image processing, recorded video analysis, and live web camera feeds.
- **Modern Executive GUI:** Build an aesthetically stunning desktop dashboard featuring dark navy themes, glassmorphism card layouts, smooth transitions, status indicators, and live FPS/count metrics.
- **Analytical Visualization:** Dynamically plot Enumeration (Human Count vs. Time) and Average Confidence Accuracy curves using Matplotlib.
- **Automated PDF Crowd Report Generation:** Provide one-click generation of professional PDF reports detailing total frames, peak crowd density, average confidence, and crowd density status (High/Low Density).

---

### 4. Scope
- **In Scope:**
  - Real-time human detection and counting on single image, video file, and live webcam feeds.
  - Custom confidence filtering (threshold = 0.5) and bounding box drawing with person labels.
  - Interactive GUI with controls for input selection, preview, detection toggle, and analytics tabs.
  - Automated PDF executive report compile engine.
- **Out of Scope:**
  - Facial recognition or biometric identity tracking.
  - Multi-camera cross-tracking or spatial re-identification across non-overlapping views.
  - Edge hardware optimization (e.g., TensorRT FPGA deployment).

---

### 5. Expected Outcomes
1. A fully functional, production-ready desktop software with a modern dark-mode UI.
2. Robust detection pipeline achieving competitive mAP and real-time capability on consumer GPUs/CPUs.
3. Automated graphical plots for temporal density and accuracy tracking.
4. Comprehensive PDF crowd analysis report output (`Crowd_Report.pdf`).
5. Complete academic task documentation (Tasks 1 through 5).

---

### 6. 12-Week Implementation Timeline

| Week | Phase | Key Tasks / Deliverables |
|---|---|---|
| **Week 1-2** | Requirements & Proposal | Literature review, defining problem statement, initial architecture design (Task 1). |
| **Week 3-4** | Survey & Benchmark Setup | Comparative literature survey (Task 2), dataset collection, baseline model testing. |
| **Week 5-6** | System Design & Data Prep | System architecture modeling (Task 3), pre-processing pipeline, modular folder setup. |
| **Week 7** | Initial Implementation (25%) | GUI skeleton creation, TensorFlow frozen graph loader setup (Task 4). |
| **Week 8** | Core Detection Engine | Image, video, and webcam frame-by-frame inference loop implementation. |
| **Week 9** | Intermediate Milestone (50%) | Integration of detection pipeline with GUI controls, bounding box renderer (Task 5). |
| **Week 10** | Analytics & Reporting | Development of Matplotlib plot generator and FPDF crowd report module. |
| **Week 11** | Optimization & UI Polish | Theme refinement, glassmorphism cards, error handling, performance tuning. |
| **Week 12** | Testing & Submission | End-to-end integration testing, final documentation, and project submission. |
