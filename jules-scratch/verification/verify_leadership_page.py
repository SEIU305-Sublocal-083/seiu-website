from playwright.sync_api import Page, expect
import os

def test_leadership_page_updates(page: Page):
    """
    This test verifies the following updates on the leadership page:
    1. The "Appointed Chairs" section has a centered card.
    2. The "Union Stewards" section is a dropdown that can be expanded.
    3. The stewards are visible after expanding the dropdown.
    """
    # 1. Arrange: Go to the leadership page.
    page.goto(f"file://{os.getcwd()}/leadership.html")

    # 2. Assert: Check that the "Appointed Chairs" card is centered.
    appointed_chairs_section = page.locator("section#chairs")
    expect(appointed_chairs_section.locator("> div")).to_have_class("flex justify-center")

    # 3. Act: Click the summary to expand the "Union Stewards" dropdown.
    stewards_summary = page.get_by_text("Union Stewards")
    stewards_summary.click()

    # 4. Assert: Check for the presence of the new stewards after expansion.
    expect(page.get_by_text("Patrick Breshears")).to_be_visible()
    expect(page.get_by_text("Richard Keuneke")).to_be_visible()
    expect(page.get_by_text("Anne Gross")).to_be_visible()
    expect(page.get_by_text("Jax Johnson")).to_be_visible()
    expect(page.get_by_text("Russ Born")).to_be_visible()
    expect(page.get_by_text("Tracey Jastad")).to_be_visible()
    expect(page.get_by_text("Andrew Struthers")).to_be_visible()

    # 5. Screenshot: Capture the final result for visual verification.
    screenshot_path = "jules-scratch/verification/verification.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")