# Portfolio automation tests

The pytest suite covers the portfolio's HTML pages and browser interactions in
both Playwright and Selenium. Browser tests use a temporary local HTTP server;
registration tests mock API responses, and contact tests mock browser window
opening so they do not require a backend or send real WhatsApp messages.
Third-party scripts are stubbed or blocked so the suite does not depend on
external CDN availability.

## Configure the WhatsApp contact form

Set `window.CHEF_WHATSAPP_NUMBER` in `contact-config.js` to the chef's WhatsApp
number in international format using digits only, with no `+`, spaces, or
punctuation (for example, a South African number starts with `27`). This is a
public contact detail; do not put credentials in this file. If it is blank or
invalid, the form displays a configuration message instead of opening a
malformed link.

The portfolio is a static site. From the workspace root, start Python's local
HTTP server:

```powershell
python -m http.server 8000
```

Open `http://localhost:8000/index.html` or
`http://localhost:8000/contact.html` in a browser. Fill in the form and select
**Send via WhatsApp**; verify that WhatsApp opens with the prefilled enquiry.
Review it and press **Send** in WhatsApp to send it.

## Deploy to GitHub Pages

In the repository settings, open **Pages** and set **Build and deployment →
Source** to **GitHub Actions**. The `Deploy portfolio to GitHub Pages` workflow
then deploys on pushes to `main`; it can also be run manually from the
repository's **Actions** tab. The project site URL will be
`https://siyabonga-makhubu.github.io/Keamo_Chef_Portfolio/`.

## Setup

From the portfolio workspace root, install the Python dependencies and the
Playwright Chromium browser:

```powershell
python -m pip install -r requirements-test.txt
python -m playwright install chromium
```

Selenium uses the installed Google Chrome browser and Selenium Manager to
resolve a compatible ChromeDriver on first run. Ensure Chrome is installed and
that Selenium Manager can access its driver download source.

## Run all tests

```powershell
python -m pytest
```

Run only one browser's tests:

```powershell
python -m pytest tests/test_portfolio_playwright.py
python -m pytest tests/test_portfolio_selenium.py
```
