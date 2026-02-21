import cv2
import numpy as np
from ultralytics import YOLO
from sklearn.cluster import KMeans
from detection.emergency_detector import detect_emergency_vehicle

model = YOLO("yolov8n.pt")

vehicle_classes = [2, 3, 5, 7]

video_path = "videos/traffic4.mp4"
cap = cv2.VideoCapture(video_path)

def detect_lane_count(x_coords):

    if len(x_coords) < 4:
        return 2

    best_k = 2
    best_inertia = float('inf')

    for k in [2, 3, 4]:
        kmeans = KMeans(n_clusters=k, n_init=10)
        kmeans.fit(x_coords)

        if kmeans.inertia_ < best_inertia:
            best_inertia = kmeans.inertia_
            best_k = k

    return best_k


def get_traffic_data():

    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return {}, []

    display_frame = frame.copy()

    height, width, _ = frame.shape

    results = model.predict(frame, conf=0.25, verbose=False)

    x_centers = []
    boxes_data = []
    ambulance_positions = []

    for result in results:
        boxes = result.boxes

        for box in boxes:
            cls = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if cls in vehicle_classes:

                x_centers.append([cx])
                boxes_data.append((x1, y1, x2, y2))

                cv2.rectangle(display_frame,(x1,y1),(x2,y2),(255,0,0),2)

                vehicle_crop = frame[y1:y2, x1:x2]
                if detect_emergency_vehicle(vehicle_crop):
                    ambulance_positions.append((cx, cy))
                    cv2.putText(display_frame,"EMERGENCY",
                    (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,0,255),
                    2)

    if len(x_centers) == 0:
        return {}, ambulance_positions

    lane_count = detect_lane_count(np.array(x_centers))

    lane_width = width // lane_count
    lane_area = lane_width * height

    for i in range(1, lane_count):
        cv2.line(display_frame,
                 (i * lane_width, 0),
                 (i * lane_width, height),
                 (0,255,0), 2)

    lane_vehicle_area = {}
    lane_density = {}

    for i in range(lane_count):
        lane_vehicle_area[f"lane{i+1}"] = 0

    for (x1, y1, x2, y2) in boxes_data:
        center_x = (x1 + x2) // 2
        box_area = (x2 - x1) * (y2 - y1)

        lane_index = min(center_x // lane_width, lane_count - 1)
        lane_vehicle_area[f"lane{lane_index+1}"] += box_area

    for i in range(lane_count):
        density = (lane_vehicle_area[f"lane{i+1}"] / lane_area) * 100
        lane_density[f"lane{i+1}"] = round(min(density, 100), 2)

        cv2.putText(display_frame,
                    f"L{i+1}: {lane_density[f'lane{i+1}']}%",
                    (i * lane_width + 20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,255),
                    2)

    if len(ambulance_positions) > 0:
        cv2.putText(display_frame,
                    "EMERGENCY VEHICLE DETECTED",
                    (50,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    3)

    cv2.imshow("Real-Time AI Traffic Monitoring", display_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()

    return lane_density, ambulance_positions