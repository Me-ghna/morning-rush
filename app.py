from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# 🧠 Store user progress
user_state = {}

# 🧾 MENU DATA
menu = {
    "orange": 60,
    "pineapple": 70,
    "watermelon": 50,
    "apple": 70,
    "mosambi": 60,
    "abc": 80,
    "green": 90,
    "carrot beetroot": 70,
    "amla": 40,
    "ginger lemon": 30,
    "honey lemon": 30,
    "fitness combo": 110,
    "detox combo": 120,
    "energy combo": 100
}

# 🟢 Home route (just to check server)
@app.route("/")
def home():
    return "Bot is live 🚀"

# 🟢 WhatsApp bot route
@app.route("/bot", methods=["POST"])
def bot():
    phone = request.values.get("From")
    msg = request.values.get("Body", "").lower().strip()
    response = MessagingResponse()

    # Initialize user
    if phone not in user_state:
        user_state[phone] = {"step": "start"}

    state = user_state[phone]

    # 🟢 STEP 1: SHOW MENU
    if state["step"] == "start":
        response.message(
            "🌅 *Welcome to Morning Rush!*\n"
            "Fresh Energy. Every Morning ☀️\n\n"

            "📋 *MENU (250ml unless mentioned)*\n\n"

            "🥤 *Classic Juices*\n"
            "🍊 Orange – ₹60\n"
            "🍍 Pineapple – ₹70\n"
            "🍉 Watermelon – ₹50\n"
            "🍎 Apple – ₹70\n"
            "🍋 Mosambi – ₹60\n\n"

            "💪 *Health & Fitness*\n"
            "🥕 ABC (Apple+Beetroot+Carrot) – ₹80\n"
            "🥬 Green Detox – ₹90\n"
            "🥕 Carrot Beetroot – ₹70\n\n"

            "⚡ *Power Shots (100ml)*\n"
            "🍏 Amla – ₹40\n"
            "🍋 Ginger Lemon – ₹30\n"
            "🍯 Honey Lemon – ₹30\n\n"

            "🔥 *Combos*\n"
            "Fitness Combo(ABC+Amla Shot) – ₹110\n"
            "Detox Combo(Green Juice+Ginger Shot) – ₹120\n"
            "Energy Combo(Orange+Pineapple) – ₹100\n\n"

            "👉 *What would you like to order?*\n"
            "Type item name (example: *orange*)"
        )
        state["step"] = "item"

    # 🟢 STEP 2: ITEM SELECTION
    elif state["step"] == "item":
        if msg in menu:
            state["item"] = msg
            response.message(
                f"👍 Great choice! *{msg.title()}*\n\n"
                "👉 How many *glasses/units* do you want?\n"
                "Example: 1, 2, 3..."
            )
            state["step"] = "quantity"
        else:
            response.message(
                "❌ Item not found.\n"
                "Please type correct name (example: orange, abc, fitness combo)"
            )

    # 🟢 STEP 3: QUANTITY
    elif state["step"] == "quantity":
        if msg.isdigit():
            state["quantity"] = int(msg)
            response.message(
                f"👌 Noted: *{state['quantity']} x {state['item'].title()}*\n\n"
                "📍 Please send your *full delivery address*\n"
                "(House no, street, landmark)"
            )
            state["step"] = "address"
        else:
            response.message("❌ Please enter a valid number (example: 1, 2, 3)")

    # 🟢 STEP 4: ADDRESS + BILL
    elif state["step"] == "address":
        state["address"] = msg

        price = menu[state["item"]]
        total = price * state["quantity"]

        response.message(
            f"🎉 *Order Confirmed!*\n\n"

            f"🧾 *Order Details*\n"
            f"Item: {state['item'].title()}\n"
            f"Quantity: {state['quantity']}\n"
            f"Total: ₹{total}\n\n"

            f"📍 Address:\n{state['address']}\n\n"

            f"⏰ Delivery: *6–9 AM*\n"
            f"🕙 Order before: *10 PM*\n\n"

            f"💰 Payment: UPI / Cash\n"
            f"👉 UPI: yourupi@bank\n\n"

            f"🙏 Thank you for choosing *Morning Rush!*"
        )

        # Reset user after order
        user_state.pop(phone)

    return str(response)

# Run app
if __name__ == "__main__":
    app.run()
