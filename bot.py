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

# Multi-Language Dictionaries (English & Hinglish)
lang_text = {
    "en": {
        "welcome": "⚡ **Welcome to Xiao Elite Store, {name}!** ⚡\n\n━━━━━━━━━━━━━━━━━━━\n👤 **Account ID:** `{user_id}`\n💰 **Wallet Balance:** `${balance:.2f}`\n🛒 **Completed Orders:** `{orders}`\n━━━━━━━━━━━━━━━━━━━\n\n✨ Select a category below or change language:",
        "browse": "🤖 AI Services",
        "entertainment": "🎬 Entertainment",
        "topup": "💳 Top-up Wallet",
        "dashboard": "👤 My Dashboard",
        "lang_btn": "🌐 Language: English",
        "support": "📞 Premium Support",
        "catalog_title": "✨ **Xiao Elite Store Catalog** ✨\n\nChoose a curated category below:",
        "back_menu": "🔙 Main Menu",
        "account_title": "👤 **Elite User Dashboard:**\n\n🆔 **Telegram ID:** `{user_id}`\n💰 **Current Balance:** `${balance:.2f}`\n🛒 **Total Purchases:** `{orders}`\n🌐 **Language:** English",
        "deposit_title": "🪙 **Top-up Wallet Gateway:**\n\n📍 **Deposit Address:**\n`{address}`\n\n📌 Send your crypto payment to the address above, then click '✅ I HAVE PAID' or type your TxID directly into chat.",
        "paid_btn": "✅ I HAVE PAID",
        "insufficient": "❌ **Insufficient Wallet Funds!**\n\nRequired: `${price:.2f}` | Your Balance: `${balance:.2f}`\nShortfall: `${shortage:.2f}`\n\n📍 **Official Crypto Deposit Address:**\n`{address}`",
        "success": "🎉 **Transaction Successful!**\n\n📦 **Item:** {item_name}\n💸 **Deducted:** `${price:.2f}`\n💰 **New Balance:** `${balance:.2f}`\n\n🔑 Your access details have been successfully processed and dispatched."
    },
    "hi": {
        "welcome": "⚡ **Xiao Elite Store mein aapka swagat hai, {name}!** ⚡\n\n━━━━━━━━━━━━━━━━━━━\n👤 **Account ID:** `{user_id}`\n💰 **Wallet Balance:** `${balance:.2f}`\n🛒 **Completed Orders:** `{orders}`\n━━━━━━━━━━━━━━━━━━━\n\n✨ Neeche category select karein ya bhasha badlein:",
        "browse": "🤖 AI Services",
        "entertainment": "🎬 Entertainment",
        "topup": "💳 Top-up Wallet",
        "dashboard": "👤 Mera Dashboard",
        "lang_btn": "🌐 Language: Hinglish",
        "support": "📞 Premium Support",
        "catalog_title": "✨ **Xiao Elite Store Catalog** ✨\n\nNeeche di gayi category select karein:",
        "back_menu": "🔙 Main Menu",
        "account_title": "👤 **User Dashboard:**\n\n🆔 **Telegram ID:** `{user_id}`\n💰 **Current Balance:** `${balance:.2f}`\n🛒 **Total Purchases:** `{orders}`\n🌐 **Bhasha:** Hinglish",
        "deposit_title": "🪙 **Top-up Wallet Gateway:**\n\n📍 **Deposit Address:**\n`{address}`\n\n📌 Upar diye gaye address par payment bhejein aur '✅ I HAVE PAID' par click karein ya TxID chat me bhejein.",
        "paid_btn": "✅ Maine Payment Kar Diya Hai",
        "insufficient": "❌ **Wallet Me Balance Kam Hai!**\n\nChahiye: `${price:.2f}` | Aapka Balance: `${balance:.2f}`\nKam Pad Rahe Hain: `${shortage:.2f}`\n\n📍 **Crypto Deposit Address:**\n`{address}`",
        "success": "🎉 **Transaction Safal Rahi!**\n\n📦 **Item:** {item_name}\n💸 **Kate Hue Paise:** `${price:.2f}`\n💰 **Naya Balance:** `${balance:.2f}`\n\n🔑 Aapki details bhej di gayi hain."
    }
}

# User Balances & Registered Users Set
user_data = {}
registered_users = set()

