import os
import requests
import datetime

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_weather_data():
    lat, lon = "37.51", "22.38"
    base_url = "http://api.weatherapi.com/v1"
    
    try:
        # Τρέχουσες, Ιστορικά, Πρόβλεψη για 2 ημέρες (για να πάρουμε το αύριο)
        curr = requests.get(f"{base_url}/current.json?key={WEATHER_API_KEY}&q={lat},{lon}").json()
        hist = requests.get(f"{base_url}/history.json?key={WEATHER_API_KEY}&q={lat},{lon}&dt={(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')}").json()
        fore = requests.get(f"{base_url}/forecast.json?key={WEATHER_API_KEY}&q={lat},{lon}&days=2").json()
        
        # Τρέχοντα
        c_t, c_h, c_w = curr['current']['temp_c'], curr['current']['humidity'], curr['current']['wind_kph']
        # Χθες
        h_t, h_h, h_w = hist['forecast']['forecastday'][0]['day']['avgtemp_c'], hist['forecast']['forecastday'][0]['day']['avghumidity'], hist['forecast']['forecastday'][0]['day']['maxwind_kph']
        # Αύριο
        f_data = fore['forecast']['forecastday'][1]['day']
        f_t, f_h, f_w = f_data['avgtemp_c'], f_data['avghumidity'], f_data['maxwind_kph']
        
        return c_t, c_h, c_w, h_t, h_h, h_w, f_t, f_h, f_w
    except:
        return [None]*9

def get_risk_analysis(temp, hum, wind=None):
    if hum > 75 and 15 <= temp <= 25: risk = "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif hum > 60: risk = "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else: risk = "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    return risk

c_t, c_h, c_w, h_t, h_h, h_w, f_t, f_h, f_w = get_weather_data()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

content = f"""Τελευταία ενημέρωση: {now}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ (ΤΩΡΑ) ---
Κατάσταση: {get_risk_analysis(c_t, c_h)}
Θερμοκρασία: {c_t}°C, Υγρασία: {c_h}%, Άνεμος: {c_w} km/h

--- ΠΡΟΗΓΟΥΜΕΝΗ ΗΜΕΡΑ (ΜΕΣΟΙ ΟΡΟΙ) ---
Κατάσταση: {get_risk_analysis(h_t, h_h)}
Θερμοκρασία: {h_t}°C, Υγρασία: {h_h}%, Μέγ. Άνεμος: {h_w} km/h

--- ΠΡΟΒΛΕΨΗ ΓΙΑ ΑΥΡΙΟ (ΜΕΣΟΙ ΟΡΟΙ) ---
Κατάσταση: {get_risk_analysis(f_t, f_h)}
Θερμοκρασία: {f_t}°C, Υγρασία: {f_h}%, Μέγ. Άνεμος: {f_w} km/h

*Σημείωση: Η πρόβλεψη αφορά την επικρατούσα τάση για το επόμενο 24ωρο.*
"""

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)