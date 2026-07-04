import os
import requests
import json
import time

# Τραβάει το κλειδί δυναμικά από τα GitHub Secrets
API_KEY = os.environ.get("GOOGLE_API_KEY")
QUERY = "ψητοπωλείο εστιατόριο Τρίπολη"

def fetch_restaurant_data():
    if not API_KEY:
        print("Σφάλμα: Δεν βρέθηκε το GOOGLE_API_KEY. Έλεγξε τα GitHub Secrets.")
        return

    search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={QUERY}&language=el&key={API_KEY}"
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        results = response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Σφάλμα API: {e}")
        return

    restaurants_data = []
    delivery_keywords = ["ντελίβερι", "delivery", "πακέτο", "διανομή", "wolt", "efood"]

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
            continue

        delivery_reviews = []
        for review in reviews:
            text = review.get("text", "")
            if any(keyword in text.lower() for keyword in delivery_keywords):
                delivery_reviews.append(text)

        restaurants_data.append({
            "name": name,
            "rating": rating,
            "review_count": user_ratings_total,
            "delivery_reviews": delivery_reviews,
            "delivery_platform": "",  
            "wolt_url": ""            
        })
        time.sleep(0.2)

    with open('restaurants.json', 'w', encoding='utf-8') as f:
        json.dump(restaurants_data, f, ensure_ascii=False, indent=4)
        
    print("Τα δεδομένα αντλήθηκαν επιτυχώς!")

if __name__ == "__main__":
    fetch_restaurant_data()