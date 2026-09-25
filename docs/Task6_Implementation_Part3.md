# Implementation Part 3 (75% Progress Report)
## Real-Time Human Detection & Counting System

**Course:** CSE411 Computer Vision  
**Project Title:** Real-Time Human Detection & Counting System  
**Team Number:** 23  
**Team Members:**  
- M ROHAN NAIDU (2023BCS0148)  
- VARSHITH KILLARI (2023BCS0157)  
- DEBAM DIAN (2023BCS0154)  
- GOPICHAND (2023BCS145)  
**Institute:** IIIT Kottayam  

---

## 1. Progress Summary (Task 5 → Task 6: 75% Completion)

| Aspect | Task 5 (50%) | Task 6 (75%) |
|---|---|---|
| **GUI** | Complete dashboard layout | Fully polished interactive UI with real-time analytics panel |
| **Model & Engine** | Inference pipeline active | Integrated multi-threaded processing engine for Image, Video, & Camera |
| **Post-Processing** | Basic box rendering | Color-coded boxes with adaptive confidence thresholds & labels |
| **Counting & Analytics** | Standalone dynamic counter | Real-time enumeration tracker & live time-series data buffering |
| **Plots & Visualizations** | Plot generation scripts | Seamless embedded Matplotlib rendering (`enumeration_plot.png`, `accuracy_plot.png`) |
| **PDF Reporting** | PDF builder prototype | Automated executive summary PDF generation (`Crowd_Report.pdf`) with metrics |
| **Integration & Test** | Single-input tests | End-to-end multi-input prototype validation across all media sources |

---

## 2. Integrated Modules & Prototype Architecture (75% Work)

The 75% system prototype integrates seven core software modules into a cohesive pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│              75% SYSTEM PROTOTYPE ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [ GUI Frontend ] <---> [ Preprocessing ] <---> [ DetectorAPI ] │
│         │                      │                      │         │
│         ▼                      ▼                      ▼         │
│  [ Dashboard UI ] <---> [ Postprocessing ] <---> [ Counting ]   │
│                                │                        │       │
│                                ▼                        ▼       │
│                     [ Plot & Report Generator ] <───────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Completed Modules:
1. **Tkinter / Custom UI Interface (`ui/`):** Full dashboard with Start screen, Input selection (Image, Video, Live Camera), Control panel (Preview, Detect, Stop), and Live Count display.
2. **Detection Core (`core/detector.py`):** TensorFlow session execution loading `frozen_inference_graph.pb` (Faster R-CNN Inception v2).
3. **Pre & Post Processing (`core/preprocessing.py`, `core/postprocessing.py`):** Frame scaling, color space conversions, person-class (`class_id == 1`) filtering with confidence thresholding (>0.5), box rendering, and bounding coordinates logic.
4. **Human Counting Module (`core/counting.py`):** Real-time frame-by-frame accumulator tracking peak counts and temporal variations.
5. **Plot & Analytics Suite (`reports/plot_generator.py`):** Matplotlib time-series plotting engine outputting `enumeration_plot.png` and `accuracy_plot.png`.
6. **Executive PDF Report Builder (`reports/pdf_generator.py`):** FPDF-driven PDF compiler creating `Crowd_Report.pdf` containing max crowd density, average confidence, total frames, and crowd level status (High/Low).

---

## 3. Demonstration & Outputs / Results (75% Prototype)

### 3.1 Quantitative Results across Test Inputs

| Test Input Scenario | Input Category | Frame Count | Max Humans Detected | Avg Accuracy | FPS | Crowd Density Status |
|---|---|---|---|---|---|---|
| **Crowd Image Sample 1** | Static Image | 1 | 15 | 92.4% | N/A | High Density |
| **Crowd Image Sample 2** | Static Image | 1 | 8 | 88.0% | N/A | Low Density |
| **Group Photo** | Static Image | 1 | 6 | 91.0% | N/A | Low Density |
| **Crowd Video Feed** | MP4 Video File | 500 | 28 | 89.6% | 8.4 FPS | High Density |
| **Live Camera Feed** | Webcam Stream | 300 | 4 | 91.2% | 7.8 FPS | Low Density |

### 3.2 Output Artifacts Generated
- **`enumeration_plot.png`:** Visualizes person count trends over elapsed operational time.
- **`accuracy_plot.png`:** Visualizes detection confidence percentage per frame over time.
- **`Crowd_Report.pdf`:** Exported summary document containing structured metrics and automated crowd status determination.

---

## 4. Remaining Work (25% to Complete Project - Task 7)

While ~75% of the system pipeline, GUI, detection logic, counting module, plot generators, and report builder are fully implemented and integrated into a functional prototype, the remaining **25%** consists of:

| S.No | Module / Component | Detailed Description of Remaining 25% Work | Completion Goal |
|---|---|---|---|
| **1** | **Ablation & Model Benchmark Study** | Perform quantitative baseline comparisons comparing Faster R-CNN Inception v2 against YOLOv3, SSD, and MobileNet-SSD across mAP, FPS, and precision/recall metrics. | Task 7 |
| **2** | **End-to-End System Stress & Boundary Testing** | Multi-hour extended camera stream tests, error resilience under corrupted video/image files, and memory leak audits. | Task 7 |
| **3** | **Final Report Compilation & Codebase Polish** | Complete 100% comprehensive documentation including Section 1-9, theoretical background, full source code structure, user guide, and repository finalization. | Task 7 |

---
