from playwright.sync_api import sync_playwright, expect
import time

def verify_changes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create a fresh context to ensure sessionStorage is empty
        context = browser.new_context()
        page = context.new_page()

        # Navigate to homepage
        print("Navigating to homepage...")
        page.goto("http://localhost:8000/index.html")

        # Wait for modal to appear (it has a 1.5s delay)
        print("Waiting for modal...")
        modal = page.locator("#bargaining-survey-modal")
        # Ensure it's not hidden
        expect(modal).not_to_have_class("hidden", timeout=5000)

        # Take screenshot of the modal
        print("Taking screenshot of modal...")
        time.sleep(2) # Wait for animation
        page.screenshot(path="verification/modal.png")

        # Verify content of the modal
        print("Verifying modal content...")
        expect(page.locator("#modal-title")).to_have_text("Fighting for Higher Education")
        expect(page.locator("#modal-btn-done")).to_have_text("Read the Article & Sign Petition")

        # Click the link
        print("Clicking the link...")
        with page.expect_navigation():
            page.locator("#modal-btn-done").click()

        # Verify we are on the news page
        print("Verifying news page...")
        expect(page).to_have_url("http://localhost:8000/news/2025-12-15-fighting-for-higher-education.html")
        expect(page.locator("h1")).to_have_text("Fighting for Higher Education")

        # Take screenshot of the article
        print("Taking screenshot of article...")
        page.screenshot(path="verification/news_article.png")

        browser.close()
        print("Verification complete.")

if __name__ == "__main__":
    verify_changes()
