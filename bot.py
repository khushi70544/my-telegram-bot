import os
import random
import time
import threading
from telebot import TeleBot, types

# Bot Token
BOT_TOKEN = "8888661139:AAFDzpjwmNDwcEe9-KNLC7hZnAnuZQd7DYQ"
bot = TeleBot(BOT_TOKEN)

# Dynamic Inventory Data - Updated Prices & Plans
inventory = {
    "chatgpt_1m": {"name": "ChatGPT Plus 1 Month", "price": 3.00, "stock": 5, "sold": 27},
    "chatgpt_6m": {"name": "ChatGPT Plus 6 Month", "price": 5.50, "stock": 5, "sold": 27},
    "spotify": {"name": "Spotify Premium 1 Month", "price": 0.50, "stock": 5, "sold": 27},
    "netflix": {"name": "Netflix Premium 1 Month", "price": 0.80, "stock": 5, "sold": 27},
    "grok": {"name": "Grok AI Premium 1 Month", "price": 4.85, "stock": 5, "sold": 27},
    "deepseek": {"name": "DeepSeek Pro 1 Month", "price": 12.00, "stock": 5, "sold": 27}
}

# User Balances & Registered Users Set
user_data = {}
registered_users = set()

def get_user(user_id, name):
    registered_users.add(user_id)
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0, "state": None, "selected_prod": None}
    return user_data[user_id]

# Broadcast function to all registered users
def broadcast_to_users(msg_text):
    for user_id in list(registered_users):
        try:
            bot.send_message(user_id, msg_text, parse_mode="Markdown")
        except Exception:
            pass

# Automated Inventory Manager for All Products
def multi_product_inventory_manager():
    # PHASE 1: Initial 10-Minute Rush (Stock 5 to 0)
    time.sleep(600) # Wait 10 mins
    for key in inventory:
        if inventory[key]["stock"] > 0:
            inventory[key]["sold"] += inventory[key]["stock"]
            inventory[key]["stock"] = 0

    # PHASE 2 & 3: Out of Stock Notification -> 30 Min Delay -> Restock Loop
    while True:
        # Phase 2: Send Out of Stock Alert
        for key, item in inventory.items():
            if item["stock"] <= 0:
                out_of_stock_msg = (
                    "⚠️ **OUT OF STOCK!**\n\n"
                    f"📦 **{item['name']}** is currently completely sold out!\n\n"
                    f"📊 **Total Sold:** `{item['sold']}`\n"
                )
                broadcast_to_users(out_of_stock_msg)
        
        # Phase 3: Wait 30 mins before restocking
        time.sleep(1800) 
        
        # Restock to 5 and send alert
        for key, item in inventory.items():
            item["stock"] = 5
            restock_msg = (
                "✅ **RESTOCK ALERT!**\n\n"
                f"📦 **{item['name']}** is back in stock!\n"
                f"🛒 **Available:** `5`\n"
            )
            broadcast_to_users(restock_msg)

# /start Command Handler with Premium Menu & Buttons
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    get_user(user_id, name)
    
    welcome_text = (
        f"👋 **Welcome, {name}!**\n\n"
        "🔥 **Premium Digital Store & Services Bot**\n"
        "Choose an option below to browse products, check your balance, or manage your account."
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🛍️ Browse Products", callback_data="browse_shop"),
        types.InlineKeyboardButton("👤 My Account", callback_data="my_account"),
        types.InlineKeyboardButton("💳 Add Funds", callback_data="add_funds"),
        types.InlineKeyboardButton("📞 Support", url="https://t.me/your_support_username")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# Callback Query Handlers for Interactive Buttons
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    user = get_user(user_id, call.from_user.first_name)
    
    if call.data == "browse_shop":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, item in inventory.items():
            status = f"🟢 Stock: {item['stock']}" if item['stock'] > 0 else "🔴 Out of Stock"
            btn_text = f"{item['name']} - ${item['price']:.2f} ({status})"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"buy_{key}"))
        
        markup.add(types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu"))
        bot.edit_message_text("📦 **Available Premium Products:**\nSelect any item to purchase:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "my_account":
        account_text = (
            f"👤 **User Profile:**\n\n"
            f"🆔 **ID:** `{user_id}`\n"
            f"💰 **Balance:** `${user['balance']:.2f}`\n"
            f"🛒 **Total Orders:** `{user['orders']}`\n"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text(account_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_funds":
        funds_text = "💳 **Add Funds to Wallet:**\n\nTo top up your balance, please contact admin or use automated payment gateways."
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="main_menu"))
        bot.edit_message_text(funds_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "main_menu":
        welcome_text = (
            f"👋 **Main Menu:**\n\n"
            "🔥 **Premium Digital Store & Services Bot**\n"
            "Choose an option below to browse products, check your balance, or manage your account."
        )
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🛍️ Browse Products", callback_data="browse_shop"),
            types.InlineKeyboardButton("👤 My Account", callback_data="my_account"),
            types.InlineKeyboardButton("💳 Add Funds", callback_data="add_funds"),
            types.InlineKeyboardButton("📞 Support", url="https://t.me/your_support_username")
        )
        bot.edit_message_text(welcome_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("buy_"):
        prod_key = call.data.split("_", 1)[1]
        item = inventory.get(prod_key)
        if item and item["stock"] > 0:
            if user["balance"] >= item["price"]:
                user["balance"] -= item["price"]
                user["orders"] += 1
                item["stock"] -= 1
                item["sold"] += 1
                bot.answer_callback_query(call.id, "Purchase successful!")
                bot.send_message(call.message.chat.id, f"✅ **Success!** You have purchased **{item['name']}**.\nEnjoy your subscription!")
            else:
                bot.answer_callback_query(call.id, "Insufficient balance!", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "Sorry, this item is currently out of stock!", show_alert=True)

if __name__ == "__main__":
    # Start inventory manager in background thread
    inventory_thread = threading.Thread(target=multi_product_inventory_manager, daemon=True)
    inventory_thread.start()
    
    # Start bot polling
    bot.infinity_polling()
