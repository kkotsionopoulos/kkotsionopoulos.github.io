import os
import requests
import datetime

# Ρύθμιση API KEY
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_weather():
    # Τρίπολη, Ελλάδα
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Tripoli,Greece"
    response = requests.get(url).json()
    
    if 'current' not in response:
        print(f"Σφάλμα API: {response}")
        return None, None
        
    temp = response['current']['temp_c']
    humidity = response['current']['humidity']
    return temp, humidity

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
    # Προσθήκη ώρας για να αλλάζει πάντα το αρχείο και να γίνεται push
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"Τελευταία ενημέρωση: {now}\nΘερμοκρασία: {temp}°C\nΥγρασία: {humidity}%\nΚατάσταση: {risk}"
    
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(content)
    print("Το αρχείο result.txt ενημερώθηκε με:")
    print(content)
else:
    print("Αποτυχία λήψης δεδομένων.")