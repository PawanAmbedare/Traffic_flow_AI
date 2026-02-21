from ultralytics import YOLO

vehicle_model = YOLO("yolov8n.pt")

vehicle_classes = [2,3,5,7]

def detect_vehicles(frame):

    results = vehicle_model(frame)
    vehicles=[]

    for r in results:
        for box in r.boxes:

            cls=int(box.cls[0])

            if cls in vehicle_classes:

                x1,y1,x2,y2=map(int,box.xyxy[0])
                cx=int((x1+x2)/2)
                cy=int((y1+y2)/2)

                vehicles.append((cx,cy,x1,y1,x2,y2))

    return vehicles