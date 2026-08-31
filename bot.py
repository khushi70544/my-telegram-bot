import os
import random
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telebot import TeleBot, types

# Bot Token
BOT_TOKEN = "8888661139:AAFDzpjwmNDwcEe9-KNLC7hZnAnuZQd7DYQ"
bot = TeleBot(BOT_TOKEN)

# Admin Telegram ID
ADMIN_ID = 888661139

# Your Real Crypto Addresses
CRYPTO_WALLETS = {
    "btc": {
        "name": "Bitcoin (BTC)", 
        "address": "bc1pj9u898umy3r7fhgrq8w6nemvepcjr0pwl89z6nn66ghqzh9wz9nqudqsla"
    },
    "usdt": {
        "name": "USDT (ERC20/BEP20)", 
        "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"
    },
    "eth": {
        "name": "Ethereum (ETH)", 
        "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"
    },
    "sol": {
        "name": "Solana (SOL)", 
        "address": "H4cw8xf8A9pg6RTGBbAj2eobWM5HFNhxDKKroLQ1aEVq"
    },
    "trx": {
        "name": "Tron (TRX)", 
        "address": "THs69sCwiGDCDU1sWBA93tL2ct1ynQ6jyF"
    }
}

# UPI Gateway
UPI_ID = "xiaostore@upi"

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
        "welcome": "⚡ **Welcome to Xiao Elite Store, {name}!** ⚡\n\n👤 **Account ID:** `{user_id}`\n💰 **Balance:** `${balance:.2f}`\n🛒 **Orders:** `{orders}`\n\n✨ Select a payment method or option below:",
        "browse": "🤖 AI Services",
        "entertainment": "🎬 Entertainment",
        "topup": "💳 Top-up Wallet",
        "dashboard": "👤 My Dashboard",
        "lang_btn": "🌐 Language: English",
        "support": "📞 Support",
        "catalog_title": "✨ **Store Catalog** ✨\n\nChoose a category:",
        "back_menu": "🔙 Main Menu",
        "account_title": "👤 **Dashboard:**\n\n🆔 ID: `{user_id}`\n💰 Balance: `${balance:.2f}`\n🛒 Orders: `{orders}`",
        "deposit_title": "🪙 **Select Payment Gateway:**\n\nChoose your preferred payment method below:",
        "crypto_menu": "🪙 **Select Crypto Currency:**\n\nChoose which crypto you want to send:",
        "crypto_text": "🪙 **Pay via {coin_name}:**\n\n📍 **Address:**\n`{address}`\n\n📌 Send payment, then click '✅ I HAVE PAID' or type your TxID.",
        "upi_text": "🇮🇳 **UPI / Indian Payment Gateway:**\n\n📍 **UPI ID:** `{upi}`\n\n📌 Pay via UPI, then click '✅ I HAVE PAID'.",
        "paid_btn": "✅ I HAVE PAID",
        "insufficient": "❌ **Insufficient Balance!**\n\nRequired: `${price:.2f}` | Balance: `${balance:.2f}`\n\n📍 **Choose top-up method:**",
        "success": "🎉 **Order Placed Successfully!**\n\n📦 **Item:** {item_name}\n💸 **Deducted:** `${price:.2f}`\n💰 **New Balance:** `${balance:.2f}`\n\n⏳ Admin has been notified for approval."
    },
    "hi": {
        "welcome": "⚡ **Xiao Elite Store mein swagat hai, {name}!** ⚡\n\n👤 **Account ID:** `{user_id}`\n💰 **Balance:** `${balance:.2f}`\n🛒 **Orders:** `{orders}`\n\n✨ Neeche payment method ya option chunein:",
        "browse": "🤖 AI Services",
        "entertainment": "🎬 Entertainment",
        "topup": "💳 Top-up Wallet",
        "dashboard": "👤 Mera Dashboard",
        "lang_btn": "🌐 Language: Hinglish",
        "support": "📞 Support",
        "catalog_title": "✨ **Store Catalog** ✨\n\nCategory chunein:",
        "back_menu": "🔙 Main Menu",
        "account_title": "👤 **Dashboard:**\n\n🆔 ID: `{user_id}`\n💰 Balance: `${balance:.2f}`\n🛒 Orders: `{orders}`",
        "deposit_title": "🪙 **Payment Gateway Chunein:**\n\nApna pasandida payment method select karein:",
        "crypto_menu": "🪙 **Crypto Currency Chunein:**\n\nKis crypto mein payment karni hai select karein:",
        "crypto_text": "🪙 **{coin_name} dwara Payment Karein:**\n\n📍 **Address:**\n`{address}`\n\n📌 Payment bhejein aur '✅ I HAVE PAID' dabayein.",
        "upi_text": "🇮🇳 **UPI Payment Gateway:**\n\n📍 **UPI ID:** `{upi}`\n\n📌 Payment karne ke baad '✅ I HAVE PAID' dabayein.",
        "paid_btn": "✅ Maine Payment Kar Diya",
        "insufficient": "❌ **Balance Kam Hai!**\n\nChahiye: `${price:.2f}` | Balance: `${balance:.2f}`\n\n📍 **Top-up ke liye method chunein:**",
        "success": "🎉 **Order Bhej Diya Gaya Hai!**\n\n📦 **Item:** {item_name}\n💸 **Kate Paise:** `${price:.2f}`\n💰 **Balance:** `${balance:.2f}`\n\n⏳ Admin ko approval ke liye bhej diya gaya hai."
    }
}

