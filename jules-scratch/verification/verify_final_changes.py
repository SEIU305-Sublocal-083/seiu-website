
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8000/news.html")
        page.screenshot(path="jules-scratch/verification/news-page-final.png")
        page.goto("http://localhost:8000/news/2025-10-27-bowling-striking-success.html")
        page.screenshot(path="jules-scratch/verification/article-page-final.png")
        browser.close()

if __name__ == "__main__":
    run()
