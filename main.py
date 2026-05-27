import os
import requests
import datetime

# Ρύθμιση API
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Tripoli,Greece"
    response = requests.get(url).json()
    if 'current' not in response:
        return None, None
    return response['current']['temp_c'], response['current']['humidity']

def calculate_risk(temp, humidity):
    if humidity > 75 and 15 <= temp <= 25:
        return "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif humidity > 60:
        return "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else:
        return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"

# Κύρια εκτέλεση
temp, humidity = get_weather()

if temp is not None:
    risk = calculate_risk(temp, humidity)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"Τελευταία ενημέρωση: {now}\nΘερμοκρασία: {temp}°C\nΥγρασία: {humidity}%\nΚατάσταση: {risk}"
    
    # Γράψιμο στο αρχείο με ασφάλεια
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(content)
        f.flush()
        os.fsync(f.fileno())
    
    # Εκτύπωση στο log για να δούμε τι έγινε
    print("Περιεχόμενο που γράφτηκε:")
    print(content)
else:
    print("Αποτυχία λήψης δεδομένων.")