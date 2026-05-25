import requests
import google.generativeai as genai
import os

# Λήψη κλειδιών από τα GitHub Secrets
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def get_weather():
    # Δεδομένα για Τρίπολη
    url = "https://api.open-meteo.com/v1/forecast?latitude=37.51&longitude=22.37&hourly=temperature_2m,relative_humidity_2m,precipitation&forecast_days=1"
    return requests.get(url).json()

def analyze_risk(weather_data):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Ανάλυσε τα εξής καιρικά δεδομένα: {weather_data}. Υπάρχει κίνδυνος για περονόσπορο; Απάντησε ΜΟΝΟ με 'ΚΙΝΔΥΝΟΣ' ή 'ΑΣΦΑΛΕΣ' και μια σύντομη αιτιολόγηση."
    response = model.generate_content(prompt)
    return response.text

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

# Εκτέλεση
data = get_weather()
report = analyze_risk(data)

# Αποθήκευση στο αρχείο για την ιστοσελίδα
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(report)

# Αποστολή στο Telegram
send_telegram_alert(f"📋 Καθημερινή ενημέρωση:\n{report}")