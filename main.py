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
        h_w = day_data['maxwind_kph']
        
        return c_t, c_h, c_w, h_t, h_h, h_w
    except:
        return None, None, None, None, None, None

def get_risk_analysis(temp, hum, wind=None):
    # Λογική για τον κίνδυνο
    if hum > 75 and 15 <= temp <= 25: risk = "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif hum > 60: risk = "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else: risk = "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    
    # Προσθήκη αιτιολόγησης αν δοθεί άνεμος
    analysis = f"Υγρασία {hum}%"
    if wind:
        if wind > 20: analysis += f", Άνεμος {wind}km/h (Υψηλή διασπορά)"
        elif wind < 2: analysis += ", Άπνοια (Στασιμότητα υγρασίας)"
        
    return risk, analysis

c_t, c_h, c_w, h_t, h_h, h_w = get_weather_data()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

c_risk, c_analysis = get_risk_analysis(c_t, c_h, c_w)
h_risk, h_analysis = get_risk_analysis(h_t, h_h) # Χωρίς άνεμο για τα ιστορικά

content = f"""Τελευταία ενημέρωση: {now}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ (ΤΩΡΑ) ---
Κατάσταση: {c_risk}
Αιτιολόγηση: {c_analysis}
Θερμοκρασία: {c_t}°C, Υγρασία: {c_h}%, Άνεμος: {c_w} km/h

--- ΜΕΣΟΙ ΟΡΟΙ ΠΡΟΗΓΟΥΜΕΝΗΣ ΗΜΕΡΑΣ ---
Κατάσταση: {h_risk}
Αιτιολόγηση: {h_analysis}
Θερμοκρασία: {h_t}°C, Υγρασία: {h_h}%
Μέγιστος Άνεμος: {h_w} km/h
"""

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)