import os
import requests
import google.generativeai as genai

def get_weather():
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        raise ValueError("Δεν βρέθηκε το WEATHER_API_KEY")
    
    # Προσθήκη ,Greece για να μην πηγαίνει στη Λιβύη
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q=Tripoli,Greece"
    response = requests.get(url)
    data = response.json()
    
    if 'current' not in data:
        raise KeyError(f"Αποτυχία λήψης καιρού: {data}")
    
    return data['current']

def analyze_risk(weather_data):
    # Ρύθμιση του Gemini
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"Ανάλυσε τον κίνδυνο για τους πεζοπόρους στον Μαινάλιο Δρυμό με βάση τα εξής δεδομένα: {weather_data}"
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    try:
        # Λήψη δεδομένων καιρού
        weather = get_weather()
        print("Επιτυχής λήψη καιρού για Τρίπολη, Ελλάδα.")
        
        # Ανάλυση με AI
        risk_report = analyze_risk(weather)
        print("\n--- Αναφορά Κινδύνου ---\n")
        print(risk_report)
        
        # Αποθήκευση αποτελέσματος σε αρχείο για το GitHub
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(risk_report)
            
    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση: {e}")
        exit(1)