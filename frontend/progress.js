// progress.js
document.addEventListener("DOMContentLoaded", async function () {

  const totalEl = document.getElementById("totalCount");
  const takenEl = document.getElementById("takenCount");
  const missedEl = document.getElementById("missedCount");

  // 🔗 Backend URL (CHANGE THIS)
  const API_URL = "https://medication-reminder-gvb4.onrender.com";

  let reminders = [];

  // -------------------------------
  // Fetch reminders from backend
  // -------------------------------
  try {
    const res = await fetch(`${API_URL}/reminders/all`);

    if (!res.ok) {
      throw new Error("Failed to fetch reminders");
    }

    reminders = await res.json();

  } catch (err) {
    console.error("❌ Error fetching reminders:", err);

    document.querySelector(".progress-container").innerHTML = `
      <p style="text-align:center; color:red;">
        ⚠️ Unable to load data. Check backend connection.
      </p>
    `;
    return;
  }

  // -------------------------------
  // Calculate counts
  // -------------------------------
  const total = reminders.length;
  const taken = reminders.filter(r => r.status === "taken").length;
  const missed = reminders.filter(r => r.status === "missed").length;
  const pending = total - taken - missed;

  // -------------------------------
  // Update UI
  // -------------------------------
  totalEl.textContent = total;
  takenEl.textContent = taken;
  missedEl.textContent = missed;

  // -------------------------------
  // Chart.js Data
  // -------------------------------
  const data = {
    labels: ["Taken 💊", "Missed ❌", "Pending ⏳"],
    datasets: [{
      data: [taken, missed, pending],
      backgroundColor: ["#4caf50", "#f44336", "#ff9800"],
      hoverOffset: 12
    }]
  };

  const config = {
    type: "pie",
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom"
        },
        title: {
          display: true,
          text: "Medicine Intake Progress 💊"
        }
      }
    }
  };

  // -------------------------------
  // Render Chart
  // -------------------------------
  const ctx = document.getElementById("progressChart");
  if (ctx) {
    new Chart(ctx, config);
  }

  // -------------------------------
  // No data message
  // -------------------------------
  if (total === 0) {
    document.querySelector(".progress-container").innerHTML = `
      <p style="text-align:center; font-size:18px; color:#666;">
        No reminders found. Add reminders first! 🕒
      </p>
    `;
  }
});