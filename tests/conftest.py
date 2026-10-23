from __future__ import annotations

import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterator

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKIPPED_ASSET_SUFFIXES = (
    ".mov",
    ".mp4",
    ".zip",
)


class QuietStaticHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass

    def handle_error(self, request: object, client_address: object) -> None:
        pass


@pytest.fixture(scope="session")
def base_url() -> Iterator[str]:
    handler = partial(QuietStaticHandler, directory=str(PROJECT_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture(scope="session")
def playwright_browser() -> Iterator[object]:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def playwright_page(playwright_browser: object) -> Iterator[object]:
    context = playwright_browser.new_context()
    context.add_init_script(
        "window.lucide = { createIcons() {} };"
        "document.addEventListener('DOMContentLoaded', () => {"
        "const style = document.createElement('style');"
        "style.textContent = 'nav .nav-links { display: flex !important; }"
        ".bg-slide { pointer-events: none !important; }"
        ".navbar { z-index: 10000 !important; }';"
        "document.head.append(style);"
        "});"
    )

    def skip_external_and_heavy_assets(route: object) -> None:
        url = route.request.url.lower().split("?", 1)[0]
        if url.startswith("https://") or url.endswith(SKIPPED_ASSET_SUFFIXES):
            route.abort()
        else:
            route.continue_()

    context.route("**/*", skip_external_and_heavy_assets)
    page = context.new_page()
    page.set_default_timeout(10000)
    try:
        yield page
    finally:
        context.close()


@pytest.fixture(scope="module")
def selenium_driver() -> Iterator[object]:
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": (
            "window.lucide = { createIcons() {} };"
            "document.addEventListener('DOMContentLoaded', () => {"
            "const style = document.createElement('style');"
            "style.textContent = 'nav .nav-links { display: flex !important; }"
            ".bg-slide { pointer-events: none !important; }"
            ".navbar { z-index: 10000 !important; }';"
            "document.head.append(style);"
            "});"
        )
    })
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd(
        "Network.setBlockedURLs",
        {
            "urls": [
                "https://*",
                "*.mov",
                "*.mp4",
                "*.zip",
            ]
        },
    )
    try:
        yield driver
    finally:
        driver.quit()
