from flask import Flask, render_template, jsonify
import threading
import time
from modules.firebase_client import FirebaseClient
from modules.ml_predictor    import MLPredictor
from modules.alert_system    import AlertSystem
from modules.data_processor  import DataProcessor

app       = Flask(__name__)
firebase  = FirebaseClient()
predictor = MLPredictor()
alerter   = AlertSystem()
processor = DataProcessor()

# ── Shared State ───────────────────────────────────────────────────────────────
state = {
    "heart_rate":   0,
    "spo2":         0,
    "temperature":  0.0,
    "risk_level":   "NORMAL",
    "risk_score":   0.0,
    "alert_count":  0,
    "last_updated": "—",
    "history":      [],
}


def monitor_loop():
    """Continuously fetch vitals from Firebase and run ML prediction."""
    while True:
        try:
            vitals = firebase.get_latest_vitals()
            if vitals:
                processed = processor.process(vitals)
                risk      = predictor.predict(processed)

                state["heart_rate"]   = processed["heart_rate"]
                state["spo2"]         = processed["spo2"]
                state["temperature"]  = processed["temperature"]
                state["risk_level"]   = risk["level"]
                state["risk_score"]   = risk["score"]
                state["last_updated"] = time.strftime("%H:%M:%S")

                # Keep rolling history (last 30 readings)
                state["history"].append({
                    "time":        state["last_updated"],
                    "heart_rate":  processed["heart_rate"],
                    "spo2":        processed["spo2"],
                    "temperature": processed["temperature"],
                    "risk":        risk["level"],
                })
                if len(state["history"]) > 30:
                    state["history"].pop(0)

                # Trigger alert if needed
                if risk["level"] in ("HIGH RISK", "CRITICAL"):
                    alerter.send_alert(state)
                    state["alert_count"] += 1

        except Exception as e:
            print(f"[Monitor] Error: {e}")

        time.sleep(5)


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status')
def status():
    return jsonify(state)


@app.route('/history')
def history():
    return jsonify(state["history"])


@app.route('/simulate')
def simulate():
    """Simulate sensor data for demo purposes."""
    import random
    state["heart_rate"]   = random.randint(55, 120)
    state["spo2"]         = random.randint(88, 100)
    state["temperature"]  = round(random.uniform(35.5, 39.5), 1)
    state["last_updated"] = time.strftime("%H:%M:%S")
    risk = predictor.predict({
        "heart_rate":  state["heart_rate"],
        "spo2":        state["spo2"],
        "temperature": state["temperature"],
    })
    state["risk_level"] = risk["level"]
    state["risk_score"] = risk["score"]
    state["history"].append({
        "time":        state["last_updated"],
        "heart_rate":  state["heart_rate"],
        "spo2":        state["spo2"],
        "temperature": state["temperature"],
        "risk":        risk["level"],
    })
    if len(state["history"]) > 30:
        state["history"].pop(0)
    return jsonify({"status": "simulated", "data": state})


if __name__ == '__main__':
    t = threading.Thread(target=monitor_loop, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
