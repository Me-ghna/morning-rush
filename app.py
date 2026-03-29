from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/")
def home():
    return "Morning Rush Bot is Running 🚀"

@app.route("/bot", methods=["POST"])
def bot():
    msg = request.values.get("Body", "").lower()
    response = MessagingResponse()

    if "hi" in msg or "hello" in msg:
        response.message(
            "Welcome to Morning Rush 🌅\n\n"
            "Menu:\n🍊 Orange\n🍍 Pineapple\n🥕 ABC\n🥬 Green Detox\n\n"
            "Send: Juice + Quantity + Address"
        )

    elif "orange" in msg or "pineapple" in msg:
        response.message("Got it! Please send your address 📍")

    elif "address" in msg:
        response.message("Your total is ₹100\nPay via UPI: yourupi@bank")

    else:
        response.message("Please send proper order 😊")

    return str(response)

if __name__ == "__main__":
    app.run()
