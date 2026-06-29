// Navigation Logic
document.querySelectorAll('.nav-item').forEach(button => {
    button.addEventListener('click', () => {
        // Update active class on buttons
        document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
        button.classList.add('active');

        // Show corresponding view
        const viewId = button.getAttribute('data-view');
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.getElementById(viewId).classList.add('active');
        
        if (viewId === 'anagrafe') loadSchools();
    });
});

// Chart.js Setup
const ctx = document.getElementById('liveChart').getContext('2d');
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = 'Inter';

const liveChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                grid: { color: 'rgba(255, 255, 255, 0.1)' }
            },
            x: {
                grid: { display: false }
            }
        },
        plugins: {
            legend: { 
                display: true,
                position: 'top',
                labels: {
                    color: '#94a3b8',
                    usePointStyle: true,
                    boxWidth: 10,
                    font: {
                        family: 'Inter',
                        size: 11
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `${context.dataset.label} | Consumo: ${context.parsed.y} L/min`;
                    }
                }
            }
        }
    }
});

// Data Fetching
let anomalyCount = 0;
let currentPage = 1;
const TOTAL_PAGES = 48;

function renderPagination() {
    const container = document.getElementById('pagination-container');
    if (!container) return;
    container.innerHTML = '';

    const prevBtn = document.createElement('button');
    prevBtn.className = 'btn';
    prevBtn.style = 'padding: 0.2rem 0.5rem; background: var(--bg-dark); color: var(--text-primary); border: 1px solid var(--border-color); cursor: pointer; border-radius: 4px;';
    prevBtn.innerText = '< Prec';
    prevBtn.disabled = currentPage === 1;
    prevBtn.onclick = () => { if (currentPage > 1) changePage(currentPage - 1); };
    container.appendChild(prevBtn);

    const maxVisible = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
    let endPage = Math.min(TOTAL_PAGES, startPage + maxVisible - 1);
    if (endPage - startPage + 1 < maxVisible) startPage = Math.max(1, endPage - maxVisible + 1);

    if (startPage > 1) {
        const btn = document.createElement('button');
        btn.className = 'btn';
        btn.style = 'padding: 0.2rem 0.5rem; background: var(--bg-dark); color: var(--text-primary); border: 1px solid var(--border-color); cursor: pointer; border-radius: 4px;';
        btn.innerText = '1';
        btn.onclick = () => changePage(1);
        container.appendChild(btn);
        if (startPage > 2) {
            const dots = document.createElement('span');
            dots.innerText = '...';
            dots.style = 'color: var(--text-secondary); padding: 0.2rem;';
            container.appendChild(dots);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const btn = document.createElement('button');
        btn.className = 'btn';
        let style = 'padding: 0.2rem 0.5rem; background: var(--bg-dark); color: var(--text-primary); border: 1px solid var(--border-color); cursor: pointer; border-radius: 4px;';
        if (i === currentPage) style = 'padding: 0.2rem 0.5rem; background: var(--accent); color: white; border: 1px solid var(--accent); cursor: default; border-radius: 4px;';
        btn.style = style;
        btn.innerText = i;
        if (i !== currentPage) btn.onclick = () => changePage(i);
        container.appendChild(btn);
    }

    if (endPage < TOTAL_PAGES) {
        if (endPage < TOTAL_PAGES - 1) {
            const dots = document.createElement('span');
            dots.innerText = '...';
            dots.style = 'color: var(--text-secondary); padding: 0.2rem;';
            container.appendChild(dots);
        }
        const btn = document.createElement('button');
        btn.className = 'btn';
        btn.style = 'padding: 0.2rem 0.5rem; background: var(--bg-dark); color: var(--text-primary); border: 1px solid var(--border-color); cursor: pointer; border-radius: 4px;';
        btn.innerText = TOTAL_PAGES;
        btn.onclick = () => changePage(TOTAL_PAGES);
        container.appendChild(btn);
    }

    const nextBtn = document.createElement('button');
    nextBtn.className = 'btn';
    nextBtn.style = 'padding: 0.2rem 0.5rem; background: var(--bg-dark); color: var(--text-primary); border: 1px solid var(--border-color); cursor: pointer; border-radius: 4px;';
    nextBtn.innerText = 'Succ >';
    nextBtn.disabled = currentPage === TOTAL_PAGES;
    nextBtn.onclick = () => { if (currentPage < TOTAL_PAGES) changePage(currentPage + 1); };
    container.appendChild(nextBtn);
}

function changePage(page) {
    currentPage = page;
    const slider = document.getElementById('timeline-slider');
    if (slider) {
        slider.value = page - 1;
        const label = document.getElementById('timeline-label');
        if (slider.value == 0) label.innerText = "Tempo Reale (Ultima mezz'ora)";
        else {
            const hours = (slider.value / 2).toFixed(1).replace('.0', '');
            label.innerText = `Dati Storici: ${hours} ore fa`;
        }
    }
    renderPagination();
    fetchLetture();
}

async function fetchLetture() {
    try {
        const schoolSelector = document.getElementById('dashboard-school-selector');
        const scuolaId = schoolSelector ? schoolSelector.value : '';
        const offset = currentPage - 1;
        
        let url = `/api/letture?limit=1000&hours_offset=${offset / 2.0}`;
        if (scuolaId) {
            url += `&scuola_id=${scuolaId}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        const latestReadings = {};
        data.forEach(d => {
            const key = `${d.scuola_nome}|${d.sensore_nome}`;
            if (!latestReadings[key]) {
                latestReadings[key] = d;
            }
        });

        liveChart.data.labels = ['Snapshot Consumi (L/min)'];
        liveChart.data.datasets = [];
        
        const colorPalette = [
            '#FF3333', '#33FF33', '#3333FF', '#FFFF33', '#FF33FF', 
            '#33FFFF', '#FF9933', '#9933FF', '#A0522D', '#FF1493'
        ];

        let colorIndex = 0;
        const schoolColorMap = {};

        Object.values(latestReadings).forEach(d => {
            if (!scuolaId && !d.sensore_is_main) return;
            
            if (!schoolColorMap[d.scuola_nome]) {
                schoolColorMap[d.scuola_nome] = colorPalette[colorIndex % colorPalette.length];
                colorIndex++;
            }
            
            let datasetLabel = scuolaId ? d.sensore_nome : d.scuola_nome;
            let bgColor = d.is_anomalia ? '#ef4444' : schoolColorMap[d.scuola_nome];
            
            liveChart.data.datasets.push({
                label: datasetLabel,
                data: [d.valore_litri],
                backgroundColor: bgColor + '99',
                borderColor: bgColor,
                borderWidth: 2,
                pointStyle: d.sensore_is_main ? 'rectRot' : 'circle'
            });
        });
        
        liveChart.update();

        // Update Table
        const tbody = document.getElementById('readings-body');
        tbody.innerHTML = '';
        anomalyCount = 0;

        const seenSchools = new Set();

        data.forEach(d => {
            // Filtro anche la tabella per mostrare solo i contatori principali nella vista generale
            if (!scuolaId && !d.sensore_is_main) return;

            // Assicuriamoci di mostrare 1 solo scarico per scuola/sensore
            const key = scuolaId ? `${d.scuola_nome}|${d.sensore_nome}` : d.scuola_nome;
            if (seenSchools.has(key)) return;
            seenSchools.add(key);

            if (d.is_anomalia) anomalyCount++;
            
            const tr = document.createElement('tr');
            const statusBadge = d.is_anomalia ? 
                '<span class="badge anomalia">Anomalia</span>' : 
                '<span class="badge normal">Normale</span>';
            
            const isPressione = d.sensore_nome && d.sensore_nome.includes('Pressione');
            const isTorbidita = d.sensore_nome && d.sensore_nome.includes('Torbidità');
            const isConducibilita = d.sensore_nome && d.sensore_nome.includes('Conducibilità');
            
            let unita = 'L/min';
            if (isPressione) unita = 'bar';
            else if (isTorbidita) unita = 'NTU';
            else if (isConducibilita) unita = 'µS/cm';
                
            tr.innerHTML = `
                <td>${new Date(d.timestamp).toLocaleTimeString()}</td>
                <td><strong>${d.scuola_nome}</strong><br><small style="color: var(--text-secondary)">${d.sensore_nome}</small></td>
                <td><strong>${d.valore_litri.toFixed(2)} ${unita}</strong></td>
                <td>${statusBadge}</td>
            `;
            tbody.appendChild(tr);
        });

        document.getElementById('anomaly-count').innerText = anomalyCount;
        
    } catch (e) {
        console.error("Error fetching data", e);
    }
}

async function fetchAggregati() {
    try {
        const schoolSelector = document.getElementById('dashboard-school-selector');
        const scuolaId = schoolSelector ? schoolSelector.value : '';
        let url = '/api/aggregati_consumi';
        if (scuolaId) {
            url += `?scuola_id=${scuolaId}`;
        }
        const response = await fetch(url);
        const data = await response.json();
        const elOrario = document.getElementById('valore-orario');
        const elGiornaliero = document.getElementById('valore-giornaliero');
        const elSettimanale = document.getElementById('valore-settimanale');
        const elMensile = document.getElementById('valore-mensile');
        if (elOrario) elOrario.innerText = `${data.consumo_orario.toFixed(0)} L`;
        if (elGiornaliero) elGiornaliero.innerText = `${data.consumo_giornaliero.toFixed(0)} L`;
        if (elSettimanale) elSettimanale.innerText = `${data.consumo_settimanale.toFixed(0)} L`;
        if (elMensile) elMensile.innerText = `${data.consumo_mensile.toFixed(0)} L`;
    } catch(e) {
        console.error("Errore recupero aggregati", e);
    }
}

async function fetchSensori(scuolaId) {
    const section = document.getElementById('school-sensors-section');
    const grid = document.getElementById('sensors-grid');
    if (!scuolaId) {
        if (section) section.style.display = 'none';
        return;
    }
    
    try {
        const response = await fetch(`/api/scuole/${scuolaId}/stato_sensori`);
        const sensori = await response.json();
        
        if (section) section.style.display = 'block';
        if (grid) {
            grid.innerHTML = '';
            sensori.forEach(s => {
                const isPressione = s.tipo === 'Pressione';
                const isTorbidita = s.tipo === 'Torbidità';
                const isConducibilita = s.tipo === 'Conducibilità';
                const isControlSensor = isPressione || isTorbidita || isConducibilita;

                const card = document.createElement('div');
                card.className = `card glass-panel ${s.is_anomalia ? 'alert-card' : ''} ${isControlSensor ? 'control-sensor-card' : ''}`;
                
                if(s.is_anomalia) {
                    card.style.border = '2px solid #ef4444';
                    card.style.animation = 'pulse 2s infinite';
                }
                
                let unit = 'L';
                let icon = '💧';
                if (isPressione) { unit = 'bar'; icon = '⏱️'; }
                else if (isTorbidita) { unit = 'NTU'; icon = '🧪'; }
                else if (isConducibilita) { unit = 'µS/cm'; icon = '⚡'; }

                let subtitle = "valore rilevato dall'ultima rilevazione";
                if (isPressione) subtitle = "Valore minimo: 1.5 bar | Massimo: 3.0 bar";
                else if (isTorbidita) subtitle = "Valore massimo consentito: 1.0 NTU";
                else if (isConducibilita) subtitle = "Valore massimo consentito: 2500 µS/cm";

                let alarmText = '';
                if (s.is_anomalia) {
                    if (isPressione) alarmText = '<div style="color: #ef4444; font-weight: bold; margin-top: 5px;">ERRORE: PRESSIONE FUORI DAI LIMITI!</div>';
                    else if (isTorbidita) alarmText = '<div style="color: #ef4444; font-weight: bold; margin-top: 5px;">ERRORE: TORBIDITÀ FUORI DAI LIMITI!</div>';
                    else if (isConducibilita) alarmText = '<div style="color: #ef4444; font-weight: bold; margin-top: 5px;">ERRORE: CONDUCIBILITÀ FUORI DAI LIMITI!</div>';
                }

                card.innerHTML = `
                    <h3>${icon} ${s.nome} <span style="font-size: 0.8em; opacity: 0.7;">(${s.tipo})</span></h3>
                    <div class="value">${s.valore_attuale.toFixed(2)} <span style="font-size: 0.5em; opacity: 0.8;">${unit}</span></div>
                    <div style="font-size: 0.75rem; margin-top: 8px; text-align: center; opacity: 0.9;">${subtitle}</div>
                    ${alarmText}
                `;
                grid.appendChild(card);
            });
        }
    } catch(e) {
        console.error("Errore fetch sensori:", e);
    }
}

let lastAlarmCount = 0;

async function checkAllarmi() {
    try {
        const response = await fetch('/api/allarmi?limit=50');
        const allarmi = await response.json();
        
        // Populate table if we are on the alarms view
        const tbody = document.getElementById('alarms-table-body');
        if (tbody) {
            tbody.innerHTML = '';
            allarmi.forEach(a => {
                const isPressione = a.sensore_nome && a.sensore_nome.includes('Pressione');
                const isTorbidita = a.sensore_nome && a.sensore_nome.includes('Torbidità');
                const isConducibilita = a.sensore_nome && a.sensore_nome.includes('Conducibilità');
                
                let unita = 'L/min';
                let tipoSensore = 'Consumo';
                if (isPressione) { unita = 'bar'; tipoSensore = 'Pressione'; }
                else if (isTorbidita) { unita = 'NTU'; tipoSensore = 'Torbidità'; }
                else if (isConducibilita) { unita = 'µS/cm'; tipoSensore = 'Conducibilità'; }

                const isPerdita = a.is_main && tipoSensore === 'Consumo';
                const causaMsg = isPerdita ? 
                    `<span style="color:var(--danger)">⚠️ Perdita occulta rilevata</span>` : 
                    `<span style="color:#f59e0b">Anomalia ${tipoSensore} (${a.sensore_nome})</span>`;

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${new Date(a.timestamp).toLocaleString()}</td>
                    <td><strong>${a.scuola_nome}</strong><br><small>${a.sensore_nome}</small></td>
                    <td style="color: var(--danger); font-weight: bold;">${a.valore_litri.toFixed(2)} ${unita}</td>
                    <td>${causaMsg}</td>
                    <td><span class="badge" style="background: rgba(16,185,129,0.2); color: #10b981; border-color: #10b981;">Inviata a vitogagliano@gmail.com</span></td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Blinking logic
        const btnAlarm = document.getElementById('nav-btn-allarmi');
        if (allarmi.length > lastAlarmCount) {
            // Nuovi allarmi rilevati!
            if (btnAlarm && !document.getElementById('allarmi').classList.contains('active')) {
                btnAlarm.classList.add('active-alarm');
            }
        }
        
        lastAlarmCount = allarmi.length;
        
    } catch(e) {
        console.error("Errore recupero allarmi", e);
    }
}

// Quando l'utente clicca sul pulsante allarmi, spegne il lampeggiamento
document.getElementById('nav-btn-allarmi').addEventListener('click', () => {
    document.getElementById('nav-btn-allarmi').classList.remove('active-alarm');
    checkAllarmi(); // Ricarica subito la tabella
});

// Esportazione Excel (CSV)
document.getElementById('btn-export-alarms').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/allarmi?limit=10000');
        const allarmi = await response.json();
        
        if (allarmi.length === 0) {
            alert("Nessun allarme da esportare.");
            return;
        }

        // Header CSV (usiamo punto e virgola come separatore per compatibilità con Excel in italiano)
        let csvContent = "Data;Ora;Scuola;Litri Consumati;Punteggio Anomalia;Stato Email\n";
        
        allarmi.forEach(a => {
            const dt = new Date(a.timestamp);
            const dataStr = dt.toLocaleDateString();
            const oraStr = dt.toLocaleTimeString();
            const litri = a.valore_litri.toFixed(2).replace('.', ','); // virgola per decimali in ITA
            const score = a.anomaly_score.toFixed(3).replace('.', ',');
            const stato = "Inviata a vitogagliano@gmail.com";
            
            // Gestione dei nomi con virgole/puntoevirgola
            const scuola = `"${a.scuola_nome}"`;
            
            csvContent += `${dataStr};${oraStr};${scuola};${litri};${score};${stato}\n`;
        });

        // Creazione file e download
        const blob = new Blob(["\uFEFF" + csvContent], { type: 'text/csv;charset=utf-8;' }); // \uFEFF for BOM UTF-8 (Excel compatibilità)
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.setAttribute("href", url);
        link.setAttribute("download", `Storico_Allarmi_AcquaSmart_${new Date().toISOString().split('T')[0]}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

    } catch (e) {
        console.error("Errore esportazione:", e);
        alert("Errore durante l'esportazione.");
    }
});

// Polling for live dashboard and alarms
setInterval(() => {
    const isLive = currentPage === 1;
    
    if(document.getElementById('dashboard').classList.contains('active') && isLive) {
        fetchLetture();
        fetchAggregati();
        const schoolSelector = document.getElementById('dashboard-school-selector');
        const scuolaId = schoolSelector ? schoolSelector.value : '';
        if(scuolaId) fetchSensori(scuolaId);
        else {
            const section = document.getElementById('school-sensors-section');
            if (section) section.style.display = 'none';
        }
    }
    checkAllarmi(); // Check alarms continuously in background
}, 3000);

document.getElementById('timeline-slider').addEventListener('change', (e) => {
    const offset = parseInt(e.target.value);
    currentPage = offset + 1;
    const label = document.getElementById('timeline-label');
    if (offset === 0) {
        label.innerText = "Tempo Reale (Ultima mezz'ora)";
    } else {
        const hours = (offset / 2).toFixed(1).replace('.0', '');
        label.innerText = `Dati Storici: ${hours} ore fa`;
    }
    renderPagination();
    fetchLetture(); // Ricarica subito i dati
});

// Init fetch
renderPagination();
fetchLetture();
fetchAggregati();
checkAllarmi();

// Anagrafe Logic
async function loadSchools() {
    try {
        const response = await fetch('/api/scuole');
        const scuole = await response.json();
        const tbody = document.getElementById('schools-body');
        tbody.innerHTML = '';
        
        scuole.forEach(s => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${s.id}</td>
                <td>${s.nome}</td>
                <td>${s.indirizzo}</td>
                <td>${s.codice_meccanografico || '-'}</td>
                <td>${s.numero_studenti}</td>
                <td>
                    <button class="btn" style="padding: 0.2rem 0.5rem; background: transparent; border: 1px solid var(--accent); color: var(--accent); margin-right: 5px;" onclick="addSensor(${s.id}, '${s.nome.replace(/'/g, "\\'")}')">+ Sensore</button>
                    <button class="btn" style="padding: 0.2rem 0.5rem; background: transparent; border: 1px solid var(--danger); color: var(--danger)" onclick="deleteSchool(${s.id})">Elimina</button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        // Update dashboard selector
        const dashboardSelector = document.getElementById('dashboard-school-selector');
        if(dashboardSelector) {
            const currentValue = dashboardSelector.value;
            dashboardSelector.innerHTML = '<option value="">Tutte le scuole</option>';
            scuole.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s.id;
                opt.textContent = s.nome;
                dashboardSelector.appendChild(opt);
            });
            dashboardSelector.value = currentValue;
        }

        // Update manual entry selector
        const manualSelector = document.getElementById('manual-scuola-select');
        if(manualSelector) {
            const currentManualValue = manualSelector.value;
            manualSelector.innerHTML = '<option value="">-- Seleziona o digita per cercare --</option>';
            scuole.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s.id;
                opt.textContent = `${s.nome} ${s.codice_meccanografico ? '('+s.codice_meccanografico+')' : ''}`;
                manualSelector.appendChild(opt);
            });
            manualSelector.value = currentManualValue;
        }

    } catch (e) {
        console.error(e);
    }
}

