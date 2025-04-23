# Backend API

This directory contains the Flask backend for the ELEC0138 Forum application.

## ⚙️ Installation

1. Create a virtual environment

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the application by add the environment variables to the `.env` file 

4. Run the application:
   ```bash
   python backend.py
   ```

## 🐋 Deployment

1.  Build the Docker image:
    ```bash
    docker build -t your-image-name .
    ```
2.  Run the Docker container:
    ```bash
    docker run -p <host-port>:<container-port> \
      -e RECAPTCHA_SECRET_KEY=<your_recaptcha_secret_key> \
      -e <VAR_NAME>=<VAR_VALUE> \
      your-image-name
    ```

## 🔐 Environment Variables

| Variable               | Description                                          | Required |
| ---------------------- | ---------------------------------------------------- | :------: |
| `MYSQL_HOST`           | Hostname or IP address of the MySQL database server. |    ❌     |
| `MYSQL_USER`           | Username for connecting to the MySQL database.       |    ❌     |
| `MYSQL_PASSWORD`       | Password for connecting to the MySQL database.       |    ❌     |
| `MYSQL_DB`             | Name of the MySQL database to use.                   |    ❌     |
| `JWT_SECRET_KEY`       | Secret key used for signing JWT tokens.              |    ❌     |
| `RECAPTCHA_SECRET_KEY` | Google reCAPTCHA v3 secret key for form validation.  |    ✅     |
