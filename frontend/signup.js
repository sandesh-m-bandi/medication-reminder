// signup.js
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("signupForm");
  const messageBox = document.getElementById("messageBox");

  // 🔗 Backend URL
  const API_URL = "https://medication-reminder-gvb4.onrender.com";

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirmPassword").value.trim();

    // Validation
    if (!username || !email || !password || !confirmPassword) {
      showMessage("⚠️ Please fill in all fields.", "error");
      return;
    }

    if (password !== confirmPassword) {
      showMessage("❌ Passwords do not match.", "error");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/users/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, email, password })
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();

      if (data.success) {
        showMessage("✅ Signup successful! Please login.", "success");

        setTimeout(() => {
          window.location.href = "login.html";
        }, 1500);

      } else {
        showMessage(data.message || "Signup failed.", "error");
      }

    } catch (error) {
      console.error("Signup error:", error);
      showMessage("⚠️ Cannot connect to server.", "error");
    }
  });

  function showMessage(msg, type) {
    messageBox.textContent = msg;
    messageBox.style.color = type === "error" ? "red" : "green";
  }
});