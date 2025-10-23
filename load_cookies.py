import json
from playwright.sync_api import sync_playwright

def normalize_same_site(value):
    if value in ["Strict", "Lax", "None"]:
        return value
    return "Lax"  # Default fallback

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

def launch_authenticated_nike_session():
    with open("cookies.json", "r") as f:
        cookies = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        load_cookies_into_context(context, cookies)

        page = context.new_page()
        page.goto("https://www.nike.com/sg/launch")

        page.wait_for_timeout(5000)
        print("✅ Nike page loaded with real browser cookies.")
        browser.close()

if __name__ == "__main__":
    launch_authenticated_nike_session()
