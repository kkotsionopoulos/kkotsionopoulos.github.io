let farmData = null;
let weatherData = null;
let parsedDraft = null;
let recognition = null;

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const [farmRes, weatherRes] = await Promise.all([
      fetch('data/farm.json'),
      fetch('data/weather.json')
    ]);
    farmData = await farmRes.json();
    weatherData = await weatherRes.json();
    
    renderFields();
    renderStock();
    renderWeather();
    initSpeechRecognition();
  } catch (err) {
    console.error("Σφάλμα κατά τη φόρτωση δεδομένων:", err);
  }
});

function renderFields() {
  const container = document.getElementById('fields-container');
  if (!container) return;
  container.innerHTML = '';
  farmData.fields.forEach(field => {
    const card = document.createElement('div');
    card.className = "border border-slate-200 rounded-lg p-3 flex flex-col justify-between hover:shadow-md transition cursor-pointer bg-white";
    card.innerHTML = `
      <div>
        <div class="flex justify-between items-start">
          <span class="font-bold text-sm text-slate-800">${field.name}</span>
          <span class="text-[10px] px-1.5 py-0.5 rounded text-white" style="background-color: ${field.color}">${field.crop}</span>
        </div>
        <p class="text-xs text-slate-500 mt-1">${field.area_ha} ha (${(field.area_ha * 10).toFixed(0)} στρ.)</p>
      </div>
      <div class="mt-2 text-[11px] font-medium text-slate-600 border-t border-slate-100 pt-1">
        ${field.status}
      </div>
    `;
    container.appendChild(card);
  });
}

function renderStock() {
  const container = document.getElementById('stock-container');
  if (!container) return;
  container.innerHTML = '';
  for (const [prod, info] of Object.entries(farmData.stock)) {
    const item = document.createElement('div');
    item.className = "p-2.5 bg-slate-50 rounded border border-slate-200";
    item.innerHTML = `
      <div class="text-[11px] text-slate-500 truncate" title="${prod}">${prod}</div>
      <div class="text-sm font-bold text-slate-800 mt-0.5">${info.quantity} <span class="text-[10px] font-normal">${info.unit}</span></div>
    `;
    container.appendChild(item);
  }
}

function renderWeather() {
  const container = document.getElementById('weather-forecast');
  if (!container) return;
  container.innerHTML = '';
  weatherData.forecast.forEach(f => {
    const row = document.createElement('div');
    row.className = "flex items-center justify-between p-2 rounded border border-slate-100 text-xs";
    row.innerHTML = `
      <span class="font-medium w-20">${f.day}</span>
      <span class="text-slate-500">${f.temp_max}° / ${f.temp_min}°C</span>
      <span class="text-slate-500">${f.rain_mm} mm</span>
      <span class="px-2 py-0.5 rounded text-[10px] font-bold ${f.suitable_harvest ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}">
        ${f.suitable_harvest ? 'Κατάλληλο' : 'Ακατάλληλο'}
      </span>
    `;
    container.appendChild(row);
  });
}

function openModal() {
  document.getElementById('record-modal').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('record-modal').classList.add('hidden');
  document.getElementById('task-input').value = '';
  document.getElementById('parse-preview').classList.add('hidden');
  document.getElementById('save-btn').disabled = true;
  parsedDraft = null;
}

function initSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.lang = 'el-GR';
    recognition.continuous = false;
    
    recognition.onresult = (e) => {
      document.getElementById('task-input').value = e.results[0][0].transcript;
      document.getElementById('mic-label').innerText = "Έναρξη Ομιλίας";
      parseAndPreview();
    };
    recognition.onerror = () => {
      document.getElementById('mic-label').innerText = "Έναρξη Ομιλίας";
    };
  } else {
    const micBtn = document.getElementById('mic-btn');
    if (micBtn) micBtn.style.display = 'none';
  }
}

