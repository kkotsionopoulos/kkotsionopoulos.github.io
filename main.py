import os
import requests
import google.generativeai as genai

# Ρύθμιση
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={os.environ['WEATHER_API_KEY']}&q=Tripoli,Greece"
    response = requests.get(url).json()
    temp = response['current']['temp_c']
    return f"Θερμοκρασία: {temp}°C"

def analyze():
    weather = get_weather()
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Ανάλυσε τον καιρό: {weather}. Υπάρχει κίνδυνος περονόσπορου; Πες μόνο ΝΑΙ ή ΟΧΙ και γιατί.")
    
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    analyze()