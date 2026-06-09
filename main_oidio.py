import os
import requests
import datetime  # Προσθήκη για την ώρα

def calculate_oidio_risk(temp, humidity, wind_kph):
    """
    Αλγόριθμος πρόβλεψης Ωιδίου
    """
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
    
    risk = calculate_oidio_risk(temp, hum, wind)
    
    # Εγγραφή με χρονική σήμανση για να ανανεώνεται το αρχείο στο GitHub
    # Εγγραφή στο αρχείο με τη σωστή δομή για το dashboard
    # ... (μέσα στο main_oidio.py)
    with open("result_oidio.txt", "w", encoding="utf-8") as f:
        f.write(f"Τελευταία ενημέρωση: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        # Λειτουργία που γράφει ομοιόμορφα τις ενότητες
        def write_section(title, risk, t, h, w, rain):
            f.write(f"{title} ---\n")
            f.write(f"Κίνδυνος: {risk}\n")
            f.write(f"Θερμοκρασία: {t}°C | Υγρασία: {h}% | Άνεμος: {w} km/h | Διαβροχή: {rain}\n")
            f.write("---\n")

        write_section("ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ", risk, temp, hum, wind, "Όχι")
        write_section("ΠΡΟΒΛΕΨΗ ΣΗΜΕΡΑ", risk, temp, hum, wind, "Όχι")
        write_section("ΠΡΟΒΛΕΨΗ ΑΥΡΙΟ", risk, temp, hum, wind, "Όχι")
        
except Exception as e:
    print(f"Σφάλμα κατά την ανάκτηση δεδομένων: {e}")