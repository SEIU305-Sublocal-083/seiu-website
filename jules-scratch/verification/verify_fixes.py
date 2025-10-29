from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    # Verify the main news page
    page.goto("http://localhost:8000/news.html")
    page.wait_for_selector("#articles-grid .bg-white") # Wait for articles to be loaded by JS
    page.screenshot(path="jules-scratch/verification/news-page-final-fix.png")

    # Verify the author change on an article page
    page.goto("http://localhost:8000/news/2025-10-27-bowling-striking-success.html")
    page.screenshot(path="jules-scratch/verification/article-page-final-fix.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