// Initial load for both dashboard and anagrafe
loadSchools();

document.getElementById('dashboard-school-selector').addEventListener('change', (e) => {
    const selectedOption = e.target.options[e.target.selectedIndex];
    const displayElement = document.getElementById('selected-school-display');
    const scuolaId = e.target.value;
    if (displayElement) {
        displayElement.innerHTML = `Stai visualizzando i dati di: <strong>${selectedOption.text}</strong>`;
    }
    fetchLetture();
    fetchAggregati();
    fetchSensori(scuolaId);
});

document.getElementById('btn-add-school').addEventListener('click', async () => {
    const nome = prompt("Nome della scuola:");
    if(!nome) return;
    const indirizzo = prompt("Indirizzo:");
    const codMecc = prompt("Codice Meccanografico:");
    const studenti = parseInt(prompt("Numero Studenti:"));
    
    if(nome && indirizzo && studenti) {
        await fetch('/api/scuole', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({nome, indirizzo, numero_studenti: studenti, codice_meccanografico: codMecc || ""})
        });
        loadSchools();
    }
});

async function editSchool(id, currentNome, currentIndirizzo, currentStudenti, currentCodMecc) {
    const nome = prompt("Nome della scuola:", currentNome);
    if(!nome) return;
    const indirizzo = prompt("Indirizzo:", currentIndirizzo);
    const codMecc = prompt("Codice Meccanografico:", currentCodMecc);
    const studenti = parseInt(prompt("Numero Studenti:", currentStudenti));
    
    if(nome && indirizzo && !isNaN(studenti)) {
        await fetch(`/api/scuole/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({nome, indirizzo, numero_studenti: studenti, codice_meccanografico: codMecc || ""})
        });
        loadSchools();
    }
}

async function deleteSchool(id) {
    if(confirm("Sei sicuro?")) {
        await fetch(`/api/scuole/${id}`, { method: 'DELETE' });
        loadSchools();
    }
}

async function addSensor(scuola_id, nomeScuola) {
    const nomeSensore = prompt(`Inserisci un nome per il nuovo punto di prelievo nella scuola ${nomeScuola} (es. Bagno Piano Primo):`);
    if(!nomeSensore) return;
    
    // Genera un topic univoco fittizio
    const randomTopic = `tesi/catania/scuole/${scuola_id}/sub_${Math.floor(Math.random() * 10000)}`;
    
    try {
        await fetch('/api/sensori', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                scuola_id: scuola_id,
                nome: nomeSensore,
                tipo: 'Acqua',
                topic_mqtt: randomTopic,
                is_main: false
            })
        });
        alert(`Sensore "${nomeSensore}" aggiunto con successo. Il simulatore inizierà a generare dati a breve.`);
    } catch(e) {
        alert("Errore nell'aggiunta del sensore.");
    }
}

// Upload CSV Logic
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const btnUpload = document.getElementById('btn-upload');

uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.style.borderColor = 'var(--accent)'; });
uploadArea.addEventListener('dragleave', () => uploadArea.style.borderColor = 'var(--text-secondary)');
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--text-secondary)';
    if(e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        uploadArea.querySelector('p').innerText = fileInput.files[0].name;
        btnUpload.style.display = 'block';
    }
});

fileInput.addEventListener('change', () => {
    if(fileInput.files.length > 0) {
        uploadArea.querySelector('p').innerText = fileInput.files[0].name;
        btnUpload.style.display = 'block';
    }
});

btnUpload.addEventListener('click', async () => {
    if(fileInput.files.length === 0) return;
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    
    btnUpload.innerText = "Caricamento...";
    try {
        const response = await fetch('/api/upload_csv', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        alert(result.message + ` (${result.righe} righe analizzate)`);
        btnUpload.innerText = "Analizza Dati";
        // Show comparison chart demo
        document.getElementById('comparison-chart-container').style.display = 'block';
        renderComparisonChart();
    } catch (e) {
        console.error(e);
        alert("Errore nell'upload");
        btnUpload.innerText = "Analizza Dati";
    }
});

// Manual Entry Logic
const btnManualEntry = document.getElementById('btn-manual-entry');
if (btnManualEntry) {
    btnManualEntry.addEventListener('click', async () => {
    const nome_scuola = prompt("Nome Scuola:");
    if (!nome_scuola) return;
    const indirizzo_scuola = prompt("Indirizzo:");
    const codice_contratto_acqua = prompt("Codice Contratto Acqua:");
    const codice_meccanografico = prompt("Codice Meccanografico:");
    const data_inizio = prompt("Data Inizio Misurazione (YYYY-MM-DD):");
    const data_fine = prompt("Data Fine Misurazione (YYYY-MM-DD):");
    const consumo = parseFloat(prompt("Consumo Rilevato (Litri/m3):"));

    if (nome_scuola && data_inizio && data_fine && !isNaN(consumo)) {
        try {
            const response = await fetch('/api/dati_reali', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    nome_scuola,
                    indirizzo_scuola: indirizzo_scuola || "",
                    codice_contratto_acqua: codice_contratto_acqua || "",
                    codice_meccanografico: codice_meccanografico || "",
                    data_inizio: data_inizio + "T00:00:00",
                    data_fine: data_fine + "T23:59:59",
                    consumo
                })
            });
            if (response.ok) {
                alert("Dato caricato con successo!");
                document.getElementById('comparison-chart-container').style.display = 'block';
                renderComparisonChart();
            } else {
                alert("Errore nel salvataggio del dato.");
            }
        } catch (e) {
            console.error(e);
            alert("Errore di rete.");
        }
    } else {
        alert("Dati non validi o operazione annullata.");
    }
});
}

function renderComparisonChart() {

    const ctxComp = document.getElementById('comparisonChart').getContext('2d');
    new Chart(ctxComp, {
        type: 'bar',
        data: {
            labels: ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu'],
            datasets: [
                {
                    label: 'Consumo Fatturato (Reale)',
                    data: [1200, 1900, 3000, 5000, 2000, 3000],
                    backgroundColor: 'rgba(59, 130, 246, 0.7)'
                },
                {
                    label: 'Consumo Sensori (Simulato)',
                    data: [1100, 1850, 3100, 4800, 2100, 2900],
                    backgroundColor: 'rgba(16, 185, 129, 0.7)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// --- Modal Ricerca Misurazione ---
const searchModal = document.getElementById('searchModal');
const btnOpenSearch = document.getElementById('btn-open-search');
const btnCloseSearch = document.getElementById('btn-close-search');
const btnExecuteSearch = document.getElementById('btn-execute-search');

if(btnOpenSearch) {
    btnOpenSearch.addEventListener('click', async () => {
        alert("Pulsante Cerca Misurazione cliccato!");
        searchModal.style.display = 'flex';
        // Populate school dropdown for search
        try {
            const response = await fetch('/api/scuole');
            const scuole = await response.json();
            const selector = document.getElementById('search-school-selector');
            selector.innerHTML = '<option value="">Tutte le scuole</option>';
            scuole.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s.id;
                opt.textContent = s.nome;
                selector.appendChild(opt);
            });
        } catch(e) {
            console.error(e);
        }
    });
}

if(btnCloseSearch) {
    btnCloseSearch.addEventListener('click', () => {
        searchModal.style.display = 'none';
    });
}

if(btnExecuteSearch) {
    btnExecuteSearch.addEventListener('click', async () => {
        const scuolaId = document.getElementById('search-school-selector').value;
        const dateVal = document.getElementById('search-date').value;
        const timeVal = document.getElementById('search-time').value;

        if(!dateVal || !timeVal) {
            alert("Inserisci sia la Data che l'Ora per effettuare la ricerca.");
            return;
        }

        const targetTime = `${dateVal}T${timeVal}:00`;
        let url = `/api/ricerca_misurazione?target_time=${encodeURIComponent(targetTime)}`;
        if (scuolaId) {
            url += `&scuola_id=${scuolaId}`;
        }

        const tbody = document.getElementById('search-results-body');
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 2rem;">Ricerca in corso...</td></tr>';

        try {
            const response = await fetch(url);
            if(!response.ok) throw new Error("Errore API");
            const data = await response.json();

            tbody.innerHTML = '';
            if(data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-secondary); padding: 2rem;">Nessuna misurazione trovata per questo orario.</td></tr>';
                return;
            }

            data.forEach(d => {
                const tr = document.createElement('tr');
                const statusBadge = d.is_anomalia ? 
                    '<span class="badge anomalia" style="background: rgba(239,68,68,0.2); color: #ef4444; border-color: #ef4444;">Anomalia</span>' : 
                    '<span class="badge normal" style="background: rgba(16,185,129,0.2); color: #10b981; border-color: #10b981;">Normale</span>';
                    
                tr.innerHTML = `
                    <td>${new Date(d.timestamp).toLocaleString()}</td>
                    <td><strong>${d.scuola_nome}</strong><br><small style="color: var(--text-secondary)">${d.sensore_nome}</small></td>
                    <td><strong>${d.valore_litri.toFixed(2)}</strong></td>
                    <td>${statusBadge}</td>
                `;
                tbody.appendChild(tr);
            });

        } catch(e) {
            console.error(e);
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--danger); padding: 2rem;">Errore durante la ricerca.</td></tr>';
        }
    });
}

// Logica per inserimento manuale consumi
const manualEntryContainer = document.getElementById('manual-entry-container');
const btnConfrontaManuale = document.getElementById('btn-confronta-manuale');

if (btnConfrontaManuale) {
    btnConfrontaManuale.addEventListener('click', async () => {
        const scuolaId = document.getElementById('manual-scuola-select').value;
        const dataInizio = document.getElementById('manual-data-inizio').value;
        const dataFine = document.getElementById('manual-data-fine').value;
        const inputValue = parseFloat(document.getElementById('manual-consumo').value.replace(',', '.'));
        const unita = document.getElementById('manual-unita').value;

        if (!scuolaId || !dataInizio || !dataFine || isNaN(inputValue)) {
            alert(`Attenzione! Compila tutti i campi:\nScuola: ${scuolaId}\nData Inizio: ${dataInizio}\nData Fine: ${dataFine}\nConsumo: Errato`);
            return;
        }

        // Convertiamo in ISO string per l'API (assumiamo orari di mezzanotte per i limiti)
        const startIso = new Date(`${dataInizio}T00:00:00`).toISOString();
        const endIso = new Date(`${dataFine}T23:59:59`).toISOString();

        btnConfrontaManuale.textContent = "⏳ Calcolo in corso...";
        btnConfrontaManuale.disabled = true;

        try {
            const url = `/api/confronto_consumi?scuola_id=${scuolaId}&start_date=${encodeURIComponent(startIso)}&end_date=${encodeURIComponent(endIso)}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error("Errore API Confronto Consumi");
            const data = await response.json();

            // Calcolo e conversione
            const consumoRealeLitri = unita === 'mc' ? inputValue * 1000 : inputValue;
            const consumoRealeMC = unita === 'mc' ? inputValue : inputValue / 1000;
            
            const consumoSimulatoLitri = data.consumo_simulato_litri || 0;
            const consumoSimulatoMC = consumoSimulatoLitri / 1000;
            
            const differenzaLitri = Math.abs(consumoRealeLitri - consumoSimulatoLitri);
            const differenzaMC = Math.abs(consumoRealeMC - consumoSimulatoMC);

            // Mostra risultati
            document.getElementById('manual-result-container').style.display = 'block';
            
            document.getElementById('res-consumo-reale').innerHTML = `
                ${consumoRealeLitri.toLocaleString('it-IT', {minimumFractionDigits: 2, maximumFractionDigits: 2})} L<br>
                <span style="font-size: 0.8rem; color: #9ca3af;">${consumoRealeMC.toLocaleString('it-IT', {minimumFractionDigits: 2, maximumFractionDigits: 2})} m³</span>
            `;
            document.getElementById('res-consumo-simulato').innerHTML = `
                ${consumoSimulatoLitri.toLocaleString('it-IT', {minimumFractionDigits: 2, maximumFractionDigits: 2})} L<br>
                <span style="font-size: 0.8rem; color: #9ca3af;">${consumoSimulatoMC.toLocaleString('it-IT', {minimumFractionDigits: 2, maximumFractionDigits: 2})} m³</span>
            `;
            
            const diffEl = document.getElementById('res-differenza');
            diffEl.innerHTML = `
                ${differenzaLitri.toLocaleString('it-IT', {minimumFractionDigits: 2, maximumFractionDigits: 2})} L<br>
                <span style="font-size: 0.8rem; color: #9ca3af;">${differenzaMC.toLocaleString('it-IT', {minimumFractionDigits: 2, maximumFractionDigits: 2})} m³</span>
            `;
            
            // Colore differenza in base alla tolleranza (es. 10%)
            const tolleranza = consumoRealeLitri * 0.10;
            if (differenzaLitri > tolleranza) {
                diffEl.style.color = "var(--danger)";
            } else {
                diffEl.style.color = "var(--success)";
            }
            
            // Danno Economico
            const tariffa = parseFloat(document.getElementById('manual-tariffa').value) || 2.50;
            const dannoEuro = differenzaMC * tariffa;
            document.getElementById('res-danno-euro').textContent = `${dannoEuro.toLocaleString('it-IT', {minimumFractionDigits: 2, maximumFractionDigits: 2})} €`;
            
            // Salva nello storico
            const btnSalva = document.getElementById('btn-salva-storico');
            btnSalva.style.display = 'inline-block';
            btnSalva.onclick = async () => {
                const selectEl = document.getElementById('manual-scuola-select');
                const nomeScuolaCompleto = selectEl.options[selectEl.selectedIndex].text;
                // Il testo della select è tipo "Liceo Galileo - ID 1" -> prendiamo la prima parte
                const nomeScuola = nomeScuolaCompleto.split(' - ')[0].trim(); 
                await fetch('/api/dati_reali', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        nome_scuola: nomeScuola,
                        indirizzo_scuola: "N/A",
                        codice_contratto_acqua: "N/A",
                        codice_meccanografico: "N/A",
                        data_inizio: startIso,
                        data_fine: endIso,
                        consumo: consumoRealeMC
                    })
                });
                alert("Salvato nello storico con successo!");
                btnSalva.style.display = 'none';
                loadStoricoBollette();
            };
            
        } catch(e) {
            console.error("Errore confronto", e);
            alert("Si è verificato un errore durante il calcolo del confronto.");
        } finally {
            btnConfrontaManuale.textContent = "🔍 Calcola ed Esegui Confronto";
            btnConfrontaManuale.disabled = false;
        }
    });
}

