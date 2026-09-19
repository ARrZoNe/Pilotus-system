# код для распознавания человека
# необходимо скачать модель YOLOv5n

import cv2
import numpy as np
import tensorflow as tf
import time

MODEL_PATH = "yolov5n-int8.tflite"
INPUT_SIZE = 320
CONF_THRESHOLD = 0.4
NMS_THRESHOLD = 0.5

interpreter = tf.lite.Interpreter(model_path=MODEL_PATH, num_threads=4)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape'][1:3]  # (H, W)

CLASSES = ["person"]

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

fps_start = time.time()
fps_count = 0
fps = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img = cv2.resize(frame, (INPUT_SIZE, INPUT_SIZE))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    outputs = interpreter.get_tensor(output_details[0]['index'])

    boxes = outputs[0][:, :4]
    scores = outputs[0][:, 4]
    class_ids = outputs[0][:, 5].astype(int)

    mask = (scores > CONF_THRESHOLD) & (class_ids == 0)
    boxes, scores, class_ids = boxes[mask], scores[mask], class_ids[mask]

    if len(boxes) > 0:
        h_orig, w_orig = frame.shape[:2]
        scale_x, scale_y = w_orig / INPUT_SIZE, h_orig / INPUT_SIZE

        indices = cv2.dnn.NMSBoxes(boxes.tolist(), scores.tolist(), CONF_THRESHOLD, NMS_THRESHOLD)
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                x1, y1 = int((x - w/2) * scale_x), int((y - h/2) * scale_y)
                x2, y2 = int((x + w/2) * scale_x), int((y + h/2) * scale_y)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Person {scores[i]:.2f}", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    fps_count += 1
    if time.time() - fps_start >= 1:
        fps = fps_count / (time.time() - fps_start)
        fps_count = 0
        fps_start = time.time()
    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow('Person Detection (CPU)', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()