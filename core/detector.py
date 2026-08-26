import os
import sys

# Suppress TensorFlow C++ log verbosity and oneDNN warnings on import
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np

class DetectorAPI:
    def __init__(self, model_path=None):
        import tensorflow._api.v2.compat.v1 as tf
        tf.disable_v2_behavior()
        self.tf = tf

        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            model_path = os.path.join(base_dir, 'frozen_inference_graph.pb')
            if not os.path.exists(model_path):
                model_path = 'frozen_inference_graph.pb'

        self.path_to_ckpt = model_path
        self.detection_graph = self.tf.Graph()

        with self.detection_graph.as_default():
            od_graph_def = self.tf.GraphDef()
            with self.tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                self.tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = self.tf.Session(graph=self.detection_graph)

        # Input and output Tensors for detection_graph
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

    def close(self):
        self.sess.close()
        self.default_graph.close()
