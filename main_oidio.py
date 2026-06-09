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
    temp = current['temp_c']
    hum = current['humidity']
    wind = current['wind_kph']
    rain = current['precip_mm']
    rain_text = f"{rain} mm" if rain > 0 else "Όχι"
    
    # Δεδομένα πρόβλεψης
    forecast_days = response['forecast']['forecastday']
    today = forecast_days[0]['day']
    tomorrow = forecast_days[1]['day']

    # Υπολογισμός ρίσκου για κάθε περίπτωση
    risk_now = calculate_oidio_risk(temp, hum, wind)
    risk_today = calculate_oidio_risk(today['avgtemp_c'], today['avghumidity'], today['maxwind_kph'])
    risk_tom = calculate_oidio_risk(tomorrow['avgtemp_c'], tomorrow['avghumidity'], tomorrow['maxwind_kph'])

    # Εγγραφή στο αρχείο
    with open("result_oidio.txt", "w", encoding="utf-8") as f:
        f.write(f"Τελευταία ενημέρωση: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        def write_section(title, risk, t, h, w, r):
            f.write(f"{title} ---\n")
            f.write(f"Κίνδυνος: {risk}\n")
            f.write(f"Θερμοκρασία: {t}°C\n")
            f.write(f"Υγρασία: {h}%\n")
            f.write(f"Άνεμος: {w} km/h\n")
            f.write(f"Διαβροχή: {r}\n")
            f.write("---\n")

        write_section("ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ", risk_now, temp, hum, wind, rain_text)
        write_section("ΠΡΟΒΛΕΨΗ ΣΗΜΕΡΑ", risk_today, today['avgtemp_c'], today['avghumidity'], today['maxwind_kph'], "0 mm")
        write_section("ΠΡΟΒΛΕΨΗ ΑΥΡΙΟ", risk_tom, tomorrow['avgtemp_c'], tomorrow['avghumidity'], tomorrow['maxwind_kph'], "0 mm")

except Exception as e:
    print(f"Σφάλμα κατά την ανάκτηση: {e}")