import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

CONFIG_PATH = 'config.json'
COOLDOWN    = 300   # seconds between repeated alerts for same patient


class AlertSystem:
    def __init__(self):
        self.cfg          = {}
        self.last_alert   = 0
        self._load_config()

    def _load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH) as f:
                    self.cfg = json.load(f)
            except Exception:
                pass

    def send_alert(self, state):
        """Send email + SMS alert for critical vitals."""
        now = datetime.now().timestamp()
        if now - self.last_alert < COOLDOWN:
            return   # Prevent alert spam

        self.last_alert = now
        subject = f"🚨 HEALTH ALERT — {state['risk_level']} Detected"
        body    = self._compose_body(state)

        self._send_email(subject, body)
        self._send_sms(body)

    def _compose_body(self, state):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
HEALTH MONITORING ALERT
{'='*40}
Time       : {ts}
Risk Level : {state['risk_level']}
Risk Score : {state['risk_score']:.1%}

CURRENT VITALS
{'='*40}
Heart Rate  : {state['heart_rate']} BPM
SpO2        : {state['spo2']}%
Temperature : {state['temperature']}°C

ACTION REQUIRED: Please check on the patient immediately.

— AI-Driven IoT Smart Health Monitoring System
  Karunya Institute of Technology and Sciences
"""

    def _send_email(self, subject, body):
        cfg = self.cfg.get('email', {})
        if not cfg.get('enabled', False):
            print(f"[AlertSystem] Email disabled. Alert: {subject}")
            return
        try:
            msg            = MIMEMultipart()
            msg['From']    = cfg['sender']
            msg['To']      = cfg['recipient']
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(cfg['sender'], cfg['password'])
                server.send_message(msg)
            print(f"[AlertSystem] Email alert sent to {cfg['recipient']}")
        except Exception as e:
            print(f"[AlertSystem] Email failed: {e}")

    def _send_sms(self, body):
        cfg = self.cfg.get('twilio', {})
        if not cfg.get('enabled', False):
            print("[AlertSystem] SMS disabled.")
            return
        try:
            from twilio.rest import Client
            client = Client(cfg['account_sid'], cfg['auth_token'])
            client.messages.create(
                body=body[:160],
                from_=cfg['from_number'],
                to=cfg['to_number']
            )
            print(f"[AlertSystem] SMS sent to {cfg['to_number']}")
        except Exception as e:
            print(f"[AlertSystem] SMS failed: {e}")
