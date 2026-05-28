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
        
        c_temp = curr['current']['temp_c']
        c_hum = curr['current']['humidity']
        c_wind = curr['current']['wind_kph']
        
        day_data = hist['forecast']['forecastday'][0]['day']
        h_temp = day_data['avgtemp_c']
        h_hum = day_data['avghumidity']
        
        return c_temp, c_hum, c_wind, h_temp, h_hum
    except:
        return None, None, None, None, None

def get_risk_analysis(temp, hum, wind):
    # Γεωπονικά Όρια (Thresholds)
    HUM_LIMIT = 75
    TEMP_MIN, TEMP_MAX = 15, 25
    WIND_LIMIT = 20
    
    factors = []
    if hum > HUM_LIMIT: factors.append(f"Υγρασία {hum}% (> {HUM_LIMIT}%) -> Ευνοεί τη βλάστηση.")
    if TEMP_MIN <= temp <= TEMP_MAX: factors.append(f"Θερμοκρασία {temp}°C (Εντός ορίων {TEMP_MIN}-{TEMP_MAX}°C).")
    if wind > WIND_LIMIT: factors.append(f"Άνεμος {wind} km/h (> {WIND_LIMIT} km/h) -> Υψηλή διασπορά.")
    elif wind < 2: factors.append("Άπνοια -> Ευνοείται η στασιμότητα υγρασίας στο φύλλωμα.")
    
    if hum > HUM_LIMIT and TEMP_MIN <= temp <= TEMP_MAX: risk = "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif hum > 60: risk = "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else: risk = "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    
    return risk, " | ".join(factors)

c_t, c_h, c_w, h_t, h_h = get_weather_data()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
risk, analysis = get_risk_analysis(c_t, c_h, c_w)

content = f"""Τελευταία ενημέρωση: {now}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ (ΤΩΡΑ) ---
Κατάσταση: {risk}
Αιτιολόγηση: {analysis}
Τιμές: Θερμοκρασία {c_t}°C, Υγρασία {c_h}%, Άνεμος {c_w} km/h

--- ΜΕΣΟΙ ΟΡΟΙ ΠΡΟΗΓΟΥΜΕΝΗΣ ΗΜΕΡΑΣ ---
Θερμοκρασία: {h_t}°C
Υγρασία: {h_h}%
"""

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)