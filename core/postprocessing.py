import cv2

def filter_and_draw_boxes(frame, boxes, scores, classes, num_detections, threshold=0.3):
    """Draw bounding boxes for Person class (class_id == 1) and calculate stats."""
    human_count = 0
    valid_scores = []
    annotated_frame = frame.copy()
    
    for i in range(num_detections):
        if classes[i] == 1 and scores[i] >= threshold:
            human_count += 1
            valid_scores.append(scores[i])
            ymin, xmin, ymax, xmax = boxes[i]
            
            # Draw green bounding box
            cv2.rectangle(annotated_frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            
            # Label box
            label = f"Person: {scores[i]:.2f}"
            cv2.putText(annotated_frame, label, (xmin, max(ymin - 8, 15)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
    avg_accuracy = (sum(valid_scores) / len(valid_scores)) if valid_scores else 0.0
    return annotated_frame, human_count, avg_accuracy
