import json
import os
import random
import time

CONFIG_PATH = 'config.json'


class FirebaseClient:
    def __init__(self):
        self.db   = None
        self.demo = True
        self._connect()

    def _connect(self):
        if not os.path.exists(CONFIG_PATH):
            print("[Firebase] config.json not found — running in DEMO mode.")
            return

        try:
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)

            import firebase_admin
            from firebase_admin import credentials, db

            cred = credentials.Certificate(cfg.get('firebase_credentials', {}))
            firebase_admin.initialize_app(cred, {
                'databaseURL': cfg.get('firebase_url', '')
            })
            self.db   = db
            self.demo = False
            print("[Firebase] Connected to Firebase Realtime DB.")
        except Exception as e:
            print(f"[Firebase] Connection failed: {e} — running in DEMO mode.")

    def get_latest_vitals(self):
        """Fetch latest vitals from Firebase or generate demo data."""
        if self.demo:
            return self._demo_vitals()

        try:
            ref  = self.db.reference('/vitals/latest')
            data = ref.get()
            return data if data else self._demo_vitals()
        except Exception as e:
            print(f"[Firebase] Read error: {e}")
            return self._demo_vitals()

    def push_vitals(self, vitals):
        """Push vitals to Firebase (called from ESP32 via REST or Python)."""
        if self.demo:
            return
        try:
            ref = self.db.reference('/vitals/latest')
            ref.set(vitals)
            ref2 = self.db.reference('/vitals/history')
            ref2.push(vitals)
        except Exception as e:
            print(f"[Firebase] Write error: {e}")

    def _demo_vitals(self):
        """Generate realistic simulated vitals for demo."""
        t = time.time()
        # Simulate slight variations
        hr   = int(72 + 10 * abs(hash(str(int(t/5))) % 10 - 5) / 5)
        spo2 = int(97 + (hash(str(int(t/7))) % 4) - 2)
        temp = round(36.8 + (hash(str(int(t/11))) % 10 - 5) / 10, 1)
        return {
            "heart_rate":  max(50, min(130, hr)),
            "spo2":        max(85, min(100, spo2)),
            "temperature": max(35.0, min(40.0, temp)),
            "timestamp":   time.strftime("%Y-%m-%d %H:%M:%S"),
        }
