from playwright.sync_api import sync_playwright

def verify_visuals():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Verify Events Page
        print("Verifying Events Page Footer...")
        page.goto("http://localhost:8000/events.html")
        page.wait_for_selector("footer")
        # Check for specific "old footer" content (e.g. 4 columns, quick links)
        content = page.content()
        if "Quick Links" in content and "Adams Hall" in content:
             print("SUCCESS: Events page has the old footer content.")
        else:
             print("ERROR: Events page footer might be incorrect.")

        page.screenshot(path="verification/events_final_footer.png", full_page=True)

        # Verify News Page
        print("Verifying News Page Footer...")
        page.goto("http://localhost:8000/news.html")
        page.wait_for_selector("footer")
        content = page.content()
        if "Quick Links" in content and "Adams Hall" in content:
             print("SUCCESS: News page has the old footer content.")
        else:
             print("ERROR: News page footer might be incorrect.")

        page.screenshot(path="verification/news_final_footer.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    verify_visuals()
