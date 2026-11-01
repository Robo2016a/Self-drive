from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

state = {
    "mode": "manual",
    "status": "Idle",
    "speed": 0.0,
    "steering": 0.0,
    "obstacle": False,
    "lane_center_offset": 0.0,
    "distance_to_obstacle": 999.0,
}


def clamp(value, lower=-1.0, upper=1.0):
    return max(lower, min(upper, value))


def set_state(status, speed=0.0, steering=0.0, obstacle=False, lane_center_offset=0.0, distance=999.0):
    state["status"] = status
    state["speed"] = float(speed)
    state["steering"] = float(steering)
    state["obstacle"] = bool(obstacle)
    state["lane_center_offset"] = float(lane_center_offset)
    state["distance_to_obstacle"] = float(distance)


def follow_lane():
    """Simple lane-following controller. This is a prototype, not full Tesla FSD."""
    lane_center_offset = 0.0
    obstacle = False
    distance = 999.0

    # Simulated sensor readout. Replace this with camera/ultrasonic data from real hardware.
    # A positive offset means the car is too far left; negative means too far right.
    lane_center_offset = -18.0
    obstacle = False
    distance = 2.8

    if distance < 1.5:
        set_state("STOP: obstacle detected", 0.0, 0.0, True, lane_center_offset, distance)
        return state["status"]

    # P controller: steer toward center of lane.
    steering = clamp(lane_center_offset / 120.0, -1.0, 1.0)

    if abs(lane_center_offset) < 15:
        speed = 0.8
        status = "Lane centered: maintaining course"
    elif lane_center_offset < 0:
        speed = 0.7
        status = "Adjusting right to keep lane"
    else:
        speed = 0.7
        status = "Adjusting left to keep lane"

    set_state(status, speed, steering, False, lane_center_offset, distance)
    return state["status"]


@app.route("/health")
def health():
    return jsonify({"ok": True, "mode": state["mode"], "status": state["status"]})


@app.route("/status")
def status():
    return jsonify(state)


@app.route("/drive")
def drive():
    action = (request.args.get("action") or "stop").lower()
    mode = (request.args.get("mode") or "manual").lower()
    state["mode"] = mode

    if mode == "auto":
        status_msg = follow_lane()
        return status_msg

    if action == "forward":
        set_state("Car moving forward", 0.8, 0.0, False, 0.0, 999.0)
        return "Car Moving Forward"
    elif action == "left":
        set_state("Car turning left", 0.6, -0.8, False, 0.0, 999.0)
        return "Car Turning Left"
    elif action == "right":
        set_state("Car turning right", 0.6, 0.8, False, 0.0, 999.0)
        return "Car Turning Right"
    elif action == "stop":
        set_state("Car stopped", 0.0, 0.0, False, 0.0, 999.0)
        return "Car Stopped"

    return "Unknown Command"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
