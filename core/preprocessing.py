import cv2

def preprocess_frame(frame, target_size=None):
    """Preprocess frame for detection and display."""
    if frame is None:
        return None
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if target_size:
        rgb_frame = cv2.resize(rgb_frame, target_size)
    return rgb_frame
