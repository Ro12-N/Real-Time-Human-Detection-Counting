# System Architecture
## Real-Time Human Detection & Counting System

**Team Number:** 23  
**Team Members:** M ROHAN NAIDU (2023BCS0148), VARSHITH KILLARI (2023BCS0157), DEBAM DIAN (2023BCS0154), GOPICHAND (2023BCS145)  
**Institute:** IIIT Kottayam  

---

### 1. Architectural Overview Diagram

```
+-----------------------------------------------------------------------------------+
|                                 USER INTERFACE                                    |
|                       (CustomTkinter Modern GUI Dashboard)                         |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                                 INPUT SELECTION                                   |
|             [ Select Image ]   |   [ Select Video ]   |   [ Open Camera ]          |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                                 PREVIEW ENGINE                                    |
|                    (Frame extraction, BGR to RGB, Resizing)                      |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           DETECTION & ANALYSIS ENGINE                             |
|    +-------------------------------------------------------------------------+    |
|    |  TensorFlow Model Loader: frozen_inference_graph.pb (Faster R-CNN)      |    |
|    +-------------------------------------------------------------------------+    |
|    |  Inference Loop: image_tensor:0 -> [boxes, scores, classes, num]        |    |
|    +-------------------------------------------------------------------------+    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                          POST-PROCESSING & COUNTING                               |
|  - Filter person class (class_id == 1)                                           |
|  - Filter confidence scores (score > 0.5)                                         |
|  - Draw green bounding boxes + confidence labels                                  |
|  - Increment human count accumulator                                              |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                                OUTPUT DISPLAY                                     |
|           (Live Video Canvas + Real-Time FPS Overlay + Human Counter)            |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           ANALYTICS & REPORT ENGINE                               |
|    +-------------------------------------------------------------------------+    |
|    |  Enumeration Plot Generator (Human Count vs. Time)                     |    |
|    |  Accuracy Plot Generator (Avg Confidence vs. Time)                     |    |
|    +-------------------------------------------------------------------------+    |
|    |  Executive PDF Report Generation (FPDF Engine -> Crowd_Report.pdf)     |    |
|    +-------------------------------------------------------------------------+    |
+-----------------------------------------------------------------------------------+
```

---

### 2. Stage-by-Stage Explanation

| Stage | Module | Key Technology | Functionality Description |
|---|---|---|---|
| **Stage 1** | User Interface | `CustomTkinter`, `Pillow` | Provides dark navy theme (`#0F172A`), control panels, navigation headers, and responsive display cards. |
| **Stage 2** | Input Selection | `tkinter.filedialog`, `cv2` | File picker for static images (`.jpg`, `.png`), video files (`.mp4`, `.avi`), or webcam index `0`. |
| **Stage 3** | Model Loading | `TensorFlow (v1 compat)` | Loads the serialized protocol buffer (`frozen_inference_graph.pb`) into memory as a `tf.Graph`. |
| **Stage 4** | Frame Processing | `OpenCV`, `NumPy` | Concurrently reads frames, converts BGR color space to RGB, resizes for optimal memory usage, and expands tensor dimensions `[1, H, W, 3]`. |
| **Stage 5** | Object Detection | `TensorFlow Engine` | Runs session inference returning raw detection boxes, confidence scores, class IDs, and detection count. |
| **Stage 6** | Post-Processing | `Python Core Logic` | Evaluates bounding box coordinates, applies threshold filtering (`score > 0.5`), and isolates human class (`class == 1`). |
| **Stage 7** | Output Display | `CustomTkinter Canvas` | Draws green bounding boxes with confidence tags, updates live counter badge, and renders frames seamlessly. |
| **Stage 8** | Performance Analytics | `Matplotlib` | Generates temporal enumeration graphs and confidence accuracy trends over execution frames. |
| **Stage 9** | Report Generation | `FPDF` | Compiles session statistics, embedded plots, peak crowd metrics, and status badges into `Crowd_Report.pdf`. |

---

### 3. Proposed Methodology & Tech Stack

#### Model Choice: Faster R-CNN Inception v2
- **Architecture:** Two-stage detector utilizing a Region Proposal Network (RPN) for high-quality candidate proposals followed by an Inception v2 feature extraction network.
- **Rationale:** Offers superior detection accuracy for partially occluded humans in multi-person scenes compared to standard single-shot detectors, providing reliable confidence scores for statistical analysis.

#### Hardware & Software Stack Table
- **Language:** Python 3.11+
- **GUI Framework:** CustomTkinter (Dark theme, glassmorphic styling)
- **Computer Vision:** OpenCV (`cv2`), Pillow (`PIL`)
- **Deep Learning Framework:** TensorFlow 2.x (`tf.compat.v1`)
- **Plotting Library:** Matplotlib
- **Document Engine:** FPDF
