import os
import requests
import datetime

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

def get_weather():
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Tripoli,Greece"
        response = requests.get(url, timeout=10).json()
        if 'current' in response:
            return response['current']['temp_c'], response['current']['humidity']
    except Exception as e:
        print(f"Σφάλμα σύνδεσης: {e}")
    return None, None

def calculate_risk(temp, humidity):
    if humidity > 75 and 15 <= temp <= 25:
        return "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif humidity > 60:
        return "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"

# Κύρια εκτέλεση
temp, humidity = get_weather()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if temp is not None:
    risk = calculate_risk(temp, humidity)
    content = f"Τελευταία ενημέρωση: {now}\nΘερμοκρασία: {temp}°C\nΥγρασία: {humidity}%\nΚατάσταση: {risk}"
else:
    content = f"Τελευταία ενημέρωση: {now}\nΤα δεδομένα δεν κατέστη δυνατό να ανακτηθούν."

# Εγγυημένο γράψιμο
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)
print("Το αρχείο result.txt ενημερώθηκε.")

# Στο τέλος του main.py, μετά το write
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)
print("--- ΤΕΛΟΣ ΕΚΤΕΛΕΣΗΣ: Το αρχείο γράφτηκε ---")