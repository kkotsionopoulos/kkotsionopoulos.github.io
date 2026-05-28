import os
import requests
import datetime

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_data():
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=37.51,22.38"
        data = requests.get(url, timeout=10).json()
        t = data['current']['temp_c']
        h = data['current']['humidity']
        w = data['current']['wind_kph']
        
        # Λογική ανάλυσης
        risk = "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"
        reason = "Συνθήκες εντός ορίων."
        
        if h > 75 and 15 <= t <= 25:
            risk = "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
            reason = f"Υγρασία {h}% (>75%) & Θερμοκρασία {t}°C ιδανική για μύκητα."
        elif h > 60:
            risk = "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
            reason = f"Υγρασία {h}% (>60%) - Απαιτείται προσοχή."
            
        return t, h, w, risk, reason
    except:
        return 0, 0, 0, "Σφάλμα", "Δεν βρέθηκαν δεδομένα"

t, h, w, risk, reason = get_data()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

content = f"""Τελευταία ενημέρωση: {now}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ ---
Κατάσταση: {risk}
Αιτιολόγηση: {reason}
Μετρήσεις: {t}°C, {h}% υγρασία, {w} km/h άνεμος
"""

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)