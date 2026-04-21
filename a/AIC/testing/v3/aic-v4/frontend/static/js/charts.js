function renderEntityChart(history) {
    const ctx = document.getElementById("entityChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: history.map(h => h.timestamp),
            datasets: [{
                label: "Score",
                data: history.map(h => h.score),
                borderColor: "#007bff",
                tension: 0.3
            }]
        }
    });
}

function renderHistoryChart(history) {
    const ctx = document.getElementById("historyChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: history.map(h => h.timestamp),
            datasets: [{
                label: "Score",
                data: history.map(h => h.score),
                borderColor: "#28a745",
                tension: 0.3
            }]
        }
    });
}