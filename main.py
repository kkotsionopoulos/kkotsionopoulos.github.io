import os
import requests
import datetime

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_weather_data():
    lat, lon = "37.51", "22.38"
    base_url = "http://api.weatherapi.com/v1"
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    try:
        curr = requests.get(f"{base_url}/current.json?key={WEATHER_API_KEY}&q={lat},{lon}").json()
        hist = requests.get(f"{base_url}/history.json?key={WEATHER_API_KEY}&q={lat},{lon}&dt={yesterday}").json()
        fore = requests.get(f"{base_url}/forecast.json?key={WEATHER_API_KEY}&q={lat},{lon}&days=2").json()
        
        c = curr['current']
        h = hist['forecast']['forecastday'][0]['day']
        f = fore['forecast']['forecastday'][1]['day']
        
        content = f"""Τελευταία ενημέρωση: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ ---
Θερμοκρασία: {c['temp_c']}°C | Υγρασία: {c['humidity']}% | Άνεμος: {c['wind_kph']} km/h

--- ΜΕΣΟΙ ΟΡΟΙ ΠΡΟΗΓΟΥΜΕΝΗΣ ΗΜΕΡΑΣ ---
Θερμοκρασία: {h['avgtemp_c']}°C | Υγρασία: {h['avghumidity']}% | Μέγ. Άνεμος: {h['maxwind_kph']} km/h

--- ΠΡΟΒΛΕΨΗ ΓΙΑ ΑΥΡΙΟ ---
Θερμοκρασία: {f['avgtemp_c']}°C | Υγρασία: {f['avghumidity']}% | Μέγ. Άνεμος: {f['maxwind_kph']} km/h
"""
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        print(f"Σφάλμα: {e}")

get_weather_data()