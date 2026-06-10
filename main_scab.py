import os
import requests
import datetime

# Υπολογισμός κινδύνου βάσει Mills (απλοποιημένο μοντέλο)
def calculate_scab_risk(temp, wetness):
    if wetness > 18:
        return "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif 10 <= wetness <= 18:
        return "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else:
        return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"

api_key = os.environ.get("WEATHER_API_KEY")
# Αντικατάστησε με την πόλη σου ή τις συντεταγμένες
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q=Tripoli"

try:
    response = requests.get(url).json()
    curr = response['current']
    
    # Προσομοίωση δεδομένων διαβροχής (αν το API δεν δίνει άμεσα ώρες διαβροχής)
    # Εδώ μπορείς να βάλεις τη λογική σου αν έχεις αισθητήρα ή υπολογισμό
    temp = curr['temp_c']
    humidity = curr['humidity']
    
    # Υπολογισμός ρίσκου
    risk = calculate_scab_risk(temp, humidity)

    # Εγγραφή στο αρχείο (Σταθερή μορφή για το JS)
    with open("result_scab.txt", "w", encoding="utf-8") as f:
        f.write(f"Τελευταία ενημέρωση: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("--- ΠΡΟΒΛΕΨΗ ΦΟΥΖΙΚΛΑΔΙΟΥ ---\n")
        f.write(f"Κίνδυνος: {risk}\n")
        f.write(f"Θερμοκρασία: {temp}°C\n")
        f.write(f"Υγρασία: {humidity}%\n")
        
except Exception as e:
    print(f"Σφάλμα κατά την εκτέλεση: {e}")