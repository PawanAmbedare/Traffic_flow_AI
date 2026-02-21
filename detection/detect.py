import cv2
import numpy as np
from ultralytics import YOLO
from sklearn.cluster import KMeans

model = YOLO("yolov8n.pt")

vehicle_classes = [2, 3, 5, 7]

video_path = "videos/traffic.mp4"
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
        return {}, False

    height, width, _ = frame.shape

    results = model.predict(frame, conf=0.25, verbose=False)

    x_centers = []
    boxes_data = []

    for result in results:
        boxes = result.boxes

        for box in boxes:
            cls = int(box.cls[0])
            if cls in vehicle_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_x = (x1 + x2) // 2

                x_centers.append([center_x])
                boxes_data.append((x1, y1, x2, y2))

    if len(x_centers) == 0:
        return {}, False

    lane_count = detect_lane_count(np.array(x_centers))

    lane_width = width // lane_count
    lane_area = lane_width * height

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

    return lane_density, False