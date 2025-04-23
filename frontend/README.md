# Frontend

This directory contains the VueJs frontend for the ELEC0138 Forum application.

## ⚙️ Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Configure the application by add the environment variables to the `.env` file 

3. Run the application:
   ```bash
   npm run dev -- --port 80 --host
   ```


## 🔐 Environment Variables

| Variable               | Description                                          | Required |
| ---------------------- | ---------------------------------------------------- | :------: |
| `VITE_BASE_URL` | Website's backend server  |    ❌     |
| `VITE_SITE_KEY` | Google reCAPTCHA v3 site key for token generattion.  |    ✅     |

