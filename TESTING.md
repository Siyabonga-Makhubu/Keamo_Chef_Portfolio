# Portfolio automation tests

The pytest suite covers the portfolio's HTML pages and browser interactions in
both Playwright and Selenium. Browser tests use a temporary local HTTP server;
the registration and contact tests mock the API responses and do not require the
application backend. Third-party scripts are stubbed or blocked so the suite
does not depend on external CDN availability.

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
