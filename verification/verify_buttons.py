from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8000/news/2025-12-15-fighting-for-higher-education.html")

        # Scroll to bottom
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # Take screenshot of the bottom area
        # We can target the main article or the footer area
        page.screenshot(path="verification/bottom_buttons.png")

        browser.close()

if __name__ == "__main__":
    run()
