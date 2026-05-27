import os
import requests

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={os.environ['WEATHER_API_KEY']}&q=Tripoli,Greece"
    response = requests.get(url).json()
    temp = response['current']['temp_c']
    humidity = response['current']['humidity']
    return temp, humidity

def calculate_risk(temp, humidity):
    # Απλοϊκός κανόνας για περονόσπορο:
    # Υψηλή υγρασία (>75%) και μέτρια θερμοκρασία (15-25°C)
    if humidity > 75 and 15 <= temp <= 25:
        return "ΥΨΗΛΟΣ ΚΙΝΔΥΝΟΣ"
    elif humidity > 60:
        return "ΜΕΤΡΙΟΣ ΚΙΝΔΥΝΟΣ"
    else:
        return "ΧΑΜΗΛΟΣ ΚΙΝΔΥΝΟΣ"

temp, humidity = get_weather()
risk = calculate_risk(temp, humidity)

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(f"Θερμοκρασία: {temp}°C, Υγρασία: {humidity}%\nΚίνδυνος Περονόσπορου: {risk}")