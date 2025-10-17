from playwright.sync_api import Page, expect
import os

def test_leadership_page_updates(page: Page):
    """
    This test verifies the following updates on the leadership page:
    1. The "Elected Officers" section appears before the "Appointed Chairs" section.
    2. The "Union Stewards" section is a static list.
    3. The stewards are visible.
    """
    # 1. Arrange: Go to the leadership page.
    page.goto(f"file://{os.getcwd()}/leadership.html")

    # 2. Assert: Check the order of the sections.
    all_sections = page.locator("main > section")
    expect(all_sections.nth(0)).to_have_id("officers")
    expect(all_sections.nth(1)).to_have_id("chairs")
    expect(all_sections.nth(2)).to_have_id("stewards")

    # 3. Assert: Check for the presence of the stewards.
    expect(page.get_by_text("Patrick Breshears")).to_be_visible()
    expect(page.get_by_text("Richard Keuneke")).to_be_visible()
    expect(page.get_by_text("Anne Gross")).to_be_visible()
    expect(page.get_by_text("Jax Johnson")).to_be_visible()
    expect(page.get_by_text("Russ Born")).to_be_visible()
    expect(page.get_by_text("Tracey Jastad")).to_be_visible()
    expect(page.get_by_text("Andrew Struthers")).to_be_visible()

    # 4. Screenshot: Capture the final result for visual verification.
    screenshot_path = "jules-scratch/verification/verification.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")