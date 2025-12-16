from playwright.sync_api import sync_playwright

def verify_new_events_design():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Verify New Events Page Layout
        print("Verifying New Events Timeline Layout...")
        page.goto("http://localhost:8000/events.html")
        page.wait_for_selector("#timeline-events > div") # Wait for timeline items

        # Take full page screenshot
        page.screenshot(path="verification/events_timeline.png", full_page=True)
        print("Events timeline screenshot saved.")

        # Test Filters
        print("Testing Filter Interaction...")
        page.click("button[data-filter='meeting']")
        page.wait_for_timeout(500) # Wait for animation/render
        page.screenshot(path="verification/events_filtered_meeting.png", full_page=True)
        print("Filtered screenshot saved.")

        browser.close()

if __name__ == "__main__":
    verify_new_events_design()
