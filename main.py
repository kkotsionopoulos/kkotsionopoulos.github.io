import os
import requests
import datetime

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_weather_data():
    lat, lon = "37.51", "22.38" # Τρίπολη Αρκαδίας
    base_url = "http://api.weatherapi.com/v1"
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    try:
        curr = requests.get(f"{base_url}/current.json?key={WEATHER_API_KEY}&q={lat},{lon}", timeout=10).json()
        hist = requests.get(f"{base_url}/history.json?key={WEATHER_API_KEY}&q={lat},{lon}&dt={yesterday}", timeout=10).json()
        fore = requests.get(f"{base_url}/forecast.json?key={WEATHER_API_KEY}&q={lat},{lon}&days=2").json()
        
        c_t, c_h, c_w = curr['current']['temp_c'], curr['current']['humidity'], curr['current']['wind_kph']
        h_t = hist['forecast']['forecastday'][0]['day']['avgtemp_c']
        h_h = hist['forecast']['forecastday'][0]['day']['avghumidity']
        h_w = hist['forecast']['forecastday'][0]['day']['maxwind_kph']
        f_data = fore['forecast']['forecastday'][1]['day']
        f_t, f_h, f_w = f_data['avgtemp_c'], f_data['avghumidity'], f_data['maxwind_kph']
        
        return c_t, c_h, c_w, h_t, h_h, h_w, f_t, f_h, f_w
    except:
        return [None]*9

def get_risk(temp, hum):
    if hum > 75 and 15 <= temp <= 25: return "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif hum > 60: return "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else: return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"

c_t, c_h, c_w, h_t, h_h, h_w, f_t, f_h, f_w = get_weather_data()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

content = f"""Τελευταία ενημέρωση: {now}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ (ΤΩΡΑ) ---
Κατάσταση: {get_risk(c_t, c_h)}
Θερμοκρασία: {c_t}°C, Υγρασία: {c_h}%, Άνεμος: {c_w} km/h

--- ΜΕΣΟΙ ΟΡΟΙ ΠΡΟΗΓΟΥΜΕΝΗΣ ΗΜΕΡΑΣ ---
Κατάσταση: {get_risk(h_t, h_h)}
Θερμοκρασία: {h_t}°C, Υγρασία: {h_h}%, Μέγ. Άνεμος: {h_w} km/h

--- ΠΡΟΒΛΕΨΗ ΓΙΑ ΑΥΡΙΟ ---
Κατάσταση: {get_risk(f_t, f_h)}
Θερμοκρασία: {f_t}°C, Υγρασία: {f_h}%, Μέγ. Άνεμος: {f_w} km/h

--- ΕΠΕΞΗΓΗΣΗ & ΜΕΘΟΔΟΛΟΓΙΑ ---
Το VineWatch εντοπίζει τον κίνδυνο περονόσπορου βάσει των εξής ορίων:
1. ΥΨΗΛΟΣ: Υγρασία > 75% και Θερμοκρασία 15-25°C (Ιδανικές συνθήκες βλάστησης σπορίων).
2. ΜΕΤΡΙΟΣ: Υγρασία > 60% (Απαιτείται επιτήρηση του αμπελώνα).
3. Άνεμος: Ταχύτητες > 20 km/h ευνοούν τη διασπορά, ενώ άπνοια (<2 km/h) ευνοεί τη στασιμότητα υγρασίας.
Το σύστημα χρησιμοποιεί real-time δεδομένα από μετεωρολογικούς σταθμούς για την υποστήριξη αποφάσεων γεωργίας ακριβείας.
"""

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)
