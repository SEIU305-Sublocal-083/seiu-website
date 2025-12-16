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

        # Expand first event
        page.click("#timeline-events summary")
        page.wait_for_timeout(500)
        page.screenshot(path="verification/events_accordion_expanded.png", full_page=True)
        print("Events screenshots saved.")

        # Verify Header Active State on News
        print("Verifying News Header Active State...")
        page.goto("http://localhost:8000/news.html")
        page.wait_for_selector("nav")
        page.screenshot(path="verification/news_header_active.png")

        # Verify Header Active State on About (random page)
        print("Verifying About Header Active State...")
        page.goto("http://localhost:8000/about.html")
        page.wait_for_selector("nav")
        page.screenshot(path="verification/about_header_active.png")

        browser.close()

if __name__ == "__main__":
    verify_updates()
