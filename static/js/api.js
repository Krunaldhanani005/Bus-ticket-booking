const API_BASE_URL = "http://localhost:8000";

async function apiCall(endpoint, method = "GET", body = null) {
    const headers = {
        "Content-Type": "application/json"
    };

    const config = {
        method: method,
        headers: headers
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error("API Call Failed:", error);
        alert("Something went wrong. Please try again.");
        throw error;
    }
}

// User Session Management (Simple)
const SESSION_KEY = "user_email";
function loginUser(email) {
    localStorage.setItem(SESSION_KEY, email);
}
function getCurrentUser() {
    return localStorage.getItem(SESSION_KEY);
}
function logoutUser() {
    localStorage.removeItem(SESSION_KEY);
    window.location.href = "index.html";
}
