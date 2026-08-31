import os
import random
import time
import threading
from telebot import TeleBot, types

# Bot Token
BOT_TOKEN = "8888661139:AAFDzpjwmNDwcEe9-KNLC7hZnAnuZQd7DYQ"
bot = TeleBot(BOT_TOKEN)

# Deposit Crypto Address
DEPOSIT_ADDRESS = "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"

# Categorized Inventory Data with Randomized Stocks and Sales
inventory = {
    "ai": {
        "chatgpt_1m": {"name": "ChatGPT Plus 1 Month", "price": 3.00, "stock": random.randint(3, 10), "sold": random.randint(20, 35)},
        "chatgpt_6m": {"name": "ChatGPT Plus 6 Month", "price": 5.50, "stock": random.randint(2, 8), "sold": random.randint(12, 28)},
        "grok": {"name": "Grok AI Premium 1 Month", "price": 4.85, "stock": random.randint(2, 7), "sold": random.randint(8, 22)},
        "deepseek": {"name": "DeepSeek Pro 1 Month", "price": 12.00, "stock": random.randint(1, 4), "sold": random.randint(5, 15)}
    },
    "entertainment": {
        "spotify": {"name": "Spotify Premium 1 Month", "price": 0.50, "stock": random.randint(6, 15), "sold": random.randint(35, 60)},
        "netflix": {"name": "Netflix Premium 1 Month", "price": 0.80, "stock": random.randint(1, 9), "sold": random.randint(18, 42)}
    }
}

# User Balances & Registered Users Set
user_data = {}
registered_users = set()

def get_user(user_id, name):
    registered_users.add(user_id)
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0, "state": None, "selected_prod": None}
    return user_data[user_id]

def broadcast_to_users(msg_text):
    for user_id in list(registered_users):
        try:
            bot.send_message(user_id, msg_text, parse_mode="Markdown")
        except Exception:
            pass

