// demetrag/js/model.js

// Ενσωματωμένα πλήρη δεδομένα για την εκμετάλλευση FARM-00455 (14 Αγροτεμάχια)
export const STATIC_FARM = {
  farm_id: "FARM-00455",
  name: "Εκμετάλλευση Loiret",
  total_area_ha: 86.2,
  crops: ["Σιτάρι", "Κριθάρι", "Ελαιοκράμβη", "Αραβόσιτος", "Ηλίανθος"],
  stock: {
    "NPK 15-15-15": { quantity: 1200, unit: "kg" },
    "Ουρία 46-0-0": { quantity: 800, unit: "kg" },
    "Ζιζανιοκτόνο Cherokee": { quantity: 45, unit: "L" },
    "Μυκητοκτόνο Amistar": { quantity: 20, unit: "L" }
  },
  parcels: [
    { id: "P-517", name: "P-517", area_ha: 6.8, crop: "Αραβόσιτος", status: "Ώριμο για Συγκομιδή", color: "#d97706", ndvi: 0.68 },
    { id: "P-518", name: "P-518", area_ha: 5.2, crop: "Αραβόσιτος", status: "Ώριμο για Συγκομιδή", color: "#d97706", ndvi: 0.65 },
    { id: "P-101", name: "P-101", area_ha: 12.4, crop: "Σιτάρι", status: "Σπαρμένο", color: "#16a34a", ndvi: 0.42 },
    { id: "P-102", name: "P-102", area_ha: 10.1, crop: "Σιτάρι", status: "Προετοιμασία Εδάφους", color: "#ca8a04", ndvi: 0.22 },
    { id: "P-103", name: "P-103", area_ha: 8.0, crop: "Σιτάρι", status: "Απαιτείται Κατεργασία", color: "#ea580c", ndvi: 0.18 },
    { id: "P-201", name: "P-201", area_ha: 8.5, crop: "Κριθάρι", status: "Σπαρμένο", color: "#16a34a", ndvi: 0.45 },
    { id: "P-202", name: "P-202", area_ha: 4.2, crop: "Κριθάρι", status: "Προετοιμασία Εδάφους", color: "#ca8a04", ndvi: 0.25 },
    { id: "P-301", name: "P-301", area_ha: 7.2, crop: "Ελαιοκράμβη", status: "Βλαστικό Στάδιο", color: "#15803d", ndvi: 0.72 },
    { id: "P-302", name: "P-302", area_ha: 7.0, crop: "Ελαιοκράμβη", status: "Βλαστικό Στάδιο", color: "#15803d", ndvi: 0.70 },
    { id: "P-401", name: "P-401", area_ha: 5.5, crop: "Ηλίανθος", status: "Αγρανάπαυση", color: "#a16207", ndvi: 0.15 },
    { id: "P-402", name: "P-402", area_ha: 5.5, crop: "Ηλίανθος", status: "Αγρανάπαυση", color: "#a16207", ndvi: 0.14 },
    { id: "P-104", name: "P-104", area_ha: 3.0, crop: "Σιτάρι", status: "Σπαρμένο", color: "#16a34a", ndvi: 0.39 },
    { id: "P-105", name: "P-105", area_ha: 1.5, crop: "Σιτάρι", status: "Σπαρμένο", color: "#16a34a", ndvi: 0.41 },
    { id: "P-203", name: "P-203", area_ha: 1.3, crop: "Κριθάρι", status: "Προετοιμασία Εδάφους", color: "#ca8a04", ndvi: 0.20 }
  ]
};

// Ενσωματωμένη πρόγνωση καιρού (Open-Meteo)
export const STATIC_WEATHER = {
  forecast: [
    { day: "Σήμερα", temp_max: 19, temp_min: 9, rain_mm: 0.0, wind_kmh: 12, condition: "Ηλιοφάνεια", suitable_harvest: true, suitable_spray: true },
    { day: "Αύριο", temp_max: 18, temp_min: 10, rain_mm: 0.2, wind_kmh: 14, condition: "Αραιή Συννεφιά", suitable_harvest: true, suitable_spray: true },
    { day: "Κυριακή", temp_max: 14, temp_min: 7, rain_mm: 6.5, wind_kmh: 26, condition: "Βροχή", suitable_harvest: false, suitable_spray: false },
    { day: "Δευτέρα", temp_max: 13, temp_min: 6, rain_mm: 9.2, wind_kmh: 32, condition: "Ισχυρή Βροχή", suitable_harvest: false, suitable_spray: false },
    { day: "Τρίτη", temp_max: 15, temp_min: 8, rain_mm: 1.2, wind_kmh: 16, condition: "Συννεφιά", suitable_harvest: false, suitable_spray: true }
  ]
};

// Συνάρτηση άμεσης επιστροφής χωρίς εξάρτηση από server
export async function loadModel() {
  return {
    farm: STATIC_FARM,
    weather: STATIC_WEATHER
  };
}
