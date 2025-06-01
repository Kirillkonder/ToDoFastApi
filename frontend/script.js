const baseUrl = "http://localhost:8000";

function getToken()       { return localStorage.getItem("token"); }
function setToken(token)  { localStorage.setItem("token", token); }
function clearToken()     { localStorage.removeItem("token"); }

function showError(id, message) {
  const alert = document.getElementById(id);
  alert.className = "alert alert-danger";
  alert.textContent = message;
  alert.classList.remove("d-none");
}

async function registerUser(e) {
  e.preventDefault();
  const { username, password } = Object.fromEntries(new FormData(e.target));
  try {
    const resp = await fetch(`${baseUrl}/users/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    if (!resp.ok) throw await resp.json();
    document.getElementById('regAlert').className = "alert alert-success";
    document.getElementById('regAlert').textContent = "Успешно! Перенаправление…";
    setTimeout(() => { window.location = "/static/login.html"; }, 1000);
  } catch (err) {
    showError('regAlert', err.detail || "Ошибка регистрации");
  }
}

async function loginUser(e) {
  e.preventDefault();
  const { username, password } = Object.fromEntries(new FormData(e.target));
  try {
    const body = new URLSearchParams({ username, password });
    const resp = await fetch(`${baseUrl}/users/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body
    });
    if (!resp.ok) throw await resp.json();
    const data = await resp.json();
    setToken(data.access_token);
    window.location = "/static/home.html";
  } catch (err) {
    showError('loginAlert', err.detail || "Неверные данные");
  }
}

function logout() {
  clearToken();
  window.location = "/static/login.html";
}
