// login.js
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("loginForm");
  const messageBox = document.getElementById("messageBox");

  // 🔗 Backend URL (CHANGE THIS)
  const API_URL = "https://medication-reminder-gvb4.onrender.com";

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();

      if (data.success) {
        showMessage("✅ Login successful! Redirecting...", "success");

        // ✅ Store login session (token or user data)
        localStorage.setItem("isLoggedIn", "true");
        localStorage.setItem("user", JSON.stringify(data.user)); // optional

        setTimeout(() => {
          window.location.href = "dashboard.html";
        }, 1500);

      } else {
        showMessage(data.message || "❌ Invalid email or password.", "error");
      }

    } catch (error) {
      console.error("Login error:", error);
      showMessage("⚠️ Cannot connect to server.", "error");
    }
  });

  function showMessage(msg, type) {
    messageBox.textContent = msg;
    messageBox.style.color = type === "error" ? "red" : "green";
  }
});