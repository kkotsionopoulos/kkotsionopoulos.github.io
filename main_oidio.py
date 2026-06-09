import os
import requests
import datetime

# Συνάρτηση κινδύνου
def calculate_oidio_risk(temp, humidity, wind_kph):
    if wind_kph > 25: return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ (Ισχυροί άνεμοι)"
    if 21 <= temp <= 30 and humidity > 60: return "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif 15 <= temp <= 30: return "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else: return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"

api_key = os.environ.get("WEATHER_API_KEY")
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q=Tripoli&days=3"

try:
    data = requests.get(url).json()
    curr = data['current']
    fcasts = data['forecast']['forecastday']
    
    with open("result_oidio.txt", "w", encoding="utf-8") as f:
        f.write(f"Τελευταία ενημέρωση: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        # Στιγμιαία Κατάσταση (από το curr)
        f.write("ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ ---\n")
        f.write(f"Κίνδυνος: {calculate_oidio_risk(curr['temp_c'], curr['humidity'], curr['wind_kph'])}\n")
        f.write(f"Θερμοκρασία: {curr['temp_c']}\nΥγρασία: {curr['humidity']}\nΆνεμος: {curr['wind_kph']}\n---\n")

        # Πρόβλεψη Σήμερα (από fcasts[0])
        f.write("ΠΡΟΒΛΕΨΗ ΣΗΜΕΡΑ ---\n")
        f.write(f"Κίνδυνος: {calculate_oidio_risk(fcasts[0]['day']['avgtemp_c'], fcasts[0]['day']['avghumidity'], fcasts[0]['day']['maxwind_kph'])}\n")
        f.write(f"Θερμοκρασία: {fcasts[0]['day']['avgtemp_c']}\nΥγρασία: {fcasts[0]['day']['avghumidity']}\nΆνεμος: {fcasts[0]['day']['maxwind_kph']}\n---\n")

        # Πρόβλεψη Αύριο (από fcasts[1])
        f.write("ΠΡΟΒΛΕΨΗ ΑΥΡΙΟ ---\n")
        f.write(f"Κίνδυνος: {calculate_oidio_risk(fcasts[1]['day']['avgtemp_c'], fcasts[1]['day']['avghumidity'], fcasts[1]['day']['maxwind_kph'])}\n")
        f.write(f"Θερμοκρασία: {fcasts[1]['day']['avgtemp_c']}\nΥγρασία: {fcasts[1]['day']['avghumidity']}\nΆνεμος: {fcasts[1]['day']['maxwind_kph']}\n---\n")

except Exception as e:
    print(f"Σφάλμα: {e}")