import os
from google.cloud import firestore
from datetime import datetime, timedelta, timezone
import time
import pytz
from send_email import send_email
import json
from google.oauth2 import service_account

creds_dict = json.loads(os.environ["FIREBASE_CREDS_JSON"])
creds = service_account.Credentials.from_service_account_info(creds_dict)
db = firestore.Client(credentials=creds)

local_tz = pytz.timezone("Asia/Kolkata")

def load_last_timestamp():
    try:
        with open("last_checked.txt", "r") as f:
            ts = f.read().strip()
            naive_dt = datetime.fromisoformat(ts)
            return local_tz.localize(naive_dt)  # make it aware in local timezone
    except:
        return datetime.now(local_tz) - timedelta(minutes=10)

def save_last_timestamp(ts):
    with open("last_checked.txt", "w") as f:
        f.write(ts.replace(tzinfo=None).isoformat())

def check_new_alerts(receiver_email="abarpanda05@gmail.com"):
    last_ts = load_last_timestamp()
    print(f"Checking for alerts since: {last_ts.isoformat()}")

    query = db.collection("locations") \
          .where("timestamp", ">", last_ts.astimezone(timezone.utc)) \
          .order_by("timestamp", direction=firestore.Query.DESCENDING) \
          .limit(1) \
          .stream()

    new_ts = last_ts
    for doc in query:
        data = doc.to_dict()
        print("data =", data)

        # Pull timestamp from Firestore
        doc_ts = data.get("timestamp")
        if not isinstance(doc_ts, datetime):
            continue

        # Ensure doc_ts is UTC-aware
        if doc_ts.tzinfo is None:
            doc_ts = doc_ts.replace(tzinfo=timezone.utc)

        # Convert doc_ts to local time for comparison and display
        local_doc_ts = doc_ts.astimezone(local_tz)

        # Use local time for email
        email = receiver_email
        subject = "Location update of Amritanshu Barpanda"
        time_at_location = data["timestamp"] + timedelta(hours=5,minutes=30)
        message = f"Hey my location is \n\nLongitude = {data["longitude"]} \nLatitude = {data["latitude"]} \nat {time_at_location.strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"New alert: {email} - {subject}")
        send_email(email, subject, message)

        # Compare in local time
        if local_doc_ts > new_ts:
            new_ts = local_doc_ts

    save_last_timestamp(new_ts)

if __name__ == "__main__":
    check_new_alerts()
