import os
import requests
import datetime

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_risk_score(temp, hum):
    # Υπολογισμός ποσοστού: Ιδανική υγρασία 75%, Θερμοκρασία 20°C
    hum_score = min(hum / 0.75, 100)
    temp_diff = abs(20 - temp)
    temp_score = max(0, 100 - (temp_diff * 5))
    score = int((hum_score * 0.6) + (temp_score * 0.4))
    
    if score > 70: label = "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif score > 40: label = "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else: label = "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    return f"{label} ({score}%)"

def get_weather_data():
    lat, lon = "37.51", "22.38"
    base_url = "http://api.weatherapi.com/v1"
    try:
        curr = requests.get(f"{base_url}/current.json?key={WEATHER_API_KEY}&q={lat},{lon}").json()
        fore = requests.get(f"{base_url}/forecast.json?key={WEATHER_API_KEY}&q={lat},{lon}&days=1").json()
        
        c = curr['current']
        f = fore['forecast']['forecastday'][0]['day']
        
        content = f"""Τελευταία ενημέρωση: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ ---
Κατάσταση: {get_risk_score(c['temp_c'], c['humidity'])}
Θερμοκρασία: {c['temp_c']}°C | Υγρασία: {c['humidity']}% | Άνεμος: {c['wind_kph']} km/h

--- ΠΡΟΒΛΕΨΗ ΓΙΑ ΣΗΜΕΡΑ ---
Κατάσταση: {get_risk_score(f['avgtemp_c'], f['avghumidity'])}
Θερμοκρασία: {f['avgtemp_c']}°C | Υγρασία: {f['avghumidity']}% | Μέγ. Άνεμος: {f['maxwind_kph']} km/h
"""
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Σφάλμα: {e}")

get_weather_data()