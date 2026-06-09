import os
import requests
import datetime

def calculate_oidio_risk(temp, humidity, wind_kph):
    if wind_kph > 25: return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ (Λόγω ισχυρών ανέμων)"
    if 21 <= temp <= 30 and humidity > 60: return "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif 15 <= temp <= 30: return "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else: return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"

api_key = os.environ.get("WEATHER_API_KEY")
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q=Tripoli"

try:
    data = requests.get(url).json()
    curr = data['current']
    fcasts = data['forecast']['forecastday']
    
    with open("result_oidio.txt", "w", encoding="utf-8") as f:
        f.write(f"Τελευταία ενημέρωση: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        def write_section(title, risk, t, h, w):
            f.write(f"{title} ---\n")
            f.write(f"Κίνδυνος: {risk}\n")
            f.write(f"Θερμοκρασία: {t}°C\n")
            f.write(f"Υγρασία: {h}%\n")
            f.write(f"Άνεμος: {w} km/h\n")
            f.write("Διαβροχή: Όχι\n---\n")

        write_section("ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ", calculate_oidio_risk(curr['temp_c'], curr['humidity'], curr['wind_kph']), curr['temp_c'], curr['humidity'], curr['wind_kph'])
        write_section("ΠΡΟΒΛΕΨΗ ΣΗΜΕΡΑ", calculate_oidio_risk(fcasts[0]['day']['avgtemp_c'], fcasts[0]['day']['avghumidity'], fcasts[0]['day']['maxwind_kph']), fcasts[0]['day']['avgtemp_c'], fcasts[0]['day']['avghumidity'], fcasts[0]['day']['maxwind_kph'])
        write_section("ΠΡΟΒΛΕΨΗ ΑΥΡΙΟ", calculate_oidio_risk(fcasts[1]['day']['avgtemp_c'], fcasts[1]['day']['avghumidity'], fcasts[1]['day']['maxwind_kph']), fcasts[1]['day']['avgtemp_c'], fcasts[1]['day']['avghumidity'], fcasts[1]['day']['maxwind_kph'])
except Exception as e:
    print(f"Error: {e}")