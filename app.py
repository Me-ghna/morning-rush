from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

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

@app.route("/")
def home():
    return "Bot is live 🚀"

@app.route("/bot", methods=["POST"])
def bot():
    phone = request.values.get("From")
    msg = request.values.get("Body", "").lower()
    response = MessagingResponse()

    if phone not in user_state:
        user_state[phone] = {"step": "start"}

    state = user_state[phone]

    # 🟢 STEP 1: SHOW MENU
    if state["step"] == "start":
        response.message(
            "🌅 *Morning Rush Menu*\n\n"
            "🥤 *Classic Juices*\n"
            "Orange ₹60\nPineapple ₹70\nWatermelon ₹50\nApple ₹70\nMosambi ₹60\n\n"
            "💪 *Health Juices*\n"
            "ABC ₹80\nGreen Detox ₹90\nCarrot Beetroot ₹70\n\n"
            "⚡ *Power Shots*\n"
            "Amla ₹40\nGinger Lemon ₹30\nHoney Lemon ₹30\n\n"
            "🔥 *Combos*\n"
            "Fitness Combo ₹110\nDetox Combo ₹120\nEnergy Combo ₹100\n\n"
            "👉 Type item name to order"
        )
        state["step"] = "item"

    # 🟢 STEP 2: ITEM SELECTION
    elif state["step"] == "item":
        if msg in menu:
            state["item"] = msg
            response.message("How many do you want?")
            state["step"] = "quantity"
        else:
            response.message("❌ Item not found. Please type correct name.")

    # 🟢 STEP 3: QUANTITY
    elif state["step"] == "quantity":
        if msg.isdigit():
            state["quantity"] = int(msg)
            response.message("📍 Please send your address")
            state["step"] = "address"
        else:
            response.message("Please enter a valid number")

    # 🟢 STEP 4: ADDRESS + BILL
    elif state["step"] == "address":
        state["address"] = msg

        price = menu[state["item"]]
        total = price * state["quantity"]

        response.message(
            f"✅ *Order Confirmed*\n\n"
            f"Item: {state['item']}\n"
            f"Qty: {state['quantity']}\n"
            f"Total: ₹{total}\n"
            f"Address: {state['address']}\n\n"
            f"⏰ Delivery: 6–9 AM\n"
            f"💰 Payment: UPI / Cash\n"
            f"👉 Pay: yourupi@bank"
        )

        user_state.pop(phone)

    return str(response)
