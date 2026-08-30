# Implementation Part 1 (25% Progress Report)
## Real-Time Human Detection & Counting System

**Team Number:** 23  
**Team Members:** M ROHAN NAIDU (2023BCS0148), VARSHITH KILLARI (2023BCS0157), DEBAM DIAN (2023BCS0154), GOPICHAND (2023BCS145)  
**Institute:** IIIT Kottayam  

---

### 1. Dataset Collection
- **Benchmark Dataset:** CrowdHuman Dataset
- **Volume:** 15,000 training images, 4,370 validation images, 5,000 test images.
- **Annotations:** 340,000+ total human instances, averaging 22.6 persons per image.
- **Source:** [CrowdHuman Official](https://www.crowdhuman.org/)

---

### 2. Pre-Processing Pipeline
To feed raw visual frames into the Faster R-CNN Inception v2 graph, frames undergo standardized pre-processing:

| Step | Operation | Description |
|---|---|---|
| **1. Color Space Conversion** | BGR to RGB | Converts OpenCV standard BGR frame matrices into RGB arrays expected by TensorFlow model graph. |
| **2. Frame Resizing** | Rescale | Adjusts input resolution dynamically while maintaining aspect ratio or scaling to tensor shape `(600, 600)`. |
| **3. Batch Dimension Expansion** | `np.expand_dims` | Adds single-batch axis to transform frame shape `[H, W, 3]` to tensor shape `[1, H, W, 3]`. |
| **4. Tensor Casting** | `tf.convert_to_tensor` | Converts NumPy array into uint8 input tensor suitable for session feeding. |

---

### 3. 25% Implementation Modules (Completed Code)

#### Module 1: TensorFlow Model Graph Initialization (`core/detector.py`)
```python
import os
import numpy as np
import tensorflow._api.v2.compat.v1 as tf
tf.disable_v2_behavior()

class DetectorAPI:
    def __init__(self, model_path="frozen_inference_graph.pb"):
        self.model_path = model_path
        self.detection_graph = tf.Graph()

        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.model_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.sess = tf.Session(graph=self.detection_graph)
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        image_np_expanded = np.expand_dims(image, axis=0)
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores,
             self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})

        im_height, im_width, _ = image.shape
        boxes_list = []
        for i in range(boxes.shape[1]):
            boxes_list.append((
                int(boxes[0, i, 0] * im_height),
                int(boxes[0, i, 1] * im_width),
                int(boxes[0, i, 2] * im_height),
                int(boxes[0, i, 3] * im_width)
            ))
        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])
```

#### Module 2: Preprocessing Script (`core/preprocessing.py`)
```python
import cv2
import numpy as np

def preprocess_frame(frame, target_size=None):
    """Convert BGR OpenCV frame to RGB and expand batch dimension."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if target_size:
        rgb_frame = cv2.resize(rgb_frame, target_size)
    return rgb_frame
```

---

### 4. Remaining Tasks & Schedule (Weeks 7–12)

| S.No | Task / Sub-module | Description | Timeline |
|---|---|---|---|
| 1 | Complete Modern UI | Build dark mode CustomTkinter views (Splash, Control, Canvas). | Week 7 |
| 2 | Image Detection Workflow | Connect image file picker to inference engine and canvas. | Week 8 |
| 3 | Video Stream Handler | Implement multi-threaded frame reader for video files. | Week 8 |
| 4 | Live Camera Integration | Add real-time webcam stream grabber. | Week 9 |
| 5 | Post-processing & Bounding Box | Render green boxes and person score tags. | Week 9 |
| 6 | Enumeration Plot Module | Generate real-time Matplotlib count vs time graphs. | Week 10 |
| 7 | Accuracy Plot Module | Generate real-time Matplotlib confidence graphs. | Week 10 |
| 8 | PDF Report Generator | Build FPDF report builder exporting to `Crowd_Report.pdf`. | Week 11 |
| 9 | Optimization & Benchmarks | Measure FPS and memory under high-density frames. | Week 11 |
| 10 | Final System Integration | End-to-end testing and documentation validation. | Week 12 |
