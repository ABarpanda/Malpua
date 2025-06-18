import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.text import MIMEText
import time
from dotenv import load_dotenv
import os

load_dotenv()

# === Firebase Admin SDK Init ===
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# === Email Setup ===
SENDER = "abarpanda05@gmail.com"
PASSWORD = f"{os.getenv('app_password')}"
RECEIVER = "subhranshu.1972@gmail.com"

def send_email_alert(data):
    subject = "📬 New Firebase Entry Alert"
    body = f"New data added: {data}"
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = RECEIVER
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, PASSWORD)
            server.send_message(msg)
        print("✅ Email sent for new entry!")
    except Exception as e:
        print("❌ Email error:", e)

# === Firestore Watch ===
def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == "ADDED":
            print(f"🔍 New document: {change.document.id}")
            send_email_alert(change.document.to_dict())

# === Set Up Listener ===
col_query = db.collection("alerts")  # Replace with your collection name
query_watch = col_query.on_snapshot(on_snapshot)

# Keep script running
print("👂 Listening for new Firestore entries...")
while True:
    time.sleep(60)
