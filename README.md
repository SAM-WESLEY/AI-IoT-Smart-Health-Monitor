# AI-Driven IoT Smart Health Monitoring & Predictive Healthcare System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/ESP32-IoT%20Hardware-E7352C?style=for-the-badge&logo=espressif&logoColor=white"/>
  <img src="https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-Dashboard-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Firebase-Cloud-FFCA28?style=for-the-badge&logo=firebase&logoColor=black"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

> An intelligent real-time patient monitoring system using ESP32 IoT sensors and AI-based predictive analytics — continuously monitoring vital signs and predicting potential health risks before they become emergencies.

---

## 📌 Overview

AI-Driven IoT Smart Health Monitoring System is a complete end-to-end healthcare IoT solution that bridges hardware sensor data with machine learning predictions. ESP32 microcontrollers collect real-time vitals — heart rate, SpO2, and body temperature — which are streamed to the cloud and analysed by an ML prediction engine that flags early signs of health deterioration, triggering instant alerts to caregivers and doctors.

---

## ✨ Features

- ❤️ **Real-time heart rate monitoring** — MAX30102 pulse oximeter sensor
- 🫁 **SpO2 tracking** — blood oxygen saturation level monitoring
- 🌡️ **Body temperature sensing** — DS18B20 digital temperature sensor
- 📡 **Cloud-based remote monitoring** — Firebase Realtime DB sync
- 🚨 **Emergency alert system** — instant SMS + email on critical readings
- 🧠 **AI-based disease prediction** — Random Forest ML risk classifier
- 📊 **Live dashboard visualisation** — real-time charts + vitals history
- ⚡ **Demo mode** — simulate live vitals without hardware

---

## 🏗️ System Architecture

```
[ESP32 + Sensors]
    ├── MAX30102  → Heart Rate + SpO2
    ├── DS18B20   → Body Temperature
    └── WiFi      → Data Transmission
         ↓
[Firebase Realtime Database]
         ↓
[ML Prediction Engine]
    ├── Random Forest    → Risk Classification
    ├── Rule-based engine → Threshold alerts
    └── Alert Trigger    → Email + SMS
         ↓
[Flask Web Dashboard]
    ├── Live vitals cards
    ├── Real-time charts
    ├── Risk level indicator
    └── Alert history log
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| IoT Hardware | ESP32 + MAX30102 + DS18B20 |
| Firmware | Arduino C++ (ESP32) |
| Cloud Database | Firebase Realtime DB |
| ML Engine | Scikit-learn (Random Forest) |
| Backend | Flask (Python) |
| Frontend | HTML + CSS + Chart.js |
| Alerts | SMTP Email + Twilio SMS |
| Data Processing | Pandas, NumPy |

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install flask scikit-learn numpy pandas firebase-admin twilio
```

### Run the Dashboard
```bash
git clone https://github.com/SAM-WESLEY/AI-IoT-Smart-Health-Monitor
cd AI-IoT-Smart-Health-Monitor
cp config.example.json config.json
python app.py
```

### Access Dashboard
Open any browser:
```
http://localhost:5000
```

### Demo Mode (No Hardware Needed)
Click the **⚡ Simulate** button on the dashboard to generate live vitals.

---

## 📊 Vital Sign Thresholds

| Parameter | Normal | Warning | Critical |
|---|---|---|---|
| Heart Rate | 60–100 BPM | <55 or >110 | <45 or >130 |
| SpO2 | 95–100% | 91–94% | <90% |
| Temperature | 36.1–37.2°C | 37.3–38.5°C | >38.5°C |

---

## 🚨 Risk Levels

| Level | Color | Action |
|---|---|---|
| NORMAL | 🟢 Green | No action needed |
| WARNING | 🟡 Yellow | Notify caregiver |
| HIGH RISK | 🟠 Orange | Alert doctor |
| CRITICAL | 🔴 Red | Emergency — call ambulance |

---

## 🗂️ Project Structure

```
AI-IoT-Smart-Health-Monitor/
├── app.py                          # Main Flask application + monitor loop
├── config.example.json             # Firebase + Email + Twilio config template
├── modules/
│   ├── firebase_client.py          # Firebase Realtime DB client + demo mode
│   ├── ml_predictor.py             # Random Forest risk prediction engine
│   ├── alert_system.py             # Email (Gmail) + SMS (Twilio) alerts
│   └── data_processor.py           # Vitals validation and cleaning
├── esp32/
│   └── health_monitor.ino          # Full Arduino firmware for ESP32
├── models/
│   └── health_risk_model.pkl       # Trained Random Forest model
├── templates/
│   └── index.html                  # Live health dashboard
├── static/
│   └── style.css
├── requirements.txt
└── README.md
```

---

## 🌍 Applications

- 🏥 Remote patient monitoring in hospitals
- 👴 Elderly care and home healthcare
- 🏨 Smart hospital infrastructure
- 📱 Telemedicine and digital health platforms

---

## 🔮 Future Scope

- ⌚ Wearable device integration (smartwatch)
- 🤖 AI doctor chatbot for symptom analysis
- 📱 Mobile health app (Android / iOS)
- 🧬 ECG monitoring module

---

## 📬 Contact

**Sam Wesley S**
📧 samwesley@karunya.edu.in
🔗 [LinkedIn](https://linkedin.com/in/samwesleys)
🐙 [GitHub](https://github.com/SAM-WESLEY)

---

<p align="center">
  <i>Built with ❤️ at Karunya Institute of Technology and Sciences</i>
</p>

<p align="center">If this project helped you, please give it a ⭐</p>
