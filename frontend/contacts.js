document.addEventListener("DOMContentLoaded", async function () {

  const API_BASE = "https://medication-reminder-gvb4.onrender.com";

  const docContainer = document.getElementById("doctorContainer");
  const template = document.getElementById("doctorTemplate");
  const searchBox = document.getElementById("searchBox");
  const searchBtn = document.getElementById("searchBtn");
  const noResultsMsg = document.querySelector(".no-results");

  let allDoctors = [];

  // -------------------------------
  // 📥 FETCH DOCTORS
  // -------------------------------
  async function loadDoctors() {
    try {
      const res = await fetch(`${API_BASE}/doctors/all`);

      if (!res.ok) throw new Error("API error");

      const doctors = await res.json();
      allDoctors = doctors;

      renderDoctors(doctors);

    } catch (error) {
      console.error("❌ Fetch error:", error);
      docContainer.innerHTML = "<p>⚠️ Failed to load doctors</p>";
    }
  }

  // -------------------------------
  // 🧠 RENDER DOCTORS
  // -------------------------------
  function renderDoctors(doctors) {
    docContainer.innerHTML = "";

    if (!doctors || doctors.length === 0) {
      noResultsMsg.style.display = "block";
      return;
    }

    noResultsMsg.style.display = "none";

    doctors.forEach((doc) => {
      const card = template.cloneNode(true);

      card.style.display = "block";
      card.removeAttribute("id");

      // ✅ Fill data
      card.querySelector("#doctorName").textContent = doc.name;
      card.querySelector("#doctorSpecialization").textContent = doc.specialization;
      card.querySelector("#doctorHospital").textContent = doc.hospital_name || "N/A";
      card.querySelector("#doctorContact").textContent = doc.contact_no || "N/A";
      card.querySelector("#doctorGender").textContent = doc.gender || "N/A";
      card.querySelector("#doctorTimings").textContent =
        `${doc.available_from || "--"} - ${doc.available_to || "--"}`;

      card.querySelector("#doctorImage").src =
        "https://cdn-icons-png.flaticon.com/512/3774/3774299.png";

      card.querySelector("#contactBtn").onclick = () => {
        alert(`📞 Calling ${doc.name}...`);
      };

      docContainer.appendChild(card);
    });
  }

  // -------------------------------
  // 🔍 SEARCH (LIVE FILTER)
  // -------------------------------
  function filterDoctors() {
    const query = searchBox.value.toLowerCase().trim();

    const filtered = allDoctors.filter(doc =>
      (doc.name || "").toLowerCase().includes(query) ||
      (doc.specialization || "").toLowerCase().includes(query) ||
      (doc.hospital_name || "").toLowerCase().includes(query)
    );

    renderDoctors(filtered);
  }

  searchBox.addEventListener("keyup", filterDoctors);
  searchBtn.addEventListener("click", (e) => {
    e.preventDefault();
    filterDoctors();
  });

  // -------------------------------
  // 🚀 INIT
  // -------------------------------
  loadDoctors();
});