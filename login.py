from playwright.sync_api import sync_playwright

def manual_login_and_save_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()

        # Set US locale
        page.goto("https://www.nike.com/sg/launch")

        print("🟢 Please log in manually. After login completes, close the browser.")
        page.wait_for_timeout(60000)  # Wait up to 60 seconds for you to log in manually

        context.storage_state(path="auth.json")
        print("✅ Session saved as auth.json")
        browser.close()
