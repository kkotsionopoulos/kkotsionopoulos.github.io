import os
import requests
import google.generativeai as genai

# Ρύθμιση API Keys
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]

def get_weather():
    # Προσθήκη Greece για να μην παίρνουμε την Τρίπολη της Λιβύης
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q=Tripoli,Greece"
    response = requests.get(url).json()
    
    if 'current' not in response:
        raise KeyError(f"Το κλειδί 'current' δεν βρέθηκε. Η απάντηση του API ήταν: {response}")
        
    temp = response['current']['temp_c']
    humidity = response['current']['humidity']
    return f"θερμοκρασία: {temp}°C, Υγρασία: {humidity}%"

def analyze_risk(weather_data):
    # Χρησιμοποιούμε gemini-pro που είναι πιο σταθερό για το παλιό SDK
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""Ανάλυσε τα δεδομένα: {weather_data}. 
    Υπάρχει κίνδυνος για περονόσπορο στην Τρίπολη; 
    Απάντησε ΜΟΝΟ με αυτή τη δομή, χωρίς άλλα σχόλια:
    ΑΠΟΤΕΛΕΣΜΑ: [ΚΙΝΔΥΝΟΣ ή ΑΣΦΑΛΕΣ]
    ΤΙΜΕΣ: [{weather_data}]
    ΑΙΤΙΟΛΟΓΙΑ: [Εξήγησε σύντομα γιατί πάρθηκε αυτή η απόφαση βάσει των τιμών]"""
    
    response = model.generate_content(prompt)
    return response.text

# Κύρια εκτέλεση
try:
    data = get_weather()
    result = analyze_risk(data)
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(result)
    print("Το αρχείο result.txt ενημερώθηκε με επιτυχία!")
except Exception as e:
    print(f"Σφάλμα κατά την εκτέλεση: {e}")
    exit(1)