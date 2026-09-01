import os
import random
import time
import threading
import requests
from flask import Flask
from telebot import TeleBot, types

# Bot Token Updated
BOT_TOKEN = "8888661139:AAFluKA60FPKddBVI1WlZskX3s2W5W6i-XU" 
bot = TeleBot(BOT_TOKEN)

# Admin Telegram ID
ADMIN_ID = 8852375598

# Your Render Web Service URL
RENDER_URL = "https://my-telegram-bot-wnyy.onrender.com"

# Crypto Wallets
CRYPTO_WALLETS = {
    "btc": {"name": "🪙 Bitcoin (BTC)", "address": "bc1pj9u898umy3r7fhgrq8w6nemvepcjr0pwl89z6nn66ghqzh9wz9nqudqsla"},
    "usdt": {"name": "💵 USDT (ERC20/BEP20)", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "eth": {"name": "💎 Ethereum (ETH)", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "sol": {"name": "🟣 Solana (SOL)", "address": "H4cw8xf8A9pg6RTGBbAj2eobWM5HFNhxDKKroLQ1aEVq"},
    "trx": {"name": "🔴 Tron (TRX)", "address": "THs69sCwiGDCDU1sWBA93tL2ct1ynQ6jyF"}
}

# Inventory with Updated Prices & Banner Images
inventory = {
    "ai": {
        "chatgpt_1m": {
            "name": "🤖 ChatGPT Plus 1 Month", 
            "price": 3.40, 
            "stock": random.randint(3, 7), 
            "sold": random.randint(20, 35),
            "image": "https://images.unsplash.com/photo-1677442136019-21780efad99a?w=600"
        },
        "chatgpt_6m": {
            "name": "🤖 ChatGPT Plus 6 Month", 
            "price": 13.90, 
            "stock": random.randint(2, 5), 
            "sold": random.randint(12, 28),
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600"
        },
        "chatgpt_pro5": {
            "name": "⚡ ChatGPT Pro ×5", 
            "price": 12.65, 
            "stock": random.randint(2, 6), 
            "sold": random.randint(3, 10),
            "image": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=600"
        },
        "chatgpt_pro20": {
            "name": "🚀 ChatGPT Pro ×20", 
            "price": 30.80, 
            "stock": random.randint(1, 4), 
            "sold": random.randint(1, 5),
            "image": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=600"
        },
        "grok": {
            "name": "🧠 Grok AI Premium 1 Month", 
            "price": 5.99, 
            "stock": random.randint(3, 8), 
            "sold": random.randint(8, 22),
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600"
        },
        "deepseek": {
            "name": "🔬 DeepSeek Pro 1 Month", 
            "price": 9.99, 
            "stock": random.randint(4, 9), 
            "sold": random.randint(5, 15),
            "image": "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=600"
        },
        "claude_max_5x": {
            "name": "🔥 Claude Max ×5", 
            "price": 14.50, 
            "stock": random.randint(2, 5), 
            "sold": random.randint(5, 15),
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600"
        },
        "claude_max_20x": {
            "name": "🌟 Claude Max ×20", 
            "price": 35.00, 
            "stock": random.randint(1, 3), 
            "sold": random.randint(1, 8),
            "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600"
        }
    },
    "entertainment": {
        "spotify": {
            "name": "🎧 Spotify Premium 1 Month", 
            "price": 1.99, 
            "stock": random.randint(5, 12), 
            "sold": random.randint(35, 60),
            "image": "https://images.unsplash.com/photo-1614680376593-902f749f7ffc?w=600"
        },
        "netflix": {
            "name": "🍿 Netflix Premium 1 Month", 
            "price": 3.49, 
            "stock": random.randint(4, 10), 
            "sold": random.randint(18, 42),
            "image": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=600"
        }
    }
}

user_data = {}
admin_states = {}

recent_sales_ticker = "🔥 **Live Feed:** `Rahul from Delhi` just purchased `ChatGPT Plus 1 Month`!"

def fake_sales_ticker_updater():
    global recent_sales_ticker
    names = ["Rahul", "Aman", "Alex", "David", "Vikram", "John", "Sameer", "Chris", "Tanvir", "Michael"]
    cities = ["Mumbai", "New York", "London", "Delhi", "Toronto", "Berlin", "Sydney", "Dubai", "Paris"]
    products = ["ChatGPT Plus 1 Month", "ChatGPT Pro ×5", "Claude Max ×5", "Spotify Premium 1 Month", "Netflix Premium 1 Month"]
    while True:
        time.sleep(random.randint(40, 80))
        n = random.choice(names)
        c = random.choice(cities)
        p = random.choice(products)
        recent_sales_ticker = f"🔥 **Live Feed:** `{n} ({c})` just purchased `{p}`!"

def get_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0}
    return user_data[user_id]

def auto_stock_updater():
    while True:
        sleep_time = random.randint(600, 1200)
        time.sleep(sleep_time)
        try:
            cat_key = random.choice(list(inventory.keys()))
            prod_key = random.choice(list(inventory[cat_key].keys()))
            item = inventory[cat_key][prod_key]
            
            action_type = random.choice(["add", "reduce"])
            if action_type == "add":
                added_qty = random.randint(2, 4)
                item["stock"] += added_qty
                msg = f"📈 **[AUTO STOCK] Added Stock:**\n\n📦 **Product:** `{item['name']}`\n➕ **Added:** `+{added_qty}`\n📦 **New Stock:** `{item['stock']}`"
            else:
                reduced_qty = random.randint(1, 2)
                if item["stock"] >= reduced_qty:
                    item["stock"] -= reduced_qty
                msg = f"📉 **[AUTO STOCK] Reduced Stock:**\n\n📦 **Product:** `{item['name']}`\n➖ **Reduced:** `-{reduced_qty}`\n📦 **New Stock:** `{item['stock']}`"
            
            bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"Stock updater error: {e}")