user_data = {}
registered_users = set()

def get_user(user_id, name):
    registered_users.add(user_id)
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0, "lang": "en"}
    return user_data[user_id]

class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    username_str = f"@{username}" if username else "No Username"
    
    user = get_user(user_id, name)
    t = lang_text[user["lang"]]
    
    try:
        bot.send_message(
            ADMIN_ID, 
            f"🚀 **New User Started Bot!**\n\n👤 **Name:** {name}\n🔗 **Username:** {username_str}\n🆔 **ID:** `{user_id}`", 
            parse_mode="Markdown"
        )
    except Exception:
        pass

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
    username = message.from_user.username
    username_str = f"@{username}" if username else "No Username"
    text = message.text
    
    if text.startswith('/'):
        return
        
    bot.send_message(message.chat.id, f"✅ **Payment Proof / TxID Received:** `{text}`\n⏳ Verification pending by admin.", parse_mode="Markdown")
    try:
        bot.send_message(
            ADMIN_ID, 
            f"🔔 **New Payment Proof Submitted!**\n\n👤 **User:** {name}\n🔗 **Username:** {username_str}\n🆔 **ID:** `{user_id}`\n💳 **Details:** `{text}`", 
            parse_mode="Markdown"
        )
    except Exception:
        pass

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    name = call.from_user.first_name
    username = call.from_user.username
    username_str = f"@{username}" if username else "No Username"
    
    user = get_user(user_id, name)
    lang = user["lang"]
    t = lang_text[lang]
    
    bot.answer_callback_query(call.id)
    
    if call.data == "toggle_lang":
        user["lang"] = "hi" if lang == "en" else "en"
        call.data = "main_menu"
        
    elif call.data == "cat_ai" or call.data == "cat_entertainment":
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
        markup.add(types.InlineKeyboardButton("🪙 Top-up Wallet", callback_data="add_funds"))
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
            
            try:
                bot.send_message(
                    ADMIN_ID, 
                    f"🛒 **New Order Placed!**\n\n👤 **Buyer:** {name}\n🔗 **Username:** {username_str}\n🆔 **ID:** `{user_id}`\n📦 **Product:** {item['name']}\n💵 **Price:** `${item['price']:.2f}`", 
                    parse_mode="Markdown"
                )
            except Exception:
                pass
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🪙 Pay via Crypto", callback_data="add_funds"),
                types.InlineKeyboardButton("🇮🇳 Pay via UPI", callback_data="pay_upi")
            )
            markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu"))
            bot.edit_message_text(t["insufficient"].format(price=item['price'], balance=user['balance']), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_funds":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🪙 Crypto Currencies", callback_data="crypto_menu"),
            types.InlineKeyboardButton("🇮🇳 UPI / QR Code", callback_data="pay_upi"),
            types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu")
        )
        bot.edit_message_text(t["deposit_title"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "crypto_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, wallet in CRYPTO_WALLETS.items():
            markup.add(types.InlineKeyboardButton(wallet["name"], callback_data=f"crypto_pay_{key}"))
        markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data="add_funds"))
        bot.edit_message_text(t["crypto_menu"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("crypto_pay_"):
        coin_key = call.data.split("_")[2]
        wallet = CRYPTO_WALLETS.get(coin_key)
        if wallet:
            text = t["crypto_text"].format(coin_name=wallet["name"], address=wallet["address"])
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(t["paid_btn"], callback_data="tx_submitted"),
                types.InlineKeyboardButton(t["back_menu"], callback_data="crypto_menu")
            )
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "pay_upi":
        text = t["upi_text"].format(upi=UPI_ID)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(t["paid_btn"], callback_data="tx_submitted"),
            types.InlineKeyboardButton(t["back_menu"], callback_data="add_funds")
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "tx_submitted":
        bot.send_message(call.message.chat.id, "✍️ Please send your Transaction Reference / TxID or Screenshot details in chat:")

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
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            time.sleep(3)
