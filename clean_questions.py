import json

# Φόρτωση του αρχείου
with open("data/questions_oikonomia.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Διατήρηση μόνο των μοναδικών ερωτήσεων
unique_questions = []
seen = set()

for item in data:
    q_text = item["question"].strip()
    if q_text not in seen:
        seen.add(q_text)
        unique_questions.append(item)

# Αποθήκευση του καθαρού αρχείου
with open("data/questions_oikonomia.json", "w", encoding="utf-8") as f:
    json.dump(unique_questions, f, ensure_ascii=False, indent=2)

print(f"Ολοκληρώθηκε! Διατηρήθηκαν {len(unique_questions)} μοναδικές ερωτήσεις.")