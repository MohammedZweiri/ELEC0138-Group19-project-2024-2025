# Phishing Attack
## Process
1. Create a virtual environment

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Send a phishing email to all victims in victim_list.csv 
  - This requires a gmail account and corresponding app password within the sender.json file, communicate with Mohammed Zweiri for credentials collections 
uceemzw@ucl.ac.uk

```
cd attacks/phishing
python send_email.py
```
4. The user will recieve an email with a fake url close to the real one https://eiec0138-forum.0138019.xyz/, asking them to login to resolve some issues.
    - The live phishy website is https://eiec0138-forum.0138019.xyz/ , which is has been done via opening a terminal and run
    ```
    cd attacks/phishing/phishing_website/frontend
    npm install
    npm run dev -- --port 80 --host
    ```
    For the backend system, open another terminal and run
    ```
    cd attacks/phishing/phishing_website/backend
    python backend.py
    ```


5. If the user attempts to login, it will send a login request to phishing backend api.
    - Nothing will happen, however, the user's credential will be stored under a victim_info.txt file under attacks/phishing/backend. 
    - Saved usernames and passwords can be tried to login in the real website later.

## Phishing website
A website similar to the real one for demonstration purpose under https://eiec0138-forum.0138019.xyz/ (compared to the original https://elec0138-forum.0138019.xyz/)


## Mitigation

1. A Multi Layer Perceptron (MLP) neural network model has been developed detect if a url is phishing url via phishing_detection.py
    - This script loads the list of potential fake urls related to the real web server stored in URL_list.txt file.
    - Then, it iterates throught each url and provides the phishing probability. 
    - The training data and feature extractor is taken from https://github.com/vaibhavbichave/Phishing-URL-Detection/tree/master. 
    - The model is retrained via running
```
cd attacks/phishing/model
python training.py
```

2. To run the url test:
```
cd attacks/phishing
python phishing_detection.py
```

## 🔐 sender.json keys

| Variable               | Description                                          | Required |
| ---------------------- | ---------------------------------------------------- | :------: |
| `email` | SMTP sender emai  |    ✅      |
| `password` | GMAIL app password  |    ✅     |