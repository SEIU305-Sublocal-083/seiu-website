from playwright.sync_api import sync_playwright

def verify_updates():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Verify Events Page - Accordion
        print("Verifying Events Accordion...")
        page.goto("http://localhost:8000/events.html")
        page.wait_for_selector("#timeline-events > div")
        page.screenshot(path="verification/events_accordion_collapsed.png", full_page=True)

        # Verify Header Navigation on Nested Pages
        # We need to find a nested page to test. Using events/2026-01-07-CAT-Meeting.html from the list above.
        print("Verifying Nested Page Header...")
        page.goto("http://localhost:8000/events/2026-01-07-CAT-Meeting.html")
        page.wait_for_selector("nav")

        # Click "News" from the nested page and verify we go to /news.html (not /events/news.html)
        print("Testing Navigation from Nested Page...")
        with page.expect_navigation(url="http://localhost:8000/news.html"):
            page.click("nav a[href='/news.html']")

        print("Navigation Successful!")
        page.screenshot(path="verification/nested_navigation_success.png")

        browser.close()

if __name__ == "__main__":
    verify_updates()
