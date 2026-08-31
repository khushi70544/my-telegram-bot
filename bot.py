import os
import random
import time
import threading
from telebot import TeleBot, types

# Bot Token
BOT_TOKEN = "8888661139:AAFDzpjwmNDwcEe9-KNLC7hZnAnuZQd7DYQ"
bot = TeleBot(BOT_TOKEN)

# Admin Telegram ID
ADMIN_ID = 888661139

# Deposit Crypto Address
DEPOSIT_ADDRESS = "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"

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

lang_text = {
    "en": {
        "welcome": "⚡ **Welcome to Xiao Elite Store, {name}!** ⚡\n\n👤 **Account ID:** `{user_id}`\n💰 **Balance:** `${balance:.2f}`\n🛒 **Orders:** `{orders}`\n\n✨ Select an option below:",
        "browse": "🤖 AI Services",
        "entertainment": "🎬 Entertainment",
        "topup": "💳 Top-up Wallet",
        "dashboard": "👤 My Dashboard",
        "lang_btn": "🌐 Language: English",
        "support": "📞 Support",
        "catalog_title": "✨ **Store Catalog** ✨\n\nChoose a category:",
        "back_menu": "🔙 Main Menu",
        "account_title": "👤 **Dashboard:**\n\n🆔 ID: `{user_id}`\n💰 Balance: `${balance:.2f}`\n🛒 Orders: `{orders}`",
        "deposit_title": "🪙 **Top-up Wallet:**\n\n📍 **Address:**\n`{address}`\n\n📌 Send payment, then click '✅ I HAVE PAID' or type your TxID.",
        "paid_btn": "✅ I HAVE PAID",
        "insufficient": "❌ **Insufficient Balance!**\n\nRequired: `${price:.2f}` | Balance: `${balance:.2f}`\n\n📍 **Deposit Address:**\n`{address}`",
        "success": "🎉 **Transaction Successful!**\n\n📦 **Item:** {item_name}\n💸 **Deducted:** `${price:.2f}`\n💰 **New Balance:** `${balance:.2f}`"
    },
    "hi": {
        "welcome": "⚡ **Xiao Elite Store mein swagat hai, {name}!** ⚡\n\n👤 **Account ID:** `{user_id}`\n💰 **Balance:** `${balance:.2f}`\n🛒 **Orders:** `{orders}`\n\n✨ Neeche se option chunein:",
        "browse": "🤖 AI Services",
        "entertainment": "🎬 Entertainment",
        "topup": "💳 Top-up Wallet",
        "dashboard": "👤 Mera Dashboard",
        "lang_btn": "🌐 Language: Hinglish",
        "support": "📞 Support",
        "catalog_title": "✨ **Store Catalog** ✨\n\nCategory chunein:",
        "back_menu": "🔙 Main Menu",
        "account_title": "👤 **Dashboard:**\n\n🆔 ID: `{user_id}`\n💰 Balance: `${balance:.2f}`\n🛒 Orders: `{orders}`",
        "deposit_title": "🪙 **Top-up Wallet:**\n\n📍 **Address:**\n`{address}`\n\n📌 Payment bhejein aur '✅ I HAVE PAID' dabayein.",
        "paid_btn": "✅ Maine Payment Kar Diya",
        "insufficient": "❌ **Balance Kam Hai!**\n\nChahiye: `${price:.2f}` | Balance: `${balance:.2f}`\n\n📍 **Address:**\n`{address}`",
        "success": "🎉 **Safal Raha!**\n\n📦 **Item:** {item_name}\n💸 **Kate Paise:** `${price:.2f}`\n💰 **Balance:** `${balance:.2f}`"
    }
}

user_data = {}
registered_users = set()

