from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import random
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

traffic_data = {
    "north": 0,
    "south": 0,
    "east": 0,
    "west": 0,
    "signal": "RED",
    "emergency": False
}

def update_traffic():
    while True:
        traffic_data["north"] = random.randint(10, 100)
        traffic_data["south"] = random.randint(10, 100)
        traffic_data["east"] = random.randint(10, 100)
        traffic_data["west"] = random.randint(10, 100)

        # Change signal randomly
        traffic_data["signal"] = random.choice(["RED", "GREEN", "YELLOW"])

        # Random emergency simulation
        traffic_data["emergency"] = random.choice([False, False, False, True])

        socketio.emit("traffic_update", traffic_data)
        time.sleep(3)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    thread = threading.Thread(target=update_traffic)
    thread.start()
if __name__ == "__main__":
    thread = threading.Thread(target=update_traffic)
    thread.daemon = True
    thread.start()

    socketio.run(app, host="127.0.0.1", port=5050, debug=False)