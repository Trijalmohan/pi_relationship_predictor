async function run() {
    const dob = document.getElementById("dob").value.trim();
    const choice = document.getElementById("choice").value;
    const output = document.getElementById("output");

    if (!dob || dob.length !== 8 || isNaN(dob)) {
        output.innerHTML = "⚠️ Please enter a valid date in DDMMYYYY format.";
        output.classList.add("fade-show");
        return;
    }

    output.innerHTML = "⏳ Searching inside π… please wait...";
    output.classList.add("fade-show");

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ dob, choice })
        });

        const data = await response.json();
        output.innerHTML = "";

        if (data.error) {
            output.innerHTML = `❌ Error: ${data.error}`;
            return;
        }

        let section = "";

        for (const key in data) {
            const item = data[key];
            section += `
                <div class="result-card">
                    <h3>${key === "partner" ? "❤️ Partner" : "💙 Close Friend"}</h3>
                    <p>🎂 Age: <b>${item.age}</b></p>
                    <p>📅 DOB: <b>${item.dob}</b></p>
                    <p>🔍 Appears at digit: <b>${item.pos?.toLocaleString()}</b></p>
                    <p>📌 Context: <code>${item.context}</code></p>
                </div>`;
        }

        output.innerHTML = section;
        output.scrollTop = output.scrollHeight;

    } catch (err) {
        output.innerHTML = `❌ Network error: ${err}`;
    }
}