// Orologio Live Sincronizzato con Internet
async function initLiveClock() {
    const clockEl = document.getElementById('live-clock');
    if (!clockEl) return;
    
    let timeOffset = 0;
    try {
        // Fetch dell'ora ufficiale da internet
        const res = await fetch('http://worldtimeapi.org/api/timezone/Europe/Rome');
        if (res.ok) {
            const data = await res.json();
            const serverTime = new Date(data.datetime).getTime();
            const localTime = Date.now();
            timeOffset = serverTime - localTime;
        }
    } catch(e) {
        console.warn("Impossibile recuperare l'ora da internet, utilizzo l'orario locale.");
    }
    
    setInterval(() => {
        const now = new Date(Date.now() + timeOffset);
        
        const day = String(now.getDate()).padStart(2, '0');
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const year = now.getFullYear();
        
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        
        clockEl.textContent = `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
    }, 1000);
}
initLiveClock();

// Logica PDF Upload
const btnPdf = document.getElementById('btn-upload-pdf');
const inputPdf = document.getElementById('pdf-bolletta-input');
const statusPdf = document.getElementById('pdf-status');
if (btnPdf && inputPdf) {
    btnPdf.onclick = () => inputPdf.click();
    inputPdf.onchange = async (e) => {
        if (!e.target.files.length) return;
        const file = e.target.files[0];
        statusPdf.textContent = "Lettura AI in corso...";
        
        const fd = new FormData();
        fd.append("file", file);
        
        try {
            const res = await fetch('/api/upload_pdf_bolletta', { method: 'POST', body: fd });
            if (!res.ok) throw new Error("Errore lettura PDF");
            const data = await res.json();
            
            if (data.data_inizio) {
                // Formatta dd/mm/yyyy in yyyy-mm-dd
                const parts = data.data_inizio.split('/');
                if (parts.length === 3) document.getElementById('manual-data-inizio').value = `${parts[2]}-${parts[1]}-${parts[0]}`;
            }
            if (data.data_fine) {
                const parts = data.data_fine.split('/');
                if (parts.length === 3) document.getElementById('manual-data-fine').value = `${parts[2]}-${parts[1]}-${parts[0]}`;
            }
            if (data.consumo_mc) {
                document.getElementById('manual-consumo').value = data.consumo_mc;
                document.getElementById('manual-unita').value = 'mc';
            }
            statusPdf.textContent = "";
            const feedbackAlert = document.getElementById('pdf-feedback-alert');
            if(feedbackAlert) {
                feedbackAlert.style.display = 'block';
                // Animazione visiva per i campi aggiornati
                ['manual-data-inizio', 'manual-data-fine', 'manual-consumo'].forEach(id => {
                    const el = document.getElementById(id);
                    if(el) {
                        el.style.transition = 'background-color 0.5s';
                        el.style.backgroundColor = 'rgba(16, 185, 129, 0.4)';
                        setTimeout(() => { el.style.backgroundColor = 'rgba(0,0,0,0.5)'; }, 2000);
                    }
                });
            }
        } catch (err) {
            statusPdf.textContent = "❌ Errore: PDF non leggibile.";
        }
    };
}

// Logica Grafico Storico (Tabella + Trend)
let trendChart = null;
async function loadStoricoBollette() {
    const tableBody = document.getElementById('storico-table-body');
    const ctxTrend = document.getElementById('trendDanniChart');
    if (!tableBody) return;
    
    const scuolaSelect = document.getElementById('manual-scuola-select');
    const scuolaId = scuolaSelect ? scuolaSelect.value : "";
    const tariffa = parseFloat(document.getElementById('manual-tariffa')?.value) || 2.50;
    
    try {
        const res = await fetch(`/api/storico_confronti?scuola_id=${scuolaId}`);
        const dati = await res.json();
        
        tableBody.innerHTML = '';
        
        const labels = [];
        const danni = [];
        
        dati.forEach(d => {
            const bollettaMc = d.consumo_bolletta_litri / 1000;
            const simulatoMc = d.consumo_simulato_litri / 1000;
            const diffLitri = Math.abs(d.consumo_bolletta_litri - d.consumo_simulato_litri);
            const danno = (diffLitri / 1000) * tariffa;
            
            labels.push(d.periodo);
            danni.push(danno);
            
            const tr = document.createElement('tr');
            tr.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
            tr.innerHTML = `
                <td style="padding: 1rem 0.5rem;">${d.periodo}</td>
                <td style="padding: 1rem 0.5rem;"><strong>${d.nome_scuola}</strong></td>
                <td style="padding: 1rem 0.5rem; color: #60a5fa;">${bollettaMc.toLocaleString('it-IT', {minimumFractionDigits:2, maximumFractionDigits:2})} m³</td>
                <td style="padding: 1rem 0.5rem; color: #34d399;">${simulatoMc.toLocaleString('it-IT', {minimumFractionDigits:2, maximumFractionDigits:2})} m³</td>
                <td style="padding: 1rem 0.5rem; color: var(--warning);">${diffLitri.toLocaleString('it-IT', {minimumFractionDigits:0, maximumFractionDigits:0})} L</td>
                <td style="padding: 1rem 0.5rem; color: var(--danger); font-weight: bold;">${danno.toLocaleString('it-IT', {minimumFractionDigits:2, maximumFractionDigits:2})} €</td>
            `;
            tableBody.appendChild(tr);
        });
        
        if (!ctxTrend) return;
        if (trendChart) trendChart.destroy();
        
        trendChart = new Chart(ctxTrend, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Trend Danno Economico Stimato (€)',
                    data: danni,
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: '#ef4444',
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true, title: { display: true, text: 'Euro (€)' } }
                }
            }
        });
        
    } catch(e) {
        console.error("Errore caricamento storico", e);
    }
}
// Carichiamo lo storico quando si apre la tab Dati Reali o si cambia la scuola
document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
        if (btn.getAttribute('data-view') === 'dati-reali') {
            loadStoricoBollette();
        }
    });
});
document.getElementById('manual-scuola-select')?.addEventListener('change', loadStoricoBollette);
