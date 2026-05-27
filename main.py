import os
import requests
from google import genai # Δοκίμασε αυτό το import

# Ρύθμιση Client - Αυτή είναι η σωστή σύνταξη
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Tripoli,Greece"
    response = requests.get(url).json()
    if 'current' not in response:
        raise KeyError("Αδυναμία λήψης καιρού")
    return f"Θερμοκρασία: {response['current']['temp_c']}°C, Υγρασία: {response['current']['humidity']}%"

def analyze_risk(weather_data):
    prompt = f"Ανάλυσε τα δεδομένα: {weather_data}. Υπάρχει κίνδυνος για περονόσπορο; Απάντησε ΜΟΝΟ: ΑΠΟΤΕΛΕΣΜΑ, ΤΙΜΕΣ, ΑΙΤΙΟΛΟΓΙΑ."
    
    # Η σωστή κλήση για το μοντέλο
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    return response.text

# Εκτέλεση
data = get_weather()
result = analyze_risk(data)
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(result)