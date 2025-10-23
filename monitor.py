from playwright.sync_api import sync_playwright

def fetch_snkrs_drops():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(user_agent="Mozilla/5.0 ...")
        page = context.new_page()
        page.goto("https://www.nike.com/sg/launch")

        try:
            page.click("button:has-text('Accept All')", timeout=5000)
        except:
            pass

        page.wait_for_selector("a[href*='/launch/t/']")

        links = page.query_selector_all("a[href*='/launch/t/']")
        for link in links:
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            if href:
                print(f"🔗 {text} — https://www.nike.com{href}")

        browser.close()