import os
import requests
import datetime

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_risk_score(temp, hum):
    score = int((min(hum / 0.75, 100) * 0.6) + (max(0, 100 - (abs(20 - temp) * 5)) * 0.4))
    if score > 70: return f"ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ ({score}%)"
    elif score > 40: return f"ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ ({score}%)"
    return f"ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ ({score}%)"

def get_weather_data():
    lat, lon = "37.51", "22.38"
    base_url = "http://api.weatherapi.com/v1"
    try:
        curr = requests.get(f"{base_url}/current.json?key={WEATHER_API_KEY}&q={lat},{lon}").json()
        hist = requests.get(f"{base_url}/history.json?key={WEATHER_API_KEY}&q={lat},{lon}&dt={(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')}").json()
        fore = requests.get(f"{base_url}/forecast.json?key={WEATHER_API_KEY}&q={lat},{lon}&days=3").json()
        
        c = curr['current']
        h = hist['forecast']['forecastday'][0]['day']
        f_today = fore['forecast']['forecastday'][0]
        f_tom = fore['forecast']['forecastday'][1]
        
        d_temp = c['temp_c'] - h['avgtemp_c']
        d_hum = c['humidity'] - h['avghumidity']
        
        content = f"""Τελευταία ενημέρωση: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ ---
Κατάσταση: {get_risk_score(c['temp_c'], c['humidity'])}
Θερμοκρασία: {c['temp_c']}°C ({'+' if d_temp > 0 else ''}{d_temp:.1f}°) | Υγρασία: {c['humidity']}% ({'+' if d_hum > 0 else ''}{d_hum:.0f}%) | Άνεμος: {c['wind_kph']} km/h

--- ΠΡΟΒΛΕΨΗ ΓΙΑ ΣΗΜΕΡΑ ({f_today['date']}) ---
Θερμοκρασία: {f_today['day']['avgtemp_c']}°C | Υγρασία: {f_today['day']['avghumidity']}% | Μέγ. Άνεμος: {f_today['day']['maxwind_kph']} km/h

--- ΠΡΟΒΛΕΨΗ ΓΙΑ ΑΥΡΙΟ ({f_tom['date']}) ---
Θερμοκρασία: {f_tom['day']['avgtemp_c']}°C | Υγρασία: {f_tom['day']['avghumidity']}% | Μέγ. Άνεμος: {f_tom['day']['maxwind_kph']} km/h
"""
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Σφάλμα: {e}")

get_weather_data()