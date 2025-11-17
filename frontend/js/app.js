window.ui = {
    showFiles: (files) => {
        const list = document.getElementById("document-list");
        list.innerHTML = "";

        files.forEach(f => {
            const li = document.createElement("li");
            li.textContent = f.name;
            list.appendChild(li);
        });
    }
};

console.log("UI inicializada");
/* ===============================
   YEARS + QUARTERS MAPPING
================================ */

const QUARTERS = {
    "2025": {
        "Q1": ["01_2025", "02_2025", "03_2025"],
        "Q2": ["04_2025", "05_2025", "06_2025"],
        "Q3": ["07_2025", "08_2025", "09_2025"],
        "Q4": ["10_2025", "11_2025", "12_2025"]
    },
    "2026": {
        "Q1": ["01_2026", "02_2026", "03_2026"],
        "Q2": ["04_2026", "05_2026", "06_2026"],
        "Q3": ["07_2026", "08_2026", "09_2026"],
        "Q4": ["10_2026", "11_2026", "12_2026"]
    }
};

/* ===============================
   UPDATE MONTHS WHEN YEAR OR QUARTER CHANGES
================================ */

function updateMonths() {
    const year = document.getElementById("year-dropdown").value;
    const quarter = document.querySelector("input[name='quarter']:checked");

    if (!quarter) return;

    const q = quarter.value;
    const months = QUARTERS[year][q];

    const container = document.getElementById("months-container");
    container.innerHTML = "";

    months.forEach(m => {
        container.innerHTML += `
            <label>
                <input type="checkbox" class="month-check" value="${m}" checked> ${m}
            </label><br>
        `;
    });
}

document.getElementById("year-dropdown").addEventListener("change", updateMonths);

document.querySelectorAll("input[name='quarter']").forEach(radio => {
    radio.addEventListener("change", updateMonths);
});
async function runScan() {
    const year = document.getElementById("year-dropdown").value;
    
    // meses selecionados
    const months = [...document.querySelectorAll(".month-check:checked")]
        .map(cb => cb.value);

    if (months.length === 0) {
        alert("Selecione pelo menos um mês.");
        return;
    }

    const payload = { year, months };

    const response = await fetch("http://127.0.0.1:8000/rh/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await response.json();
    console.log("SCAN RESULT:", data);

    renderScanResults(data);
}
function renderScanResults(data) {
    const container = document.getElementById("scan-results");
    container.innerHTML = "";

    for (const monthKey in data.months) {
        const month = data.months[monthKey];

        container.innerHTML += `
            <div class="scan-month-block">
                <h3>${monthKey}</h3>
                <ul>
                    ${Object.entries(month.groups).map(([g, info]) => `
                        <li>
                          Grupo ${g}: 
                          ${info.files.length > 0 
                            ? info.files.length + " ficheiros"
                            : "<span style='color: orange;'>vazio ⚠</span>"
                          }
                        </li>
                    `).join("")}
                </ul>
            </div>
        `;
    }
}
async function runBaseJoin() {
    const year = document.getElementById("year-dropdown").value;

    const months = [...document.querySelectorAll(".month-check:checked")]
        .map(cb => cb.value);

    if (months.length === 0) {
        alert("Selecione pelo menos um mês.");
        return;
    }

    const payload = { year, months };

    const res = await fetch("http://127.0.0.1:8000/rh/join/base", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await res.json();
    console.log("BASE JOIN:", data);

    renderBaseJoin(data);
}
function renderBaseJoin(data) {
    const container = document.getElementById("base-join-results");
    container.innerHTML = "";

    for (const month in data) {
        const { pdf, warnings } = data[month];

        container.innerHTML += `
            <div class="base-join-block">
                <h3>${month}</h3>
                <p><strong>PDF:</strong> ${pdf}</p>
                <p>${warnings.length > 0 
                        ? "<strong>Avisos:</strong> " + warnings.join(", ")
                        : "Sem avisos"
                   }
                </p>
                <a href="file:///${pdf.replace(/\\/g, "/")}" target="_blank" class="btn-open">
                    Abrir PDF
                </a>
            </div>
        `;
    }
}
