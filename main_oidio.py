import os
import requests
import datetime

# ... (ο κώδικας του calculate_oidio_risk παραμένει ο ίδιος)

try:
    # ... (ο κώδικας ανάκτησης API παραμένει ο ίδιος)
    
    with open("result_oidio.txt", "w", encoding="utf-8") as f:
        f.write(f"UPDATE: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        
        # Στιγμιαία Κατάσταση
        f.write("---SECTION_START---\n")
        f.write(f"ΣΤΙΓΜΙΑΙΑ ΚΑΤΑΣΤΑΣΗ\n")
        f.write(f"Κίνδυνος: {risk_now}\n")
        f.write(f"Θερμοκρασία: {temp}\n")
        f.write(f"Υγρασία: {hum}\n")
        f.write(f"Άνεμος: {wind}\n")
        f.write("---SECTION_END---\n")
        
        # Πρόβλεψη Σήμερα & Αύριο (με την ίδια δομή)
        # ... (αντίστοιχα write για σήμερα και αύριο)

except Exception as e:
    print(f"Σφάλμα: {e}")