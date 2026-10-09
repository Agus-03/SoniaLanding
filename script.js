// SONIA Early Adopter validation event
// For production, set API_ENDPOINT to your backend endpoint.
// Expected response: { "ok": true } or HTTP 2xx.
// The endpoint should increment an aggregate click counter server-side.

const API_ENDPOINT = "/api/early-adopter-click";

const button = document.getElementById("earlyAdopterButton");
const status = document.getElementById("earlyStatus");

async function registerEarlyAdopterInterest() {
  button.disabled = true;
  status.className = "early-status";
  status.textContent = "Registrando tu interés…";

  try {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        event: "early_adopter_cta_click",
        page: window.location.pathname,
        referrer: document.referrer || null,
        utm_source: new URLSearchParams(location.search).get("utm_source"),
        utm_medium: new URLSearchParams(location.search).get("utm_medium"),
        utm_campaign: new URLSearchParams(location.search).get("utm_campaign")
      }),
      keepalive: true
    });

    if (!response.ok) throw new Error("endpoint-not-ready");

    status.textContent =
      "¡Gracias por tu interés! El programa Early Adopter todavía no está habilitado. Tu interés quedó registrado y nos ayuda a validar la demanda de SONIA.";
    status.classList.add("error");
  } catch (error) {
    // Prototype fallback: preserves a local count when no backend is connected.
    const key = "sonia_early_adopter_clicks";
    const count = Number(localStorage.getItem(key) || 0) + 1;
    localStorage.setItem(key, String(count));

    status.textContent =
      "El acceso Early Adopter todavía no está habilitado. Registramos tu interés para esta etapa de validación.";
    status.classList.add("error");
  } finally {
    button.disabled = false;
  }
}

button.addEventListener("click", registerEarlyAdopterInterest);

document.querySelectorAll("[data-early-adopter]").forEach((link) => {
  link.addEventListener("click", () => {
    // The actual event is sent when the user presses the final CTA.
  });
});
