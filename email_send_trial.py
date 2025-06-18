import functions_framework
from send_email import send_email

@functions_framework.cloud_event
def on_alert_created(cloud_event):
    # Firestore event structure
    data = cloud_event.data
    value = data.get("value", {})
    fields = value.get("fields", {})

    # Extract Firestore document fields
    email = fields.get("email", {}).get("stringValue", "")
    subject = fields.get("subject", {}).get("stringValue", "Alert Triggered")
    message = fields.get("message", {}).get("stringValue", "New alert generated.")

    print(f"Received new alert document: to={email}, subject={subject}")
    if email:
        send_email(email, subject, message)
    return None
    
    # data = cloud_event.data
    # print(data)