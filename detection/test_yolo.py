from detect import get_traffic_data

density, ambulance = get_traffic_data()

print("Lane Density (%):", density)
print("Ambulance:", ambulance)