function toggleSpeech() {
  if (!recognition) return;
  document.getElementById('mic-label').innerText = "Ακρόαση...";
  recognition.start();
}

function parseAndPreview() {
  const text = document.getElementById('task-input').value.toLowerCase();
  if (!text.trim()) return;

  if (text.includes("όχι") || text.includes("μην") || text.includes("δεν") || text.includes("ακύρωσε")) {
    alert("Η εντολή απορρίφθηκε: Ανιχνεύθηκε άρνηση ή αρνητική οδηγία.");
    return;
  }

  let matchedField = farmData.fields.find(f => text.includes(f.name.toLowerCase()) || text.includes(f.id.toLowerCase()));
  if (!matchedField) {
    matchedField = farmData.fields[2]; // Fallback στο P-101
  }

  let matchedProduct = Object.keys(farmData.stock).find(p => text.includes(p.toLowerCase()));
  if (!matchedProduct) {
    matchedProduct = "NPK 15-15-15";
  }

  const numMatch = text.match(/(\d+([\.,]\d+)?)/);
  let rate = numMatch ? parseFloat(numMatch[1].replace(',', '.')) : 100;

  const isPerHa = text.includes("ανά εκτάριο") || text.includes("/ha") || text.includes("το εκτάριο") || !text.includes("συνολικά");
  const totalDeduction = isPerHa ? Math.round(rate * matchedField.area_ha) : rate;

  parsedDraft = {
    field: matchedField,
    product: matchedProduct,
    rate: rate,
    isPerHa: isPerHa,
    totalDeduction: totalDeduction,
    unit: farmData.stock[matchedProduct].unit
  };

  document.getElementById('parsed-field').innerText = `${parsedDraft.field.name} (${parsedDraft.field.crop}, ${parsedDraft.field.area_ha} ha)`;
  document.getElementById('parsed-product').innerText = parsedDraft.product;
  document.getElementById('parsed-rate').innerText = `${parsedDraft.rate} ${parsedDraft.unit}${isPerHa ? '/ha' : ' συνολικά'}`;
  document.getElementById('parsed-total').innerText = `${parsedDraft.totalDeduction} ${parsedDraft.unit}`;

  document.getElementById('parse-preview').classList.remove('hidden');
  document.getElementById('save-btn').disabled = false;
}

function commitWork() {
  if (!parsedDraft) return;

  farmData.stock[parsedDraft.product].quantity -= parsedDraft.totalDeduction;
  if (farmData.stock[parsedDraft.product].quantity < 0) {
    farmData.stock[parsedDraft.product].quantity = 0;
  }

  parsedDraft.field.status = "Εφαρμογή Ολοκληρώθηκε";
  parsedDraft.field.color = "#15803d";

  renderFields();
  renderStock();

  const log = document.getElementById('receipt-log');
  const receipt = document.createElement('div');
  receipt.className = "p-2.5 bg-emerald-50 border border-emerald-200 rounded text-slate-800 space-y-0.5 text-xs mb-2";
  receipt.innerHTML = `
    <div class="font-bold text-emerald-900 flex justify-between">
      <span>Απόδειξη Καταγραφής #${Math.floor(1000 + Math.random() * 9000)}</span>
      <span class="text-[10px] text-slate-500">${new Date().toLocaleTimeString()}</span>
    </div>
    <div>Αγρός: <strong>${parsedDraft.field.name}</strong> | Προϊόν: <strong>${parsedDraft.product}</strong></div>
    <div>Χρήση: -${parsedDraft.totalDeduction} ${parsedDraft.unit} (Υπόλοιπο αποθήκης: ${farmData.stock[parsedDraft.product].quantity} ${parsedDraft.unit})</div>
  `;
  
  if (log.children.length === 1 && log.children[0].innerText.includes("Δεν υπάρχουν")) {
    log.innerHTML = '';
  }
  log.prepend(receipt);

  closeModal();
}