def multi_product_inventory_manager():
    time.sleep(600)
    for category in inventory.values():
        for key in category:
            if category[key]["stock"] > 0:
                category[key]["sold"] += category[key]["stock"]
                category[key]["stock"] = 0

    while True:
        for category in inventory.values():
            for key, item in category.items():
                if item["stock"] <= 0:
                    out_of_stock_msg = (
                        "⚠️ **OUT OF STOCK!**\n\n"
                        f"📦 **{item['name']}** is currently completely sold out!\n\n"
                        f"📊 **Total Sold:** `{item['sold']}`\n"
                    )
                    broadcast_to_users(out_of_stock_msg)
        
        time.sleep(1800) 
        
        for category in inventory.values():
            for key, item in category.items():
                item["stock"] = random.randint(3, 10)
                restock_msg = (
                    "✅ **RESTOCK ALERT!**\n\n"
                    f"📦 **{item['name']}** is back in stock!\n"
                    f"🛒 **Available Stock:** `{item['stock']}`\n"
                )
                broadcast_to_users(restock_msg)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    user = get_user(user_id, name)
    
    welcome_text = (
        f"⚡ **Welcome to Xiao Elite Store, {name}!** ⚡\n\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Account ID:** `{user_id}`\n"
        f"💰 **Wallet Balance:** `${user['balance']:.2f}`\n"
        f"🛒 **Completed Orders:** `{user['orders']}`\n"
        f"━━━━━━━━━━━━━━━━━━━\n\n"
        "✨ Select a category below to explore high-end subscriptions:"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🤖 AI Services", callback_data="cat_ai"),
        types.InlineKeyboardButton("🎬 Entertainment", callback_data="cat_entertainment"),
        types.InlineKeyboardButton("💳 Top-up Wallet", callback_data="add_funds"),
        types.InlineKeyboardButton("👤 My Dashboard", callback_data="my_account"),
        types.InlineKeyboardButton("📞 Premium Support", url="https://t.me/your_support_username")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    user = get_user(user_id, call.from_user.first_name)
    
    if call.data == "cat_ai" or call.data == "cat_entertainment":
        cat_key = call.data.split("_")[1]
        cat_name = "🤖 AI Subscriptions" if cat_key == "ai" else "🎬 Entertainment & Streaming"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, item in inventory[cat_key].items():
            stock_status = f"🟢 Stock: {item['stock']}" if item['stock'] > 0 else "🔴 Sold Out"
            btn_text = f"🔹 {item['name']} | ${item['price']:.2f} ({stock_status})"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"item_{cat_key}_{key}"))
        
        markup.add(types.InlineKeyboardButton("🔙 Back to Categories", callback_data="browse_shop"))
        bot.edit_message_text(f"📂 **{cat_name}**\nSelect an item to view features and buy:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "browse_shop":
        welcome_text = (
            "✨ **Xiao Elite Store Catalog** ✨\n\n"
            "Choose a curated category below:"
        )
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🤖 AI Services", callback_data="cat_ai"),
            types.InlineKeyboardButton("🎬 Entertainment", callback_data="cat_entertainment"),
            types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")
        )
        bot.edit_message_text(welcome_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("item_"):
        _, cat_key, prod_key = call.data.split("_", 2)
        item = inventory[cat_key].get(prod_key)
        if not item:
            return
        
        stock_display = f"`{item['stock']} available`" if item['stock'] > 0 else "`Out of Stock`"
        prod_text = (
            f"💎 **Product Specifications:**\n\n"
            f"📌 **Service:** {item['name']}\n"
            f"💵 **Price:** `${item['price']:.2f}`\n"
            f"📦 **Available Stock:** {stock_display}\n"
            f"📊 **Global Sales:** `{item['sold']}`\n\n"
            f"Choose your preferred payment method:"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        if item['stock'] > 0:
            markup.add(types.InlineKeyboardButton("⚡ Instant Buy (Wallet Balance)", callback_data=f"pay_wallet_{cat_key}_{prod_key}"))
        markup.add(types.InlineKeyboardButton("🪙 Crypto Top-up & Deposit", callback_data="add_funds"))
        markup.add(types.InlineKeyboardButton("🔙 Back to Category", callback_data=f"cat_{cat_key}"))
        
        bot.edit_message_text(prod_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("pay_wallet_"):
        _, _, cat_key, prod_key = call.data.split("_", 3)
        item = inventory[cat_key].get(prod_key)
        
        if not item or item["stock"] <= 0:
            bot.answer_callback_query(call.id, "Sorry, this product is out of stock!", show_alert=True)
            return
            
        if user["balance"] >= item["price"]:
            user["balance"] -= item["price"]
            user["orders"] += 1
            item["stock"] -= 1
            item["sold"] += 1
            
            success_text = (
                f"🎉 **Transaction Successful!**\n\n"
                f"📦 **Item:** {item['name']}\n"
                f"💸 **Deducted:** `${item['price']:.2f}`\n"
                f"💰 **New Balance:** `${user['balance']:.2f}`\n\n"
                "🔑 Your access details have been successfully processed and dispatched."
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🛍️ Continue Shopping", callback_data="browse_shop"))
            bot.edit_message_text(success_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            shortage = item["price"] - user["balance"]
            fail_text = (
                f"❌ **Insufficient Wallet Funds!**\n\n"
                f"Required: `${item['price']:.2f}` | Your Balance: `${user['balance']:.2f}`\n"
                f"Shortfall: `${shortage:.2f}`\n\n"
                f"📍 **Official Crypto Deposit Address:**\n`{DEPOSIT_ADDRESS}`\n\n"
                "Transfer funds to the address above, then submit your transaction receipt below."
            )
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("✅ Submit Transaction ID (TxID)", callback_data="deposit_paid"),
                types.InlineKeyboardButton("🔙 Return to Product", callback_data=f"item_{cat_key}_{prod_key}")
            )
            bot.edit_message_text(fail_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_funds" or call.data == "deposit_paid":
        deposit_text = (
            f"🪙 **Top-up Wallet Gateway:**\n\n"
            f"📍 **Deposit Address:**\n`{DEPOSIT_ADDRESS}`\n\n"
            "📌 Send your crypto payment to the address above, then click '✅ I HAVE PAID' or type your TxID directly into the chat."
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("✅ I HAVE PAID", callback_data="tx_submitted"),
            types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")
        )
        bot.edit_message_text(deposit_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "tx_submitted":
        bot.answer_callback_query(call.id, "Send your Transaction Hash (TxID) in chat now!", show_alert=True)
        bot.send_message(call.message.chat.id, "✍️ Please drop your Transaction Hash (TxID) in this chat for verification:")

    elif call.data == "my_account":
        account_text = (
            f"👤 **Elite User Dashboard:**\n\n"
            f"🆔 **Telegram ID:** `{user_id}`\n"
            f"💰 **Current Balance:** `${user['balance']:.2f}`\n"
            f"🛒 **Total Purchases:** `{user['orders']}`\n"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu"))
        bot.edit_message_text(account_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_Mode="Markdown")

    elif call.data == "main_menu":
        welcome_text = (
            f"⚡ **Xiao Elite Store Menu** ⚡\n\n"
            f"👤 **Account ID:** `{user_id}`\n"
            f"💰 **Wallet Balance:** `${user['balance']:.2f}`\n"
            f"🛒 **Completed Orders:** `{user['orders']}`\n\n"
            "✨ Select a category below to explore high-end subscriptions:"
        )
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🤖 AI Services", callback_data="cat_ai"),
            types.InlineKeyboardButton("🎬 Entertainment", callback_data="cat_entertainment"),
            types.InlineKeyboardButton("💳 Top-up Wallet", callback_data="add_funds"),
            types.InlineKeyboardButton("👤 My Dashboard", callback_data="my_account"),
            types.InlineKeyboardButton("📞 Premium Support", url="https://t.me/your_support_username")
        )
        bot.edit_message_text(welcome_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    inventory_thread = threading.Thread(target=multi_product_inventory_manager, daemon=True)
    inventory_thread.start()
    
    bot.infinity_polling()
