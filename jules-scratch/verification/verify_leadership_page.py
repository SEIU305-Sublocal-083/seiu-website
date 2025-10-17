from playwright.sync_api import Page, expect
import os

def test_leadership_page_stewards_and_officers_section(page: Page):
    """
    This test verifies that the Stewards section on the leadership page
    is correctly formatted and displays the new members, and that Gino Ballardo
    is in the Elected Officers section.
    """
    # 1. Arrange: Go to the leadership page.
    # The file is local, so we use the file:// protocol.
    page.goto(f"file://{os.getcwd()}/leadership.html")

    # 2. Assert: Check for the new Stewards section title.
    stewards_title = page.get_by_role("heading", name="Union Stewards")
    expect(stewards_title).to_be_visible()

    # 3. Assert: Check for the presence of the new stewards.
    expect(page.get_by_text("Patrick Breshears")).to_be_visible()
    expect(page.get_by_text("Richard Keuneke")).to_be_visible()
    expect(page.get_by_text("Anne Gross")).to_be_visible()
    expect(page.get_by_text("Jax Johnson")).to_be_visible()
    expect(page.get_by_text("Russ Born")).to_be_visible()
    expect(page.get_by_text("Tracey Jastad")).to_be_visible()
    expect(page.get_by_text("Andrew Struthers")).to_be_visible()

    # 4. Assert: Ensure Richard Marucha is not present.
    expect(page.get_by_text("Richard Marucha")).not_to_be_visible()

    # 5. Assert: Check for Gino Ballardo in the Elected Officers section.
    elected_officers_section = page.locator("section#officers")
    expect(elected_officers_section.get_by_text("Gino Ballardo")).to_be_visible()

    # 6. Screenshot: Capture the final result for visual verification.
    screenshot_path = "jules-scratch/verification/verification.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")