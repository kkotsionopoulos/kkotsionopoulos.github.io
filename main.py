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
        return None, None
    return None, None

def calculate_risk(temp, humidity):
    reasoning = f"Ανάλυση δεδομένων: Θερμοκρασία {temp}°C, Υγρασία {humidity}%."
    
    if humidity > 75 and 15 <= temp <= 25:
        risk = "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
        explanation = "Οι συνθήκες είναι ιδανικές για την ανάπτυξη του μύκητα (υψηλή υγρασία και κατάλληλο θερμικό εύρος)."
    elif humidity > 60:
        risk = "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
        explanation = "Η υγρασία είναι αυξημένη, απαιτείται παρακολούθηση καθώς πλησιάζουμε το όριο κινδύνου."
    else:
        risk = "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"
        explanation = "Οι τρέχουσες συνθήκες δεν ευνοούν την ανάπτυξη παθογόνων."
        
    return risk, f"{reasoning}\nΕπεξήγηση: {explanation}"

# Κύρια εκτέλεση
temp, humidity = get_weather()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if temp is not None:
    risk, explanation = calculate_risk(temp, humidity)
    content = f"Τελευταία ενημέρωση: {now}\nΘερμοκρασία: {temp}°C\nΥγρασία: {humidity}%\nΚατάσταση: {risk}\n\n{explanation}"
else:
    content = f"Τελευταία ενημέρωση: {now}\nΤα δεδομένα δεν κατέστη δυνατό να ανακτηθούν."

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(content)
print("--- ΤΕΛΟΣ ΕΚΤΕΛΕΣΗΣ: Το αρχείο result.txt ενημερώθηκε ---")