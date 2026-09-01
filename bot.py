import os
import random
import time
import threading
import requests
from flask import Flask
from telebot import TeleBot, types

BOT_TOKEN = "8888661139:AAFluKA60FPKddBVI1WlZskX3s2W5W6i-XU" 
bot = TeleBot(BOT_TOKEN)
ADMIN_ID = 8852375598
RENDER_URL = "https://my-telegram-bot-wnyy.onrender.com"

CRYPTO_WALLETS = {
    "btc": {"name": "🪙 BTC", "address": "bc1pj9u898umy3r7fhgrq8w6nemvepcjr0pwl89z6nn66ghqzh9wz9nqudqsla"},
    "usdt": {"name": "💵 USDT", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "eth": {"name": "💎 ETH", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "sol": {"name": "🟣 SOL", "address": "H4cw8xf8A9pg6RTGBbAj2eobWM5HFNhxDKKroLQ1aEVq"}
}

inventory = {
    "ai": {
        "chatgpt_1m": {"name": "🤖 ChatGPT 1M", "price": 3.40, "stock": 5, "sold": 20, "image": "https://images.unsplash.com/photo-1677442136019-21780efad99a?w=600"},
        "claude_max": {"name": "🔥 Claude Max", "price": 14.50, "stock": 3, "sold": 15, "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600"}
    },
    "entertainment": {
        "spotify": {"name": "🎧 Spotify 1M", "price": 1.99, "stock": 10, "sold": 40, "image": "https://images.unsplash.com/photo-1614680376593-902f749f7ffc?w=600"}
    }
}

user_data = {}
admin_states = {}
recent_sales_ticker = "🔥 **Live Feed:** `Rahul` just purchased `ChatGPT 1M`!"

def fake_sales_ticker_updater():
    global recent_sales_ticker
    names = ["Rahul", "Aman", "Alex", "David", "Vikram"]
    products = ["ChatGPT 1M", "Claude Max", "Spotify 1M"]
    while True:
        time.sleep(random.randint(40, 80))
        recent_sales_ticker = f"🔥 **Live Feed:** `{random.choice(names)}` just purchased `{random.choice(products)}`!"

def get_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0}
    return user_data[user_id]

def auto_stock_updater():
    pass

def keep_alive():
    while True:
        time.sleep(300)
        try:
            requests.get(RENDER_URL)
        except:
            pass

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def get_main_menu():
    markup = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton("🤖 AI", callback_data="cat_ai")
    b2 = types.InlineKeyboardButton("🎬 ENT", callback_data="cat_entertainment")
    b3 = types.InlineKeyboardButton("💳 WALLET", callback_data="add_funds")
    b4 = types.InlineKeyboardButton("👤 PROFILE", callback_data="my_account")
    b5 = types.InlineKeyboardButton("📞 SUPPORT", url="https://t.me/ZhiGeAI")
    markup.add(b1, b2)
    markup.add(b3, b4)
    markup.add(b5)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = get_user(message.from_user.id)
    text = f"⚡ **WELCOME!** ⚡\n\n{recent_sales_ticker}\n💰 **BALANCE:** `${user['balance']:.2f}`"
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.send_message(message.chat.id, "✅ **PAYMENT PROOF RECEIVED.** PENDING ADMIN VERIFICATION.")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user = get_user(call.from_user.id)
    bot.answer_callback_query(call.id)
    
    if call.data == "main_menu":
        text = f"⚡ **MAIN MENU** ⚡\n\n{recent_sales_ticker}\n💰 **BALANCE:** `${user['balance']:.2f}`"
        try:
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=get_main_menu(), parse_mode="Markdown")
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=get_main_menu(), parse_mode="Markdown")
            
    elif call.data.startswith("cat_"):
        cat_key = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup()
        for key, item in inventory.get(cat_key, {}).items():
            btn = types.InlineKeyboardButton(f"{item['name']} | ${item['price']}", callback_data=f"item_{cat_key}_{key}")
            markup.add(btn)
        back_btn = types.InlineKeyboardButton("🔙 BACK", callback_data="main_menu")
        markup.add(back_btn)
        bot.edit_message_text("📌 **CHOOSE PRODUCT:**", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data.startswith("item_"):
        parts = call.data.split("_")
        cat_key, prod_key = parts[1], "_".join(parts[2:])
        item = inventory[cat_key].get(prod_key)
        markup = types.InlineKeyboardMarkup()
        buy_btn = types.InlineKeyboardButton("⚡ BUY 1x", callback_data=f"buy_{cat_key}_{prod_key}_1")
        back_btn = types.InlineKeyboardButton("🔙 BACK", callback_data=f"cat_{cat_key}")
        markup.add(buy_btn)
        markup.add(back_btn)
        bot.send_photo(call.message.chat.id, item['image'], caption=f"🏷️ {item['name']}\n💵 ${item['price']}", reply_markup=markup)

    elif call.data == "add_funds":
        markup = types.InlineKeyboardMarkup()
        for key, wallet in CRYPTO_WALLETS.items():
            btn = types.InlineKeyboardButton(wallet["name"], callback_data="tx_submitted")
            markup.add(btn)
        back_btn = types.InlineKeyboardButton("🔙 BACK", callback_data="main_menu")
        markup.add(back_btn)
        bot.edit_message_text("💳 **SELECT CRYPTO TO PAY:**", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "tx_submitted":
        bot.send_message(call.message.chat.id, "✍️ **PLEASE SEND YOUR TXID HERE:**", parse_mode="Markdown")
        
    elif call.data == "my_account":
        text = f"👤 **DASHBOARD:**\n💰 **BALANCE:** `${user['balance']:.2f}`"
        markup = types.InlineKeyboardMarkup()
        back_btn = types.InlineKeyboardButton("🔙 BACK", callback_data="main_menu")
        markup.add(back_btn)
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(timeout=60), daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    threading.Thread(target=fake_sales_ticker_updater, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
        
