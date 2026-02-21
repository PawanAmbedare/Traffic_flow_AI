import cv2
from vehicle_detection import detect_vehicles
from ambulance_detection import detect_ambulance
from lane_counter import count_lanes
from emergency_logic import check_emergency

cap=cv2.VideoCapture("traffic.mp4")
frame_count=0

while True:

    ret,frame=cap.read()
    if not ret:
        break

    frame_count+=1
    if frame_count%2!=0:
        continue

    frame=cv2.resize(frame,(900,600))

    vehicles=detect_vehicles(frame)
    ambulance=detect_ambulance(frame)

    l1,l2,l3=count_lanes(vehicles)
    emergency,lane=check_emergency(ambulance)

    if emergency:
        green_lane=lane
    else:

        max_lane=max(l1,l2,l3)

        if max_lane==l1:
            green_lane="Lane1"
        elif max_lane==l2:
            green_lane="Lane2"
        else:
            green_lane="Lane3"

    print("Lane1:",l1,
          "Lane2:",l2,
          "Lane3:",l3,
          "Emergency:",emergency,
          "Priority:",green_lane)

    cv2.imshow("ATS AI",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()