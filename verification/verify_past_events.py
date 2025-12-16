from playwright.sync_api import sync_playwright

def verify_past_events_links():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to events page
        print("Navigating to Events Page...")
        page.goto("http://localhost:8000/events.html")

        # Click "View Past Events" to reveal them
        print("Opening Past Events...")
        page.click("#toggle-past-events")

        # Wait for toggle animation/visibility
        # The container #past-events-wrapper should lose the 'hidden' class
        page.wait_for_selector("#past-events-wrapper:not(.hidden)")

        # Check if there are links in the past events wrapper
        # We expect at least one link if there are past events
        links = page.query_selector_all("#past-events-wrapper a")

        if len(links) > 0:
            print(f"Found {len(links)} clickable links in past events.")
            # Verify the first link has an href
            first_href = links[0].get_attribute("href")
            print(f"First link href: {first_href}")

            if first_href and first_href != "#":
                print("SUCCESS: Past events are linked.")
            else:
                print("WARNING: Link href seems empty or placeholder.")
        else:
            print("ERROR: No links found in past events section.")

        page.screenshot(path="verification/past_events_links.png")
        browser.close()

if __name__ == "__main__":
    verify_past_events_links()
