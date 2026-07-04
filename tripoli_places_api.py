import requests
import json
import time
import os

# Το script διαβάζει πλέον το κλειδί με ασφάλεια από τα Secrets του GitHub
API_KEY = os.environ.get("GOOGLE_API_KEY")
QUERY = "ψητοπωλείο εστιατόριο Τρίπολη"

def fetch_restaurant_data():
    # 1. Αναζήτηση καταστημάτων
    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={QUERY}&language=el&key={API_KEY}"
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        results = response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Σφάλμα κατά την επικοινωνία με το API: {e}")
        return

    restaurants_data = []
    # Λέξεις-κλειδιά για φιλτράρισμα κριτικών
    delivery_keywords = ["ντελίβερι", "delivery", "πακέτο", "διανομή", "αργησε", "γρήγορο", "wolt", "efood"]

    print(f"Βρέθηκαν {len(results)} καταστήματα. Ξεκινάει η ανάλυση κριτικών (μπορεί να πάρει λίγα δευτερόλεπτα)...")

    # 2. Άντληση κριτικών για κάθε κατάστημα
    for place in results:
        place_id = place.get("place_id")
        name = place.get("name")
        rating = place.get("rating", 0)
        user_ratings_total = place.get("user_ratings_total", 0)

        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,user_ratings_total,reviews&language=el&key={API_KEY}"
        
        try:
            details_response = requests.get(details_url)
            reviews = details_response.json().get("result", {}).get("reviews", [])
        except requests.exceptions.RequestException:
            print(f"Σφάλμα κατά τη λήψη λεπτομερειών για το κατάστημα: {name}")
            continue

        delivery_reviews = []
        
        # 3. Φιλτράρισμα βάσει λέξεων-κλειδιών
        for review in reviews:
            text = review.get("text", "")
            if any(keyword in text.lower() for keyword in delivery_keywords):
                delivery_reviews.append(text)

        # 4. Δομή των δεδομένων για το JSON
        restaurants_data.append({
            "name": name,
            "rating": rating,
            "review_count": user_ratings_total,
            "delivery_reviews": delivery_reviews,
            "delivery_platform": "",  # Προς χειροκίνητη συμπλήρωση
            "wolt_url": ""            # Προς χειροκίνητη συμπλήρωση
        })
        
        # Μικρή παύση για την αποφυγή block από το API της Google
        time.sleep(0.2)

    # 5. Αποθήκευση στο αρχείο restaurants.json
    with open('restaurants.json', 'w', encoding='utf-8') as f:
        json.dump(restaurants_data, f, ensure_ascii=False, indent=4)
        
    print("Το αρχείο restaurants.json δημιουργήθηκε με επιτυχία! Μπορείς πλέον να το επεξεργαστείς.")

if __name__ == "__main__":
    fetch_restaurant_data()