import requests
import os
import datetime  # Σωστό import για την ώρα

def calculate_scab_risk(temp, wetness_hours):
    """
    Υπολογισμός κινδύνου Φουζικλαδίου βάσει του πίνακα του Mills.
    """
    if wetness_hours >= 12 and 15 <= temp <= 25:
        return "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ (Πιθανή μόλυνση)"
    elif wetness_hours >= 6 and 15 <= temp <= 25:
        return "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ (Απαιτείται παρακολούθηση)"
    else:
        return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"

# Ρυθμίσεις API
api_key = os.environ.get("WEATHER_API_KEY")
city = "Tripoli"
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}"

try:
    response = requests.get(url).json()
    current = response['current']
    
    temp = current['temp_c']
    hum = current['humidity']
    wetness_hours = 12 if hum > 85 else 0 
    
    risk = calculate_scab_risk(temp, wetness_hours)
    
    # Εγγραφή στο result_scab.txt
    with open("result_scab.txt", "w", encoding="utf-8") as f:
        f.write(f"Τελευταία ενημέρωση: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"--- ΠΡΟΒΛΕΨΗ ΦΟΥΖΙΚΛΑΔΙΟΥ ---\n")
        f.write(f"Κίνδυνος: {risk}\n")
        f.write(f"Θερμοκρασία: {temp}°C\n")
        f.write(f"Υγρασία: {hum}%\n")
        
except Exception as e:
    print(f"Σφάλμα: {e}")