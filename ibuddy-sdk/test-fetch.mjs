// Run with: node test-fetch.mjs
// Tests the same fetch call the SDK makes from Node.js (no CORS)

const BASE_URL = "http://127.0.0.1:8000";
const ENDPOINT = "/api/v1/chat";
const url = `${BASE_URL}${ENDPOINT}`;

const body = JSON.stringify({
  query: "Hello",
  conversation_history: []
});

console.log("Testing POST", url);

try {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body
  });

  console.log("Status:", response.status, response.statusText);
  console.log("Response headers:", Object.fromEntries(response.headers.entries()));

  const text = await response.text();
  console.log("Body:", text);
} catch (err) {
  console.error("fetch threw:", err.message);
  console.error("cause:", err.cause);
}
