import requests
import json
import datetime

def get_beaufort(wind_kph):
    """Μετατροπές km/h σε κλίμακα Μποφόρ"""
    if wind_kph < 2: return 0
    elif wind_kph < 6: return 1
    elif wind_kph < 12: return 2
    elif wind_kph < 20: return 3
    elif wind_kph < 29: return 4
    elif wind_kph < 39: return 5
    elif wind_kph < 50: return 6
    elif wind_kph < 62: return 7
    elif wind_kph < 75: return 8
    else: return 9

def calculate_beach_risk(wind_kph, wind_dir, beach_orientation):
    beaufort = get_beaufort(wind_kph)
    
    # Υπολογισμός αν ο άνεμος είναι "κόντρα" (Onshore) στην παραλία
    # 0 μοίρες διαφορά σημαίνει ότι ο άνεμος έρχεται κάθετα από τη θάλασσα στην ακτή
    angle_diff = abs((wind_dir - beach_orientation + 180) % 360 - 180)
    is_onshore = angle_diff < 60  # Ο άνεμος "χτυπάει" την ακτή

    if beaufort >= 6 and is_onshore:
        status = "ΠΟΛΥ ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ (Έντονος Κυματισμός & Ρεύματα)"
        flag = "🔴 Κόκκινη Σημαία"
        color = "#e74c3c"  # Κόκκινο
    elif (beaufort == 5 and is_onshore) or (beaufort >= 6 and not is_onshore):
        status = "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ (Mεγάλα κύματα / Χρειάζεται Προσοχή)"
        flag = "🟡 Κίτρινη Σημαία"
        color = "#e67e22"  # Πορτοκαλί
    elif (beaufort == 4 and is_onshore) or (beaufort == 5 and not is_onshore):
        status = "ΜΕΤΡΙΟΣ ΚΥΜΑΤΙΣΜΟΣ (Ελαφρύς κυματισμός)"
        flag = "🟡 Κίτρινη Σημαία"
        color = "#f1c40f"  # Κίτρινο
    else:
        status = "ΗΡΕΜΗ ΘΑΛΑΣΣΑ (Ασφαλής Κολύμβηση)"
        flag = "🟢 Πράσινη Σημαία"
        color = "#27ae60"  # Πράσινο

    return {
        "beaufort": beaufort,
        "status": status,
        "flag": flag,
        "color": color,
        "is_onshore": "Κόντρα Άνεμος (Onshore)" if is_onshore else "Εύνοια (Offshore/Side)"
    }

# Λίστα με δημοφιλείς παραλίες, συντεταγμένες (ακριβώς στην ακτή) και τον προσανατολισμό τους (orientation)
# Orientation: 0=Βορράς, 90=Ανατολή, 180=Νότος, 270=Δύση
beaches = {
    # Παραλίες Αρκαδίας & Αργολίδου (Βόρειος Κυνουρία / Αργολικός Κόλπος)
    "Παράλιο Άστρος": {"lat": 37.4168, "lon": 22.7661, "orientation": 90},
    "Ξηροπήγαδο": {"lat": 37.4619, "lon": 22.7448, "orientation": 95},
    "Κυβέρι": {"lat": 37.5186, "lon": 22.7302, "orientation": 110},
    "Άγιος Ανδρέας (Αρκαδία)": {"lat": 37.34878926810164, "lon": 22.799061122487423, "orientation": 80},
    "Κρυονέρι (Αρκαδία)": {"lat": 37.3182, "lon": 22.8123, "orientation": 100},
    "Ζαρίτσι (Τυρός)": {"lat": 37.2854, "lon": 22.8451, "orientation": 105},
    "Πλάκα Λεωνιδίου": {"lat": 37.1483, "lon": 22.8932, "orientation": 90},

    # Υπόλοιπες Παραλίες Πελοποννήσου & Ελλάδας
    "Καλαμάτα - Ανατολική Παραλία": {"lat": 37.0231, "lon": 22.1251, "orientation": 180},
    "Βοϊδοκοιλιά (Μεσσηνία)": {"lat": 36.9632, "lon": 21.6611, "orientation": 270},
    "Στούπα (Μάνη)": {"lat": 36.8481, "lon": 22.2592, "orientation": 225},
    "Τολό (Ναύπλιο)": {"lat": 37.5204, "lon": 22.8601, "orientation": 135},
    "Καραθώνα (Ναύπλιο)": {"lat": 37.5451, "lon": 22.8182, "orientation": 200},
    "Ζαχάρω (Ηλεία)": {"lat": 37.4812, "lon": 21.6111, "orientation": 270},
    "Κουρούτα (Αμαλιάδα)": {"lat": 37.7712, "lon": 21.2911, "orientation": 270},
    "Καλογριά (Αχαΐα)": {"lat": 38.1611, "lon": 21.3651, "orientation": 270},
    "Ξυλόκαστρο (Κορινθία)": {"lat": 38.0791, "lon": 22.6311, "orientation": 25},
    "Βουλιαγμένη (Αττική)": {"lat": 37.8111, "lon": 23.7781, "orientation": 180},
    "Μπάτης (Παλαιό Φάληρο)": {"lat": 37.9221, "lon": 23.6911, "orientation": 210},
    "Επανωμή (Θεσσαλονίκη)": {"lat": 40.3811, "lon": 22.8911, "orientation": 200},
    "Φαλάσαρνα (Χανιά)": {"lat": 35.5111, "lon": 23.5781, "orientation": 270},
    "Ελαφονήσι (Χανιά)": {"lat": 35.2711, "lon": 23.5411, "orientation": 210},
    "Πρέβελη (Ρέθυμνο)": {"lat": 35.1511, "lon": 24.4711, "orientation": 180},
    "Super Paradise (Μύκονος)": {"lat": 37.4111, "lon": 25.3681, "orientation": 180}
}

sea_results = {
    "last_update": datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    "beaches": {}
}

for name, info in beaches.items():
    try:
        # Κλήση στο Open-Meteo Weather API για άνεμο και κύμα
        url = f"https://api.open-meteo.com/v1/forecast?latitude={info['lat']}&longitude={info['lon']}&current=wind_speed_10m,wind_direction_10m"
        res = requests.get(url, timeout=10).json()
        
        current = res['current']
        wind_kph = current['wind_speed_10m']
        wind_dir = current['wind_direction_10m']
        
        risk = calculate_beach_risk(wind_kph, wind_dir, info['orientation'])
        
        sea_results["beaches"][name] = {
            "lat": info['lat'],
            "lon": info['lon'],
            "wind_kph": round(wind_kph, 1),
            "wind_dir": wind_dir,
            "beaufort": risk["beaufort"],
            "status": risk["status"],
            "flag": risk["flag"],
            "color": risk["color"],
            "wind_type": risk["is_onshore"]
        }
    except Exception as e:
        print(f"Σφάλμα για την παραλία {name}: {e}")

try:
    with open("sea_data.json", "w", encoding="utf-8") as f:
        json.dump(sea_results, f, ensure_ascii=False, indent=4)
        print("Το αρχείο sea_data.json ενημερώθηκε επιτυχώς.")
except Exception as e:
    print(f"Σφάλμα εγγραφής: {e}")