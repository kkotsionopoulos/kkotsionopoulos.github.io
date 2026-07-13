import os
import requests
import json
import datetime

def calculate_fire_risk(temp, humidity, wind_kph):
    # Βασικός αλγόριθμος υπολογισμού κινδύνου (0-100%)
    # Ο κίνδυνος αυξάνεται με τη θερμοκρασία και τον άνεμο, και μειώνεται με την υγρασία
    risk = (temp * 1.5) + (wind_kph * 1.2) - (humidity * 0.5)
    
    # Κανονικοποίηση μεταξύ 0 και 100
    risk = max(0, min(100, risk))
    
    if risk >= 75:
        level = "ΠΟΛΥ ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
        color = "#e74c3c"  # Κόκκινο
    elif risk >= 50:
        level = "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
        color = "#e67e22"  # Πορτοκαλί
    elif risk >= 30:
        level = "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
        color = "#f1c40f"  # Κίτρινο
    else:
        level = "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"
        color = "#27ae60"  # Πράσινο
        
    return {"risk_percentage": round(risk, 1), "level": level, "color": color}

api_key = os.environ.get("WEATHER_API_KEY")

# Λίστα με ενδεικτικές πόλεις/έδρες περιφερειών (μπορείς να προσθέσεις όποιες θέλεις)
# Λίστα με τις κύριες πόλεις της Ελλάδας (ανά νομό) και επιλεγμένα χωριά
locations = {
    # Πελοπόννησος & Χωριά
    "Tripoli": "Τρίπολη",
    "Sparti": "Σπάρτη",
    "Kalamata": "Καλαμάτα",
    "Korinthos": "Κόρινθος",
    "Nafplio": "Ναύπλιο",
    "Pyrgos": "Πύργος",
    "Patra": "Πάτρα",
    "Vytina": "Βυτίνα",
    "Dimitsana": "Δημητσάνα",
    "Stemnitsa": "Στεμνίτσα",
    "Lagadia": "Λαγκάδια",
    
    # Αττική & Στερεά Ελλάδα
    "Athens": "Αθήνα",
    "Lamia": "Λαμία",
    "Chalkida": "Χαλκίδα",
    "Livadeia": "Λιβαδειά",
    "Karpenisi": "Καρπενήσι",
    "Amfissa": "Άμφισσα",
    "Mesolongi": "Μεσολόγγι",

    # Θεσσαλία
    "Larissa": "Λάρισα",
    "Volos": "Βόλος",
    "Trikala": "Τρίκαλα",
    "Karditsa": "Καρδίτσα",

    # Ήπειρος
    "Ioannina": "Ιωάννινα",
    "Arta": "Άρτα",
    "Preveza": "Πρέβεζα",
    "Igoumenitsa": "Ηγουμενίτσα",

    # Μακεδονία & Θράκη
    "Thessaloniki": "Θεσσαλονίκη",
    "Serres": "Σέρρες",
    "Kavala": "Καβάλα",
    "Katerini": "Κατερίνη",
    "Veria": "Βέροια",
    "Kozani": "Κοζάνη",
    "Kastoria": "Καστοριά",
    "Florina": "Φλώρινα",
    "Alexandroupoli": "Αλεξανδρούπολη",
    "Komotini": "Κομοτηνή",
    "Xanthi": "Ξάνθη",

    # Νησιά & Κρήτη
    "Kerkyra": "Κέρκυρα",
    "Zakynthos": "Ζάκυνθος",
    "Mytilini": "Μυτιλήνη",
    "Chios": "Χίος",
    "Ermoupoli": "Σύρος",
    "Rodos": "Ρόδος",
    "Heraklion": "Ηράκλειο",
    "Chania": "Χανιά",
    "Rethymno": "Ρέθυμνο"
}

fire_results = {
    "last_update": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    "regions": {}
}

for city, region_name in locations.items():
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url, timeout=10).json()
        
        curr = response['current']
        temp = curr['temp_c']
        humidity = curr['humidity']
        wind = curr['wind_kph']
        
        risk_data = calculate_fire_risk(temp, humidity, wind)
        
        fire_results["regions"][region_name] = {
            "city": city,
            "temp": temp,
            "humidity": humidity,
            "wind": wind,
            "risk": risk_data["risk_percentage"],
            "level": risk_data["level"],
            "color": risk_data["color"]
        }
    except Exception as city_error:
        print(f"Αποτυχία λήψης δεδομένων για την περιοχή {region_name} ({city}): {city_error}")

# Αποθήκευση στο αρχείο, εφόσον μαζευτούν τα δεδομένα
try:
    with open("fire_data.json", "w", encoding="utf-8") as f:
        json.dump(fire_results, f, ensure_ascii=False, indent=4)
        print("Το αρχείο fire_data.json ενημερώθηκε επιτυχώς.")
except Exception as e:
    print(f"Σφάλμα κατά την εγγραφή του αρχείου: {e}")
        
    # Αποθήκευση σε JSON αρχείο
    with open("fire_data.json", "w", encoding="utf-8") as f:
        json.dump(fire_results, f, ensure_ascii=False, indent=4)
        print("Το αρχείο fire_data.json ενημερώθηκε επιτυχώς.")

except Exception as e:
    print(f"Σφάλμα κατά την εκτέλεση: {e}")