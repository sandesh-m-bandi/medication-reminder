document.addEventListener("DOMContentLoaded", async function () {
  const container = document.querySelector("main");
  const searchBox = document.getElementById("searchBox");
  const searchBtn = document.getElementById("searchBtn");
  const noResultsMsg = document.querySelector(".no-results");
  const docContainer = document.getElementById("doctorContainer");
  const template = document.getElementById("doctorTemplate");

  // 🔗 ✅ CHANGE THIS
  const API_BASE = "https://medication-reminder-gvb4.onrender.com";

  // -------------------------------
  // 📥 Load doctors from database
  // -------------------------------
  async function loadDoctorsFromDB() {
    try {
      const res = await fetch(`${API_BASE}/all`);

      if (!res.ok) {
        throw new Error("Failed to fetch doctors");
      }

      const doctors = await res.json();
      renderDoctors(doctors);

    } catch (err) {
      console.error("❌ Error loading doctors:", err);
      container.innerHTML = `<p class="error">⚠️ Could not load doctors from database.</p>`;
    }
  }

  // -------------------------------
  // 🧠 Render doctors
  // -------------------------------
  function renderDoctors(doctors) {
    docContainer.innerHTML = "";

    if (!doctors || doctors.length === 0) {
      noResultsMsg.style.display = "block";
      return;
    }

    noResultsMsg.style.display = "none";

    doctors.forEach((doctor) => {
      const card = template.cloneNode(true);
      card.style.display = "block";
      card.removeAttribute("id");

      card.querySelector("#doctorName").textContent = doctor.name;
      card.querySelector("#doctorSpecialization").textContent = doctor.specialization;
      card.querySelector("#doctorHospital").textContent = doctor.hospital_name || "N/A";
      card.querySelector("#doctorContact").textContent = doctor.contact_no || "N/A";
      card.querySelector("#doctorGender").textContent = doctor.gender || "N/A";
      card.querySelector("#doctorTimings").textContent =
        `${doctor.available_from || "--:--"} - ${doctor.available_to || "--:--"}`;

      card.querySelector("#doctorImage").src =
        "https://cdn-icons-png.flaticon.com/512/3774/3774299.png";

      const contactBtn = card.querySelector("#contactBtn");
      contactBtn.onclick = () => alert(`Calling ${doctor.name}...`);

      docContainer.appendChild(card);
    });
  }

  // -------------------------------
  // 🔍 Search filter
  // -------------------------------
  function filterDoctors() {
    const query = searchBox.value.toLowerCase().trim();
    const doctorCards = document.querySelectorAll(".doctor-card:not(#doctorTemplate)");

    let visibleCount = 0;

    doctorCards.forEach((card) => {
      const text = card.textContent.toLowerCase();

      if (text.includes(query)) {
        card.style.display = "block";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    noResultsMsg.style.display = visibleCount === 0 ? "block" : "none";
  }

  // -------------------------------
  // 🎯 Event listeners
  // -------------------------------
  searchBox.addEventListener("keyup", filterDoctors);

  searchBtn.addEventListener("click", (e) => {
    e.preventDefault();
    filterDoctors();
  });

  // -------------------------------
  // 🚀 MAIN EXECUTION
  // -------------------------------
  await loadDoctorsFromDB();
});