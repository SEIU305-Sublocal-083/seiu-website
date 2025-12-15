from playwright.sync_api import sync_playwright

def verify_updates():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Verify News Page
        print("Verifying News Page...")
        page.goto("http://localhost:8000/news.html")
        page.wait_for_selector("#articles-grid > div") # Wait for articles to load
        page.screenshot(path="verification/news_page.png", full_page=True)
        print("News page screenshot saved.")

        # Verify Events Page
        print("Verifying Events Page...")
        page.goto("http://localhost:8000/events.html")
        page.wait_for_selector("#upcoming-events-container > div") # Wait for events to load
        page.screenshot(path="verification/events_page.png", full_page=True)
        print("Events page screenshot saved.")

        browser.close()

if __name__ == "__main__":
    verify_updates()
