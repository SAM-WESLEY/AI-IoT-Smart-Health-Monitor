import numpy as np
import pickle
import os

MODEL_PATH = 'models/health_risk_model.pkl'

RISK_LEVELS = [
    (0.00, 0.30, "NORMAL",    "#22c55e"),
    (0.30, 0.55, "WARNING",   "#eab308"),
    (0.55, 0.75, "HIGH RISK", "#f97316"),
    (0.75, 1.01, "CRITICAL",  "#ef4444"),
]

# Rule-based thresholds (fallback)
def rule_based_score(hr, spo2, temp):
    score = 0.0
    # Heart rate scoring
    if hr < 45 or hr > 130:   score += 0.40
    elif hr < 55 or hr > 110: score += 0.20
    elif hr < 60 or hr > 100: score += 0.10
    # SpO2 scoring
    if spo2 < 90:   score += 0.45
    elif spo2 < 94: score += 0.25
    elif spo2 < 95: score += 0.10
    # Temperature scoring
    if temp > 38.5:   score += 0.30
    elif temp > 37.5: score += 0.15
    elif temp < 35.5: score += 0.25
    return min(score, 1.0)


class MLPredictor:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"[MLPredictor] Model loaded: {MODEL_PATH}")
            except Exception as e:
                print(f"[MLPredictor] Could not load model: {e}")
        else:
            print("[MLPredictor] No model found — using rule-based scoring.")

    def predict(self, vitals):
        hr   = vitals.get("heart_rate",  72)
        spo2 = vitals.get("spo2",        98)
        temp = vitals.get("temperature", 36.8)

        if self.model:
            try:
                features = np.array([[hr, spo2, temp]])
                score    = float(self.model.predict_proba(features)[0][1])
            except Exception:
                score = rule_based_score(hr, spo2, temp)
        else:
            score = rule_based_score(hr, spo2, temp)

        level = "NORMAL"
        color = "#22c55e"
        for low, high, lbl, clr in RISK_LEVELS:
            if low <= score < high:
                level = lbl
                color = clr
                break

        return {
            "score": round(score, 3),
            "level": level,
            "color": color,
        }

    def train(self, X, y):
        """Train Random Forest on labelled vitals data."""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        clf = RandomForestClassifier(
            n_estimators=100, random_state=42, class_weight='balanced')
        clf.fit(X_train, y_train)

        preds = clf.predict(X_test)
        print(classification_report(y_test, preds))

        os.makedirs('models', exist_ok=True)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(clf, f)

        self.model = clf
        print(f"[MLPredictor] Model saved to {MODEL_PATH}")
        return clf
