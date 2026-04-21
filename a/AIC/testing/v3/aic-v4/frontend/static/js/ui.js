document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("scoreForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const entity = document.getElementById("entityInput").value;
        const resultDiv = document.getElementById("scoreResult");

        resultDiv.innerHTML = "<div class='text-muted'>Scoring...</div>";

        const res = await fetch("/api/score", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ entity })
        });

        const data = await res.json();

        if (data.error) {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        } else {
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                    Score: <strong>${data.score}</strong><br>
                    Confidence: <strong>${data.confidence}</strong>
                </div>
            `;
        }
    });
});