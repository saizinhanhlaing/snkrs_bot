from playwright.sync_api import sync_playwright
import json

def normalize_same_site(value):
    if value in ["Strict", "Lax", "None"]:
        return value
    return "Lax"

def load_cookies_into_context(context, cookies):
    context.add_cookies([
        {
            "name": c["name"],
            "value": c["value"],
            "domain": c.get("domain", ".nike.com"),
            "path": c.get("path", "/"),
            "secure": c.get("secure", False),
            "httpOnly": c.get("httpOnly", False),
            "sameSite": normalize_same_site(c.get("sameSite")),
            "expires": c.get("expirationDate", -1) or -1,
        }
        for c in cookies if "nike.com" in c.get("domain", "")
    ])

def simulate_join_draw(product_url):
    with open("cookies.json", "r") as f:
        cookies = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        context = browser.new_context()
        load_cookies_into_context(context, cookies)

        page = context.new_page()
        page.goto(product_url)

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        print("🔍 Looking for Join Draw button...")

        try:
            button = page.query_selector("button:has-text('Join Draw')")
            if button:
                print("✅ 'Join Draw' button found.")
                # button.click()  # You can enable this to simulate clicking
            else:
                print("❌ No 'Join Draw' button on this page.")
        except Exception as e:
            print(f"⚠️ Error while looking for Join button: {e}")

        page.wait_for_timeout(5000)
        browser.close()
