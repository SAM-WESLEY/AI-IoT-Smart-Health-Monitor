class DataProcessor:
    def process(self, raw):
        """Clean and validate raw sensor readings."""
        hr   = self._clamp(float(raw.get('heart_rate',  72)),  30, 200)
        spo2 = self._clamp(float(raw.get('spo2',        98)),  50, 100)
        temp = self._clamp(float(raw.get('temperature', 36.8)), 30, 45)
        return {"heart_rate": int(hr), "spo2": int(spo2), "temperature": round(temp, 1)}

    def _clamp(self, val, lo, hi):
        return max(lo, min(hi, val))
