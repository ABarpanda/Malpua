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

    message = f"Hello Novia \nYour Barida is here :\nLatitude: {latitude}\nLongitude: {longitude}\nTime: {timestamp}"
    # print(message)
    send_email("srutipriyadarshani13@gmail.com", "Barida's location", message)

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