def get_user(user_id, name):
    registered_users.add(user_id)
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0, "state": None, "selected_prod": None, "lang": "en"}
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
    lang = user["lang"]
    
    t = lang_text[lang]
    welcome_text = t["welcome"].format(name=name, user_id=user_id, balance=user['balance'], orders=user['orders'])
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t["browse"], callback_data="cat_ai"),
        types.InlineKeyboardButton(t["entertainment"], callback_data="cat_entertainment"),
        types.InlineKeyboardButton(t["topup"], callback_data="add_funds"),
        types.InlineKeyboardButton(t["dashboard"], callback_data="my_account"),
        types.InlineKeyboardButton(t["lang_btn"], callback_data="toggle_lang"),
        types.InlineKeyboardButton(t["support"], url="https://t.me/ZhiGeAI")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    user = get_user(user_id, call.from_user.first_name)
    lang = user["lang"]
    t = lang_text[lang]
    
    if call.data == "toggle_lang":
        user["lang"] = "hi" if lang == "en" else "en"
        handle_callbacks(types.CallbackQuery(id=call.id, from_user=call.from_user, chat_instance=call.chat_instance, message=call.message, data="main_menu"))
        return

    if call.data == "cat_ai" or call.data == "cat_entertainment":
        cat_key = call.data.split("_")[1]
        cat_name = "🤖 AI Subscriptions" if cat_key == "ai" else "🎬 Entertainment & Streaming"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, item in inventory[cat_key].items():
            stock_status = f"🟢 Stock: {item['stock']}" if item['stock'] > 0 else "🔴 Sold Out"
            btn_text = f"🔹 {item['name']} | ${item['price']:.2f} ({stock_status})"
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"item_{cat_key}_{key}"))
        
        markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data="browse_shop"))
        bot.edit_message_text(f"📂 **{cat_name}**", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "browse_shop":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(t["browse"], callback_data="cat_ai"),
            types.InlineKeyboardButton(t["entertainment"], callback_data="cat_entertainment"),
            types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu")
        )
        bot.edit_message_text(t["catalog_title"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

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
            f"📦 **Stock:** {stock_display}\n"
            f"📊 **Sales:** `{item['sold']}`\n"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        if item['stock'] > 0:
            markup.add(types.InlineKeyboardButton("⚡ Instant Buy (Wallet)", callback_data=f"pay_wallet_{cat_key}_{prod_key}"))
        markup.add(types.InlineKeyboardButton("🪙 Crypto Top-up", callback_data="add_funds"))
        markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data=f"cat_{cat_key}"))
        
        bot.edit_message_text(prod_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("pay_wallet_"):
        _, _, cat_key, prod_key = call.data.split("_", 3)
        item = inventory[cat_key].get(prod_key)
        
        if not item or item["stock"] <= 0:
            bot.answer_callback_query(call.id, "Out of stock!", show_alert=True)
            return
            
        if user["balance"] >= item["price"]:
            user["balance"] -= item["price"]
            user["orders"] += 1
            item["stock"] -= 1
            item["sold"] += 1
            
            success_text = t["success"].format(item_name=item['name'], price=item['price'], balance=user['balance'])
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data="browse_shop"))
            bot.edit_message_text(success_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            shortage = item["price"] - user["balance"]
            fail_text = t["insufficient"].format(price=item['price'], balance=user['balance'], shortage=shortage, address=DEPOSIT_ADDRESS)
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("✅ Submit TxID", callback_data="deposit_paid"),
                types.InlineKeyboardButton(t["back_menu"], callback_data=f"item_{cat_key}_{prod_key}")
            )
            bot.edit_message_text(fail_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_funds" or call.data == "deposit_paid":
        deposit_text = t["deposit_title"].format(address=DEPOSIT_ADDRESS)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(t["paid_btn"], callback_data="tx_submitted"),
            types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu")
        )
        bot.edit_message_text(deposit_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "tx_submitted":
        bot.answer_callback_query(call.id, "Send your TxID in chat!", show_alert=True)
        bot.send_message(call.message.chat.id, "✍️ Please send your Transaction Hash (TxID) in chat:")

    elif call.data == "my_account":
        account_text = t["account_title"].format(user_id=user_id, balance=user['balance'], orders=user['orders'])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu"))
        bot.edit_message_text(account_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "main_menu":
        welcome_text = t["welcome"].format(name=call.from_user.first_name, user_id=user_id, balance=user['balance'], orders=user['orders'])
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(t["browse"], callback_data="cat_ai"),
            types.InlineKeyboardButton(t["entertainment"], callback_data="cat_entertainment"),
            types.InlineKeyboardButton(t["topup"], callback_data="add_funds"),
            types.InlineKeyboardButton(t["dashboard"], callback_data="my_account"),
            types.InlineKeyboardButton(t["lang_btn"], callback_data="toggle_lang"),
            types.InlineKeyboardButton(t["support"], url="https://t.me/ZhiGeAI")
        )
        bot.edit_message_text(welcome_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    inventory_thread = threading.Thread(target=multi_product_inventory_manager, daemon=True)
    inventory_thread.start()
    
    bot.infinity_polling()
