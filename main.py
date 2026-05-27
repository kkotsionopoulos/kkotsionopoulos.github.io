import os
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={os.environ['WEATHER_API_KEY']}&q=Tripoli,Greece"
    response = requests.get(url).json()
    if 'current' not in response:
        raise KeyError("Αδυναμία λήψης καιρού")
    return f"Θερμοκρασία: {response['current']['temp_c']}°C, Υγρασία: {response['current']['humidity']}%"

def analyze_risk(weather_data):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Ανάλυσε: {weather_data}. Υπάρχει κίνδυνος περονόσπορου; Απάντησε ΜΟΝΟ: ΑΠΟΤΕΛΕΣΜΑ, ΤΙΜΕΣ, ΑΙΤΙΟΛΟΓΙΑ."
    response = model.generate_content(prompt)
    return response.text

data = get_weather()
result = analyze_risk(data)
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(result)