from flask import Flask, request, jsonify
import datetime
from send_email import send_email

# Optional: import your email function here
# from send_email import send_email

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask Location Server is running."

@app.route("/location", methods=["POST"])
def receive_location():
    data = request.json
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    timestamp = data.get("timestamp", datetime.datetime.now())

    message_novia = f"Hello Novia \nBarida is here :\nLatitude: {latitude}\nLongitude: {longitude}\nTime: {timestamp}"
    message_parents = f"Rishu's location update: \nLatitude: {latitude}\nLongitude: {longitude}\nTime: {timestamp}"
    send_email("srutipriyadarshani13@gmail.com", "Barida's location", message_novia)
    send_email("ssekhar72@yahoo.com", "Rishu's location", message_parents)

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
