const form = document.querySelector("#lookupForm");
const input = document.querySelector("#companyName");
const emptyState = document.querySelector("#emptyState");
const loadingState = document.querySelector("#loadingState");
const errorState = document.querySelector("#errorState");
const resultCard = document.querySelector("#resultCard");

const fields = {
  exchange: document.querySelector("#exchange"),
  companyTitle: document.querySelector("#companyTitle"),
  website: document.querySelector("#website"),
  symbol: document.querySelector("#symbol"),
  price: document.querySelector("#price"),
  priceSource: document.querySelector("#priceSource"),
  revenue: document.querySelector("#revenue"),
  revenueSource: document.querySelector("#revenueSource"),
  marketCap: document.querySelector("#marketCap"),
  updatedAt: document.querySelector("#updatedAt"),
};

function setVisible(element, visible) {
  element.classList.toggle("hidden", !visible);
}

function showLoading() {
  setVisible(emptyState, false);
  setVisible(errorState, false);
  setVisible(resultCard, false);
  setVisible(loadingState, true);
}

function showError(message) {
  errorState.textContent = message;
  setVisible(emptyState, false);
  setVisible(loadingState, false);
  setVisible(resultCard, false);
  setVisible(errorState, true);
}

function displayResult(data) {
  fields.exchange.textContent = data.exchange || "Yahoo Finance";
  fields.companyTitle.textContent = data.companyName || data.symbol;
  fields.symbol.textContent = data.symbol;
  fields.price.textContent = data.latestPriceFormatted || "Not available";
  fields.priceSource.textContent = data.priceSource ? `Source: ${data.priceSource}` : "No market price returned";
  fields.revenue.textContent = data.revenueFormatted || "Not available";
  fields.revenueSource.textContent = data.revenueSource
    ? `${data.revenueSource}${data.revenuePeriod ? `, ${data.revenuePeriod}` : ""}`
    : "No revenue returned";
  fields.marketCap.textContent = data.marketCapFormatted || "Not available";
  fields.updatedAt.textContent = `Updated ${data.updatedAt}`;

  if (data.website) {
    fields.website.href = data.website;
    fields.website.textContent = data.website.replace(/^https?:\/\//, "");
    setVisible(fields.website, true);
  } else {
    fields.website.removeAttribute("href");
    fields.website.textContent = "";
    setVisible(fields.website, false);
  }

  setVisible(emptyState, false);
  setVisible(loadingState, false);
  setVisible(errorState, false);
  setVisible(resultCard, true);
}

async function lookupCompany(name) {
  showLoading();
  try {
    const response = await fetch(`/api/company?name=${encodeURIComponent(name)}`);
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Unable to load company data.");
    }
    displayResult(data);
  } catch (error) {
    showError(error.message);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const name = input.value.trim();
  if (name) {
    lookupCompany(name);
  }
});

document.querySelectorAll("[data-company]").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.dataset.company;
    lookupCompany(button.dataset.company);
  });
});
