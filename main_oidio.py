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
    current = response['current']
    
    temp = current['temp_c']
    hum = current['humidity']
    wind = current['wind_kph']
    precip = current['precip_mm']
    
    # Υπολογισμός κειμένου διαβροχής
    rain_text = f"{precip} mm" if precip > 0 else "Όχι"
    risk = calculate_oidio_risk(temp, hum, wind)
    
    # Εγγραφή στο αρχείο
    with open("result_oidio.txt", "w", encoding="utf-8") as f:
        f.write(f"Τελευταία ενημέρωση: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        def write_section(title, risk, t, h, w, r):
            f.write(f"{title} ---\n")
            f.write(f"Κίνδυνος: {risk}\n")
            f.write(f"Θερμοκρασία: {t}°C | Υγρασία: {h}% | Άνεμος: {w} km/h | Διαβροχή: {r}\n")
            f.write("---\n")

        # Εγγραφή των ενοτήτων
        write_section("ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ", risk, temp, hum, wind, rain_text)
        write_section("ΠΡΟΒΛΕΨΗ ΣΗΜΕΡΑ", risk, temp, hum, wind, "Όχι")
        write_section("ΠΡΟΒΛΕΨΗ ΑΥΡΙΟ", risk, temp, hum, wind, "Όχι")
        
except Exception as e:
    print(f"Σφάλμα κατά την ανάκτηση δεδομένων: {e}")