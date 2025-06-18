import os
from google.cloud import firestore
from datetime import datetime, timedelta,timezone
import time
import pytz
from send_email import send_email  # you define this

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccountKey.json"
db = firestore.Client()
def load_last_timestamp():
    try:
        with open("last_checked.txt", "r") as f:
            ts = f.read().strip()
            return datetime.fromisoformat(ts)
    except:
        return datetime.now() - timedelta(minutes=10)

def save_last_timestamp(ts):
    with open("last_checked.txt", "w") as f:
        f.write(ts.isoformat())

def check_new_alerts():
    last_ts = load_last_timestamp()
    print(f"Checking for alerts since: {last_ts.isoformat()}")

    query = db.collection("locations") \
          .where("timestamp", ">", last_ts) \
          .order_by("timestamp", direction=firestore.Query.DESCENDING) \
          .limit(1) \
          .stream()
    print(query)

    new_ts = last_ts
    for doc in query:
        data = doc.to_dict()
        print("data=",data)
        email = "abarpanda05@gmail.com"
        subject = "Please ignore"
        message = data.get("timestamp", "No message")
        print(message)

        print(f"New alert: {email} - {subject}")
        send_email(email, subject, str(message))

        # ... inside your loop or query:
        doc_ts = data.get("timestamp")

        if isinstance(doc_ts, datetime):
            # Make doc_ts timezone-aware if it is naive
            if doc_ts.tzinfo is None:
                doc_ts = doc_ts.replace(tzinfo=timezone.utc)

            if doc_ts > new_ts:
                new_ts = doc_ts

    save_last_timestamp(new_ts)

if __name__ == "__main__":
    check_new_alerts()
