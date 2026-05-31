import os
import requests
import datetime
import json

# Ρύθμιση API και παραμέτρων
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_risk_score(temp, hum, precip, offset, growth_stage):
    # 1. Κανόνας των 3 Δεκαδών (Αναμονή βλάστησης)
    if not growth_stage: 
        return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ (Αναμονή βλάστησης)"
    
    # 2. Calibration (Offset)
    adj_temp = temp + offset
    
    # 3. Leaf Wetness Estimation (Υγρασία > 85% και βροχόπτωση)
    leaf_wetness = (hum > 85 and precip > 0)
    
    # 4. Αλγόριθμος VineScore
    # Βασική βαθμολογία με βάση την υγρασία (60%) και θερμοκρασία (40%)
    score = (hum * 0.6) + (max(0, 100 - (abs(20 - adj_temp) * 5)) * 0.4)
    
    # Προσθήκη επιβάρυνσης αν υπάρχει Leaf Wetness
    if leaf_wetness: 
        score += 20
    
    score = min(score, 99)
    
    if score > 70: return f"ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ ({score:.0f}%)"
    elif score > 40: return f"ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ ({score:.0f}%)"
    return f"ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ ({score:.0f}%)"

def get_weather_data():
    lat, lon = "37.51", "22.38"
    base_url = "http://api.weatherapi.com/v1"
    
    # Υποθετικές ρυθμίσεις χρήστη (για το prototype)
    user_offset = 0 
    user_growth_stage = True
    
    try:
        curr = requests.get(f"{base_url}/current.json?key={WEATHER_API_KEY}&q={lat},{lon}").json()
        fore = requests.get(f"{base_url}/forecast.json?key={WEATHER_API_KEY}&q={lat},{lon}&days=3").json()
        
        c = curr['current']
        f_today = fore['forecast']['forecastday'][0]
        f_tom = fore['forecast']['forecastday'][1]
        
        content = f"""Τελευταία ενημέρωση: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}

--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ ---
Κίνδυνος: {get_risk_score(c['temp_c'], c['humidity'], c.get('precip_mm', 0), user_offset, user_growth_stage)}
Θερμοκρασία: {c['temp_c']}°C | Υγρασία: {c['humidity']}% | Άνεμος: {c['wind_kph']} km/h

--- ΠΡΟΒΛΕΨΗ ΓΙΑ ΣΗΜΕΡΑ ({f_today['date']}) ---
Κίνδυνος: {get_risk_score(f_today['day']['avgtemp_c'], f_today['day']['avghumidity'], f_today['day']['totalprecip_mm'], user_offset, user_growth_stage)}
Θερμοκρασία: {f_today['day']['avgtemp_c']}°C | Υγρασία: {f_today['day']['avghumidity']}% | Μέγ. Άνεμος: {f_today['day']['maxwind_kph']} km/h

--- ΠΡΟΒΛΕΨΗ ΓΙΑ ΑΥΡΙΟ ({f_tom['date']}) ---
Κίνδυνος: {get_risk_score(f_tom['day']['avgtemp_c'], f_tom['day']['avghumidity'], f_tom['day']['totalprecip_mm'], user_offset, user_growth_stage)}
Θερμοκρασία: {f_tom['day']['avgtemp_c']}°C | Υγρασία: {f_tom['day']['avghumidity']}% | Μέγ. Άνεμος: {f_tom['day']['maxwind_kph']} km/h
"""
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(content)
            
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_weather_data()