import os
import requests
import datetime

def calculate_oidio_risk(temp, humidity, wind_kph):
    if wind_kph > 25:
        return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ (Λόγω ισχυρών ανέμων)"
    if 21 <= temp <= 30 and humidity > 60:
        return "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif 15 <= temp <= 30:
        return "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else:
        return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"

# Ανάκτηση δεδομένων
api_key = os.environ.get("WEATHER_API_KEY")
city = "Tripoli"
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}"

try:
    response = requests.get(url).json()
    
    # Τρέχοντα δεδομένα
    current = response['current']
    
    # Δεδομένα πρόβλεψης (Η λίστα forecastday)
    forecast_days = response['forecast']['forecastday']
    
    # Σήμερα (forecast_days[0])
    today = forecast_days[0]['day']
    # Αύριο (forecast_days[1])
    tomorrow = forecast_days[1]['day']

    # Εγγραφή στο αρχείο
    with open("result_oidio.txt", "w", encoding="utf-8") as f:
        f.write(f"Τελευταία ενημέρωση: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        def write_section(title, risk, t, h, w, r):
            f.write(f"{title} ---\n")
            f.write(f"Κίνδυνος: {risk}\n")
            f.write(f"Θερμοκρασία: {t}°C | Υγρασία: {h}% | Άνεμος: {w} km/h | Διαβροχή: {r}\n")
            f.write("---\n")

        # Εγγραφή με διαφορετικές τιμές
        write_section("ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ", calculate_oidio_risk(current['temp_c'], current['humidity'], current['wind_kph']), current['temp_c'], current['humidity'], current['wind_kph'], "0 mm")
        write_section("ΠΡΟΒΛΕΨΗ ΣΗΜΕΡΑ", calculate_oidio_risk(today['avgtemp_c'], today['avghumidity'], today['maxwind_kph']), today['avgtemp_c'], today['avghumidity'], today['maxwind_kph'], "0 mm")
        write_section("ΠΡΟΒΛΕΨΗ ΑΥΡΙΟ", calculate_oidio_risk(tomorrow['avgtemp_c'], tomorrow['avghumidity'], tomorrow['maxwind_kph']), tomorrow['avgtemp_c'], tomorrow['avghumidity'], tomorrow['maxwind_kph'], "0 mm")

except Exception as e:
    print(f"Σφάλμα: {e}")