import os
import requests
import datetime

# Ρύθμιση API Key
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_risk_score(temp, hum, precip, offset, growth_stage):
    if not growth_stage: 
        return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ (Αναμονή βλάστησης)"
    
    adj_temp = temp + offset
    leaf_wetness = (hum > 85 and precip > 0)
    score = (hum * 0.6) + (max(0, 100 - (abs(20 - adj_temp) * 5)) * 0.4)
    
    if leaf_wetness: 
        score += 20
    
    score = min(score, 99)
    
    if score > 70: 
        return f"ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ ({score:.0f}%)"
    elif score > 40: 
        return f"ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ ({score:.0f}%)"
    return f"ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ ({score:.0f}%)"

def get_weather_data():
    print(f"DEBUG: Ξεκίνημα λήψης δεδομένων...") # Αυτό θα φανεί στο Log!
    lat, lon = "37.51", "22.38"
    base_url = "http://api.weatherapi.com/v1"
    
    try:
        curr = requests.get(f"{base_url}/current.json?key={WEATHER_API_KEY}&q={lat},{lon}").json()
        fore = requests.get(f"{base_url}/forecast.json?key={WEATHER_API_KEY}&q={lat},{lon}&days=3").json()
        
        c = curr['current']
        f_today = fore['forecast']['forecastday'][0]
        f_tom = fore['forecast']['forecastday'][1]
        
        # Λογική Διαβροχής
        wet_today = "Ναι" if f_today['day']['avghumidity'] > 85 and f_today['day']['totalprecip_mm'] > 0 else "Όχι"
        wet_tom = "Ναι" if f_tom['day']['avghumidity'] > 85 and f_tom['day']['totalprecip_mm'] > 0 else "Όχι"
        
        # Δημιουργία περιεχομένου με την τρέχουσα ώρα
        content = f"""Τελευταία ενημέρωση: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
--- ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ ---
Κίνδυνος: {get_risk_score(c['temp_c'], c['humidity'], c.get('precip_mm', 0), 0, True)}
Θερμοκρασία: {c['temp_c']}°C | Υγρασία: {c['humidity']}% | Άνεμος: {c['wind_kph']} km/h

--- ΠΡΟΒΛΕΨΗ ΣΗΜΕΡΑ ---
Κίνδυνος: {get_risk_score(f_today['day']['avgtemp_c'], f_today['day']['avghumidity'], f_today['day']['totalprecip_mm'], 0, True)}
Θερμοκρασία: {f_today['day']['avgtemp_c']}°C | Υγρασία: {f_today['day']['avghumidity']}% | Άνεμος: {f_today['day']['maxwind_kph']} km/h | Διαβροχή: {wet_today}

--- ΠΡΟΒΛΕΨΗ ΑΥΡΙΟ ---
Κίνδυνος: {get_risk_score(f_tom['day']['avgtemp_c'], f_tom['day']['avghumidity'], f_tom['day']['totalprecip_mm'], 0, True)}
Θερμοκρασία: {f_tom['day']['avgtemp_c']}°C | Υγρασία: {f_tom['day']['avghumidity']}% | Άνεμος: {f_tom['day']['maxwind_kph']} km/h | Διαβροχή: {wet_tom}"""
        
        with open("result.txt", "w", encoding="utf-8") as f: 
            f.write(content)
            
    except Exception as e: 
        print(f"Σφάλμα: {e}")

if __name__ == "__main__": 
    get_weather_data()