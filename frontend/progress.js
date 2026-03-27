// progress.js
document.addEventListener("DOMContentLoaded", function () {
  // Get progress elements
  const totalEl = document.getElementById("totalCount");
  const takenEl = document.getElementById("takenCount");
  const missedEl = document.getElementById("missedCount");

  // Fetch reminders data from localStorage (saved by reminders.js)
  const reminders = JSON.parse(localStorage.getItem("reminders")) || [];

  // Calculate counts
  const total = reminders.length;
  const taken = reminders.filter(r => r.status === "taken").length;
  const missed = reminders.filter(r => r.status === "missed").length;

  // Update stats on the page
  totalEl.textContent = total;
  takenEl.textContent = taken;
  missedEl.textContent = missed;

  // Prepare data for Chart.js
  const data = {
    labels: ["Taken 💊", "Missed ❌", "Pending ⏳"],
    datasets: [{
      data: [taken, missed, total - taken - missed],
      backgroundColor: ["#4caf50", "#f44336", "#ff9800"],
      hoverOffset: 12
    }]
  };

  // Configure the chart
  const config = {
    type: "pie",
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color: "#333",
            font: { size: 14 }
          }
        },
        title: {
          display: true,
          text: "Medicine Intake Progress 💊",
          font: { size: 20 },
          color: "#333"
        }
      }
    }
  };

  // Render chart
  const ctx = document.getElementById("progressChart");
  if (ctx) {
    new Chart(ctx, config);
  }

  // Message if no reminders
  if (total === 0) {
    document.querySelector(".progress-container").innerHTML = `
      <p style="text-align:center; font-size:18px; color:#666;">
        No reminders added yet. Go to <strong>Reminders</strong> to add your first one! 🕒
      </p>
    `;
  }
});