def keep_alive():
    while True:
        time.sleep(300)
        try:
            requests.get(RENDER_URL)
        except Exception as e:
            print(f"Keep-alive ping error: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running successfully!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    user = get_user(user_id)

    text = f"""⚡ **WELCOME TO XIAO ELITE STORE, {name.upper()}!** ⚡

{recent_sales_ticker}

👤 **ACCOUNT ID:** `{user_id}`
💰 **WALLET BALANCE:** `${user['balance']:.2f}`
🛒 **TOTAL ORDERS:** `{user['orders']}`

✨ **PLEASE SELECT AN OPTION BELOW:**"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🤖 AI SERVICES", callback_data="cat_ai"),
        types.InlineKeyboardButton("🎬 ENTERTAINMENT", callback_data="cat_entertainment"),
        types.InlineKeyboardButton("💳 TOP-UP WALLET", callback_data="add_funds"),
        types.InlineKeyboardButton("👤 MY DASHBOARD", callback_data="my_account"),
        types.InlineKeyboardButton("📞 SUPPORT", url="https://t.me/ZhiGeAI")
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

    if user_id == ADMIN_ID and ADMIN_ID in admin_states and admin_states[ADMIN_ID].get("action") == "awaiting_reply_msg":
        target_user_id = admin_states[ADMIN_ID]["target_user"]
        try:
            bot.send_message(target_user_id, f"🎉 **ADMIN MESSAGE / PRODUCT DETAILS:**\n\n{text}", parse_mode="Markdown")
            bot.send_message(ADMIN_ID, f"✅ **MESSAGE SUCCESSFULLY SENT TO USER** `{target_user_id}`!")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"❌ **FAILED TO SEND MESSAGE:** `{e}`")
        del admin_states[ADMIN_ID]
        return

    bot.send_message(message.chat.id, f"✅ **PAYMENT PROOF / TXID RECEIVED:**\n`{text}`\n\n⏳ **VERIFICATION PENDING BY ADMIN.**", parse_mode="Markdown")
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{user_id}"),
            types.InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{user_id}")
        )
        bot.send_message(
            ADMIN_ID, 
            f"🔔 **NEW PAYMENT PROOF SUBMITTED!**\n\n👤 **USER:** {name}\n🔗 **USERNAME:** {username_str}\n🆔 **ID:** `{user_id}`\n💳 **DETAILS:** `{text}`", 
            reply_markup=markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Admin error: {e}")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    name = call.from_user.first_name
    user = get_user(user_id)
    
    bot.answer_callback_query(call.id)
    
    if call.data.startswith("approve_") or call.data.startswith("reject_"):
        if user_id != ADMIN_ID:
            return
        action, target_id = call.data.split("_")
        target_id = int(target_id)
        
        if action == "approve":
            bot.edit_message_text(f"{call.message.text}\n\n✅ **STATUS:** **APPROVED**", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
            try:
                bot.send_message(target_id, "🎉 **YOUR PAYMENT HAS BEEN APPROVED BY THE ADMIN!**")
            except:
                pass
            admin_states[ADMIN_ID] = {"action": "awaiting_reply_msg", "target_user": target_id}
            bot.send_message(ADMIN_ID, f"✍️ **NOW SEND THE MESSAGE/PRODUCT DETAILS YOU WANT TO SEND TO USER** `{target_id}`:")
        else:
            bot.edit_message_text(f"{call.message.text}\n\n❌ **STATUS:** **REJECTED**", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
            try:
                bot.send_message(target_id, "❌ **YOUR PAYMENT VERIFICATION WAS REJECTED BY ADMIN.**")
            except:
                pass
        return
        
    elif call.data == "cat_ai" or call.data == "cat_entertainment":
        cat_key = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, item in inventory[cat_key].items():
            stock_label = f"🟢 IN STOCK ({item['stock']})" if item['stock'] > 0 else "🔴 SOLD OUT"
            markup.add(types.InlineKeyboardButton(f"{item['name']} | ${item['price']:.2f} [{stock_label}]", callback_data=f"item_{cat_key}_{key}"))
        markup.add(types.InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="main_menu"))
        
        cat_text = f"""✨ **STORE CATALOG:**

{recent_sales_ticker}

📌 **CHOOSE A CATEGORY BELOW:**"""
        try:
            bot.edit_message_text(cat_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.send_message(call.message.chat.id, cat_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("item_"):
        parts = call.data.split("_")
        cat_key = parts[1]
        prod_key = "_".join(parts[2:])
        item = inventory[cat_key].get(prod_key)
        if not item: return
        
        scarcity_tag = "⚠️ **HIGH DEMAND - SELLING FAST!**" if item['stock'] <= 3 else "🔥 **HOT DEAL - INSTANT DELIVERY**"
        
        text = f"""📌 **PRODUCT DETAILS:**

🏷️ **NAME:** {item['name']}
💵 **PRICE:** `${item['price']:.2f}`
📦 **STOCK:** `{item['stock']} available`
🔥 **TOTAL SOLD:** `{item['sold']}+ units`

{scarcity_tag}

🔢 **SELECT QUANTITY BELOW:**"""

        markup = types.InlineKeyboardMarkup(row_width=5)
        qty_buttons = []
        for q in range(1, 6):
            if item['stock'] >= q:
                qty_buttons.append(types.InlineKeyboardButton(str(q), callback_data=f"qty_{cat_key}_{prod_key}_{q}"))
        markup.add(*qty_buttons)
        markup.add(types.InlineKeyboardButton("🔙 BACK TO CATALOG", callback_data=f"cat_{cat_key}"))
        
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        bot.send_photo(call.message.chat.id, item['image'], caption=text, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("qty_"):
        parts = call.data.split("_")
        qty_str = parts[-1]
        cat_key = parts[1]
        prod_key = "_".join(parts[2:-1])
        
        qty = int(qty_str)
        item = inventory[cat_key].get(prod_key)
        if not item: return

        total_price = item["price"] * qty
        text = f"""📌 **ORDER SUMMARY:**

🏷️ **PRODUCT:** {item['name']}
🔢 **QUANTITY:** `{qty}`
💵 **TOTAL PRICE:** `${total_price:.2f}`
📦 **AVAILABLE STOCK:** `{item['stock']}`

⚡ **CLICK CONFIRM BELOW TO LOCK IN THIS PRICE!**"""
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        if item['stock'] >= qty:
            markup.add(types.InlineKeyboardButton(f"⚡ CONFIRM & BUY ({qty}x) - ${total_price:.2f}", callback_data=f"buy_{cat_key}_{prod_key}_{qty}"))
        markup.add(types.InlineKeyboardButton("🪙 TOP-UP WALLET", callback_data="add_funds"))
        markup.add(types.InlineKeyboardButton("🔙 BACK TO PRODUCT", callback_data=f"item_{cat_key}_{prod_key}"))
        
        try:
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("buy_"):
        parts = call.data.split("_")
        qty_str = parts[-1]
        cat_key = parts[1]
        prod_key = "_".join(parts[2:-1])
        
        qty = int(qty_str)
        item = inventory[cat_key].get(prod_key)
        if not item: return
        
        total_price = item["price"] * qty

        if user["balance"] >= total_price:
            user["balance"] -= total_price
            user["orders"] += 1
            item["stock"] -= qty
            item["sold"] += qty
            
            text = f"""🎉 **ORDER PLACED SUCCESSFULLY!**

📦 **ITEM:** {item['name']} (Qty: {qty})
💸 **TOTAL DEDUCTED:** `${total_price:.2f}`
💰 **NEW BALANCE:** `${user['balance']:.2f}`

⏳ **ADMIN HAS BEEN NOTIFIED FOR INSTANT DISPATCH.**"""

            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏠 BACK TO MAIN MENU", callback_data="main_menu"))
            
            try:
                bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, reply_markup=markup, parse_mode="Markdown")
            except:
                bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            
            try:
                username = call.from_user.username
                username_str = f"@{username}" if username else "No Username"
                bot.send_message(
                    ADMIN_ID, 
                    f"🛒 **NEW ORDER PLACED!**\n\n👤 **BUYER:** {name}\n🔗 **USERNAME:** {username_str}\n🆔 **ID:** `{user_id}`\n📦 **PRODUCT:** {item['name']} (x{qty})\n💵 **TOTAL:** `${total_price:.2f}`", 
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Admin order notification error: {e}")
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🪙 PAY VIA CRYPTO", callback_data="crypto_menu"),
                types.InlineKeyboardButton("🏠 BACK TO MAIN MENU", callback_data="main_menu")
            )
            text = f"""❌ **INSUFFICIENT WALLET BALANCE!**

💵 **REQUIRED:** `${total_price:.2f}` | 💰 **YOUR BALANCE:** `${user['balance']:.2f}`

📍 **CHOOSE TOP-UP METHOD BELOW:**"""
            try:
                bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, reply_markup=markup, parse_mode="Markdown")
            except:
                bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_funds":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🪙 CRYPTO CURRENCIES", callback_data="crypto_menu"),
            types.InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="main_menu")
        )
        funds_text = """💳 **SELECT PAYMENT GATEWAY:**

📌 **CHOOSE YOUR PREFERRED CRYPTO CURRENCY BELOW:**"""
        try:
            bot.edit_message_text(funds_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.send_message(call.message.chat.id, funds_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "crypto_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, wallet in CRYPTO_WALLETS.items():
            markup.add(types.InlineKeyboardButton(wallet["name"], callback_data=f"crypto_pay_{key}"))
        markup.add(types.InlineKeyboardButton("🔙 BACK", callback_data="add_funds"))
        bot.edit_message_text("🪙 **SELECT CRYPTO CURRENCY:**\n\n📌 **CHOOSE WHICH CRYPTO YOU WANT TO SEND:**", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("crypto_pay_"):
        coin_key = call.data.split("_")[2]
        wallet = CRYPTO_WALLETS.get(coin_key)
        if wallet:
            text = f"""🪙 **PAY VIA {wallet['name']}:**

📍 **DEPOSIT ADDRESS:**
`{wallet['address']}`

📌 **SEND PAYMENT, THEN CLICK 'I HAVE PAID' OR TYPE YOUR TXID.**"""
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("✅ I HAVE PAID (SEND TXID)", callback_data="tx_submitted"),
                types.InlineKeyboardButton("🔙 BACK", callback_data="crypto_menu")
            )
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "tx_submitted":
        bot.send_message(call.message.chat.id, "✍️ **PLEASE SEND YOUR TRANSACTION REFERENCE / TXID OR SCREENSHOT DETAILS IN CHAT:**", parse_mode="Markdown")

    elif call.data == "my_account":
        text = f"👤 **USER DASHBOARD:**\n\n🆔 **ID:** `{user_id}`\n💰 **BALANCE:** `${user['balance']:.2f}`\n🛒 **TOTAL ORDERS:** `{user['orders']}`"
        markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="main_menu"))
        try:
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "main_menu":
        text = f"""⚡ **WELCOME TO XIAO ELITE STORE, {name.upper()}!** ⚡

{recent_sales_ticker}

👤 **ACCOUNT ID:** `{user_id}`
💰 **WALLET BALANCE:** `${user['balance']:.2f}`
🛒 **TOTAL ORDERS:** `{user['orders']}`

✨ **PLEASE SELECT AN OPTION BELOW:**"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🤖 AI SERVICES", callback_data="cat_ai"),
            types.InlineKeyboardButton("🎬 ENTERTAINMENT", 
