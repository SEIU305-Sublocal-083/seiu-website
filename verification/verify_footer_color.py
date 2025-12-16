from playwright.sync_api import sync_playwright

def verify_footer_colors():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Verify News Page Footer Colors
        print("Verifying News Page Footer Colors...")
        page.goto("http://localhost:8000/news.html")

        # Select a footer link
        link = page.locator("footer a[href='/about.html']")

        # Check computed style
        color = link.evaluate("element => window.getComputedStyle(element).color")
        print(f"Computed color of footer link: {color}")

        # rgb(209, 213, 219) is roughly gray-300 (#D1D5DB)
        # rgb(0, 0, 0) would be black

        if color == "rgb(209, 213, 219)":
            print("SUCCESS: Footer link color is gray-300.")
        else:
            print(f"WARNING: Footer link color is {color}. Please verify visually.")

        page.screenshot(path="verification/footer_contrast_check.png")
        browser.close()

if __name__ == "__main__":
    verify_footer_colors()
