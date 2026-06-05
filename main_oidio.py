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
    with open("result_oidio.txt", "w", encoding="utf-8") as f:
        f.write(f"Τελευταία ενημέρωση: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"--- ΠΡΟΒΛΕΨΗ ΩΙΔΙΟΥ ---\n")
        f.write(f"Κίνδυνος: {risk}\n")
        f.write(f"Θερμοκρασία: {temp}°C\n")
        f.write(f"Υγρασία: {hum}%\n")
        f.write(f"Άνεμος: {wind} km/h")
        
except Exception as e:
    print(f"Σφάλμα κατά την ανάκτηση δεδομένων: {e}")