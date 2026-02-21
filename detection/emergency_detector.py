import cv2
import numpy as np

def detect_emergency_vehicle(vehicle_crop):

    h, w, _ = vehicle_crop.shape

    # Ignore very small vehicles
    if w*h < 15000:
        return False

    hsv = cv2.cvtColor(vehicle_crop, cv2.COLOR_BGR2HSV)

    # Focus only on TOP 30% (where siren lights are)
    top_region = hsv[0:int(h*0.3), :]

    # RED MASK
    lower_red1 = np.array([0,120,70])
    upper_red1 = np.array([10,255,255])
    mask_red1 = cv2.inRange(top_region, lower_red1, upper_red1)

    lower_red2 = np.array([170,120,70])
    upper_red2 = np.array([180,255,255])
    mask_red2 = cv2.inRange(top_region, lower_red2, upper_red2)

    red_mask = mask_red1 + mask_red2

    # BLUE MASK
    lower_blue = np.array([100,150,0])
    upper_blue = np.array([140,255,255])
    blue_mask = cv2.inRange(top_region, lower_blue, upper_blue)

    combined_mask = red_mask + blue_mask

    pixel_count = cv2.countNonZero(combined_mask)

    # Now strict threshold
    if pixel_count > 2000:
        return True

    return False