import os
import requests
import datetime

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_weather_data():
    base_url = "http://api.weatherapi.com/v1"
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    try:
        curr = requests.get(f"{base_url}/current.json?key={WEATHER_API_KEY}&q=Tripoli,Greece", timeout=10).json()
        hist = requests.get(f"{base_url}/history.json?key={WEATHER_API_KEY}&q=Tripoli,Greece&dt={yesterday}", timeout=10).json()
        
        c_t = curr['current']['temp_c']
        c_h = curr['current']['humidity']
        c_w = curr['current']['wind_kph']
        
        day_data = hist['forecast']['forecastday'][0]['day']
        h_t = day_data['avgtemp_c']
        h_h = day_data['avghumidity']
        h_w = day_data['maxwind_kph'] # Ο μέγιστος άνεμος της χθεσινής μέρας
        
        return c_t, c_h, c_w, h_t, h_h, h_w
    except:
        return None, None, None, None, None, None

def get_risk_analysis(temp, hum, wind):
    reasons = []
    if hum > 75: reasons.append(f"Υγρασία {hum}% (>75%) -> Υψηλός κίνδυνος.")
    if 15 <= temp <= 25: reasons.append(f"Θερμοκρασία {temp}°C -> Ιδανική για τον μύκητα.")
    if wind > 20: reasons.append(f"Άνεμος {wind} km/h -> Ευνοεί τη διασπορά.")
    elif wind < 2: reasons.append("Άπνοια -> Στασιμότητα υγρασίας.")
    
    if hum > 75 and 15 <= temp <= 25: risk = "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif hum > 60: risk = "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else: risk = "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    
    analysis = " | ".join(reasons) if reasons else "Συνθήκες εντός ορίων."
    return risk, analysis

c_t, c_h, c_w, h_t, h_h, h_w = get_weather_data()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
risk, analysis = get_risk_analysis(c_t, c_h, c_w)

content = f"""Τελευταία ενημέρωση: {now}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ (ΤΩΡΑ) ---
Κατάσταση: {risk}
Αιτιολόγηση: {analysis}
Θερμοκρασία: {c_t}°C, Υγρασία: {c_h}%, Άνεμος: {c_w} km/h

--- ΜΕΣΟΙ ΟΡΟΙ ΠΡΟΗΓΟΥΜΕΝΗΣ ΗΜΕΡΑΣ ---
Θερμοκρασία: {h_t}°C
Υγρασία: {h_h}%
Μέγιστος Άνεμος: {h_w} km/h
"""

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)