def get_user(user_id, name):
    registered_users.add(user_id)
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0, "lang": "en"}
    return user_data[user_id]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    user = get_user(user_id, name)
    t = lang_text[user["lang"]]
    
    text = t["welcome"].format(name=name, user_id=user_id, balance=user['balance'], orders=user['orders'])
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t["browse"], callback_data="cat_ai"),
        types.InlineKeyboardButton(t["entertainment"], callback_data="cat_entertainment"),
        types.InlineKeyboardButton(t["topup"], callback_data="add_funds"),
        types.InlineKeyboardButton(t["dashboard"], callback_data="my_account"),
        types.InlineKeyboardButton(t["lang_btn"], callback_data="toggle_lang"),
        types.InlineKeyboardButton(t["support"], url="https://t.me/ZhiGeAI")
    )
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    text = message.text
    
    if text.startswith('/'):
        return
        
    bot.send_message(message.chat.id, f"✅ **TxID Received:** `{text}`\n⏳ Verification pending.", parse_mode="Markdown")
    try:
        bot.send_message(ADMIN_ID, f"🔔 **New TxID:**\n👤 {name} (`{user_id}`)\n💳 `{text}`", parse_mode="Markdown")
    except Exception:
        pass

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    user = get_user(user_id, call.from_user.first_name)
    lang = user["lang"]
    t = lang_text[lang]
    
    if call.data == "toggle_lang":
        user["lang"] = "hi" if lang == "en" else "en"
        call.data = "main_menu"
        
    if call.data == "cat_ai" or call.data == "cat_entertainment":
        cat_key = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, item in inventory[cat_key].items():
            stock = f"🟢 {item['stock']}" if item['stock'] > 0 else "🔴 Sold Out"
            markup.add(types.InlineKeyboardButton(f"{item['name']} | ${item['price']:.2f} ({stock})", callback_data=f"item_{cat_key}_{key}"))
        markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu"))
        bot.edit_message_text(t["catalog_title"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("item_"):
        _, cat_key, prod_key = call.data.split("_", 2)
        item = inventory[cat_key].get(prod_key)
        if not item: return
        
        text = f"📌 **{item['name']}**\n💵 Price: `${item['price']:.2f}`\n📦 Stock: `{item['stock']}`"
        markup = types.InlineKeyboardMarkup(row_width=1)
        if item['stock'] > 0:
            markup.add(types.InlineKeyboardButton("⚡ Instant Buy", callback_data=f"buy_{cat_key}_{prod_key}"))
        markup.add(types.InlineKeyboardButton("🪙 Top-up", callback_data="add_funds"))
        markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data=f"cat_{cat_key}"))
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("buy_"):
        _, cat_key, prod_key = call.data.split("_", 2)
        item = inventory[cat_key].get(prod_key)
        if user["balance"] >= item["price"]:
            user["balance"] -= item["price"]
            user["orders"] += 1
            item["stock"] -= 1
            item["sold"] += 1
            text = t["success"].format(item_name=item['name'], price=item['price'], balance=user['balance'])
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu"))
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            text = t["insufficient"].format(price=item['price'], balance=user['balance'], address=DEPOSIT_ADDRESS)
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu"))
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_funds" or call.data == "tx_submitted":
        text = t["deposit_title"].format(address=DEPOSIT_ADDRESS)
        markup = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(t["paid_btn"], callback_data="tx_submitted"),
            types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu")
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        if call.data == "tx_submitted":
            bot.send_message(call.message.chat.id, "✍️ Send your Transaction Hash (TxID):")

    elif call.data == "my_account":
        text = t["account_title"].format(user_id=user_id, balance=user['balance'], orders=user['orders'])
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu"))
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "main_menu":
        text = t["welcome"].format(name=call.from_user.first_name, user_id=user_id, balance=user['balance'], orders=user['orders'])
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(t["browse"], callback_data="cat_ai"),
            types.InlineKeyboardButton(t["entertainment"], callback_data="cat_entertainment"),
            types.InlineKeyboardButton(t["topup"], callback_data="add_funds"),
            types.InlineKeyboardButton(t["dashboard"], callback_data="my_account"),
            types.InlineKeyboardButton(t["lang_btn"], callback_data="toggle_lang"),
            types.InlineKeyboardButton(t["support"], url="https://t.me/ZhiGeAI")
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            time.sleep(3)
