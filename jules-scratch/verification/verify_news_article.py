from playwright.sync_api import sync_playwright, Page, expect
import os

def run_test(page: Page):
    """
    This test verifies that the new news article is displayed correctly on the news page.
    """
    # 1. Arrange: Go to the news page.
    page.goto(f"file://{os.getcwd()}/news.html")

    # 2. Act: Scroll to the recent articles section.
    page.locator("#recent-articles").scroll_into_view_if_needed()

    # 3. Assert: Check that the new article is present.
    # We use get_by_text to find the new article's title.
    expect(page.get_by_text("November COLA Increase Coming Soon!")).to_be_visible()

    # 4. Screenshot: Capture the final result for visual verification.
    page.screenshot(path="jules-scratch/verification/verification.png")

    # 5. Act: Click on the new article to navigate to its page.
    page.get_by_text("November COLA Increase Coming Soon!").click()

    # 6. Assert: Check that the new article's page is loaded correctly.
    expect(page).to_have_title("News: November COLA Increase Coming Soon! - SEIU Local 503, OSU")
    expect(page.get_by_text("Our Next COLA Increase is Coming!")).to_be_visible()

    # 7. Screenshot: Capture the final result for visual verification.
    page.screenshot(path="jules-scratch/verification/article_page.png")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    run_test(page)
    browser.close()