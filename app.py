from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

user_state = {}

@app.route("/bot", methods=["POST"])
def bot():
    phone = request.values.get("From")
    msg = request.values.get("Body", "").lower()
    response = MessagingResponse()

    if phone not in user_state:
        user_state[phone] = {"step": "start"}

    state = user_state[phone]

    if state["step"] == "start":
        response.message(
            "Welcome to Morning Rush 🌅\n\n"
            "Menu:\n🍊 Orange\n🍍 Pineapple\n🥕 ABC\n🥬 Green Detox\n\n"
            "Type juice name to order"
        )
        state["step"] = "juice"

    elif state["step"] == "juice":
        state["juice"] = msg
        response.message("How many do you want?")
        state["step"] = "quantity"

    elif state["step"] == "quantity":
        state["quantity"] = msg
        response.message("Please send your address 📍")
        state["step"] = "address"

    elif state["step"] == "address":
        state["address"] = msg
        response.message(
            f"Order Confirmed ✅\n\n"
            f"Juice: {state['juice']}\n"
            f"Quantity: {state['quantity']}\n"
            f"Address: {state['address']}\n\n"
            f"Delivery: 6–9 AM"
        )
        user_state.pop(phone)

    return str(response)
