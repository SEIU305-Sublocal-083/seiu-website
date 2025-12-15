from playwright.sync_api import sync_playwright, expect
import time

def verify_button_style():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the news article
        print("Navigating to news article...")
        page.goto("http://localhost:8000/news/2025-12-15-fighting-for-higher-education.html")

        # Wait for content to load
        expect(page.locator("h1")).to_have_text("Fighting for Higher Education")

        # Find the button
        button = page.locator("a.btn-primary")

        # Take a screenshot of the button specifically
        print("Taking screenshot of button...")
        # Scroll to button
        button.scroll_into_view_if_needed()
        time.sleep(0.5) # Wait for potential animations
        page.screenshot(path="verification/petition_button.png", clip=button.bounding_box())

        # Also take a wider shot
        page.screenshot(path="verification/news_page_with_button.png")

        browser.close()
        print("Verification complete.")

if __name__ == "__main__":
    verify_button_style()
