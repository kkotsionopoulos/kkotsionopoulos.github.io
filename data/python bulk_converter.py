import json
import os
import re


def parse_questions_text(text, category="oikonomia"):
  questions_list = []

  # Καθαρισμός κειμένου από περιττές κενές γραμμές
  text = text.replace("\r\n", "\n")

  # Χωρίζουμε το κείμενο ανά ερώτηση με βάση τον αριθμό της (π.χ. "1.", "2." κλπ.)
  # Αναζητά μοτίβα τύπου: "1. Ερώτηση...", "2) Ερώτηση..."
  raw_questions = re.split(r'\n(?=\d+[\.\)]\s)', text)

  for raw in raw_questions:
    if not raw.strip():
      continue

    lines = [line.strip() for line in raw.strip().split("\n") if line.strip()]
    if not lines:
      continue

    # Η πρώτη γραμμή είναι η ερώτηση (αφαιρούμε τον αριθμό στην αρχή, π.χ. "1. ")
    q_line = lines[0]
    q_text = re.sub(r"^\d+[\.\)]\s*", "", q_line).strip()

    options = []
    correct_idx = 0  # Default 0 αν δεν βρεθεί

    # Εντοπισμός επιλογών (α., β., γ., δ. ή a., b., c., d.)
    option_pattern = re.compile(r"^([α-δa-d][\.\)])\s*(.*)", re.IGNORECASE)

    for line in lines[1:]:
      match = option_pattern.match(line)
      if match:
        opt_text = match.group(2).strip()
        options.append(opt_text)
        # Εδώ μπορείς να ορίσεις κάποιο σημάδι αν έχεις τις απαντήσεις,
        # αλλιώς τις βάζει προεπιλογή στην 1η (0) και τις διορθώνεις εύκολα στο JSON.
      else:
        # Αν η γραμμή είναι συνέχεια της προηγούμενης επιλογής ή ερώτησης
        if options:
          options[-1] += " " + line
        else:
          q_text += " " + line

    # Εξασφαλίζουμε ότι θα έχουμε πάντα 4 επιλογές
    while len(options) < 4:
      options.append("Κενή επιλογή")
    options = options[:4]

    q_obj = {
        "category": category,
        "question": q_text,
        "options": options,
        "correct": correct_idx,  # Θα το ελέγξεις γρήγορα στο JSON
    }
    questions_list.append(q_obj)

  return questions_list


def main():
  print("--- Μαζικός Μετατροπέας Κειμένου σε JSON για Quiz ΑΣΕΠ ---")
  category = input("Δώσε κατηγορία (π.χ. oikonomia): ").strip() or "oikonomia"
  filename = f"questions_{category}.json"

  print(
      "\nΕπικόλλησε παρακάτω όλες τις ερωτήσεις σου μαζί."
      "\nΌταν τελειώσεις, πάτησε Enter, άσε μια κενή γραμμή και γράψτε"
      " 'TELOS' σε μια νέα γραμμή και πάτησε Enter:\n"
  )

  lines = []
  while True:
    try:
      line = input()
      if line.strip() == "TELOS":
        break
      lines.append(line)
    except EOFError:
      break

  full_text = "\n".join(lines)

  # Μετατροπή
  parsed_data = parse_questions_text(full_text, category)

  # Αποθήκευση
  os.makedirs("data", exist_ok=True)
  filepath = os.path.join("data", filename)

  with open(filepath, "w", encoding="utf-8") as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=2)

  print(
      f"\n Επιτυχία! Μετατράπηκαν και αποθηκεύτηκαν {len(parsed_data)}"
      f" ερωτήσεις στο αρχείο '{filepath}'."
  )
  print(
      "Σημείωση: Έλεγξε γρήγορα το JSON αρχείο για τυχόν διορθώσεις στις"
      " σωστές απαντήσεις (correct)."
  )


if __name__ == "__main__":
  main()