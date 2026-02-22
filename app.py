from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import random
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

traffic_state = {
    "north": 0,
    "south": 0,
    "east": 0,
    "west": 0,
    "active_lane": "north",
    "timer": 30,
    "emergency": False,
    "logs": []
}

def log_event(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    traffic_state["logs"].insert(0, f"[{timestamp}] {message}")
    traffic_state["logs"] = traffic_state["logs"][:10]

def traffic_engine():
    while True:
        # Simulate vehicle detection
        traffic_state["north"] = random.randint(10, 100)
        traffic_state["south"] = random.randint(10, 100)
        traffic_state["east"] = random.randint(10, 100)
        traffic_state["west"] = random.randint(10, 100)

        # Emergency randomly
        traffic_state["emergency"] = random.choice([False, False, False, True])

        if traffic_state["emergency"]:
            traffic_state["active_lane"] = random.choice(["north","south","east","west"])
            traffic_state["timer"] = 20
            log_event("🚑 Emergency detected! Override activated.")
        else:
            # Choose highest density lane
            lane = max(["north","south","east","west"], 
                       key=lambda x: traffic_state[x])
            traffic_state["active_lane"] = lane
            traffic_state["timer"] = 30 + traffic_state[lane] // 2
            log_event(f"AI allocated green to {lane.upper()} lane.")

        socketio.emit("update", traffic_state)

        time.sleep(3)

@app.route("/")
def home():
    return render_template("dashboard.html")

if __name__ == "__main__":
    thread = threading.Thread(target=traffic_engine)
    thread.daemon = True
    thread.start()
    socketio.run(app, host="127.0.0.1", port=5055, debug=False)