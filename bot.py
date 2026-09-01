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
    "btc": {"name": "🪙 Bitcoin (BTC)", "address": "bc1pj9u898umy3r7fhgrq8w6nemvepcjr0pwl89z6nn66ghqzh9wz9nqudqsla"},
    "usdt": {"name": "💵 USDT (ERC20/BEP20)", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "eth": {"name": "💎 Ethereum (ETH)", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "sol": {"name": "🟣 Solana (SOL)", "address": "H4cw8xf8A9pg6RTGBbAj2eobWM5HFNhxDKKroLQ1aEVq"},
    "trx": {"name": "🔴 Tron (TRX)", "address": "THs69sCwiGDCDU1sWBA93tL2ct1ynQ6jyF"}
}

inventory = {
    "ai": {
        "chatgpt_1m": {
            "name": "🤖 ChatGPT Plus 1 Month", 
            "price": 3.40, 
            "stock": random.randint(3, 7), 
            "sold": random.randint(20, 35),
            "image": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo_%282023%29.svg"
        },
        "chatgpt_6m": {
            "name": "🤖 ChatGPT Plus 6 Month", 
            "price": 13.90, 
            "stock": random.randint(2, 5), 
            "sold": random.randint(12, 28),
            "image": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo_%282023%29.svg"
        },
        "chatgpt_pro5": {
            "name": "⚡ ChatGPT Pro ×5 Accounts", 
            "price": 12.65, 
            "stock": random.randint(2, 6), 
            "sold": random.randint(3, 10),
            "image": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo_%282023%29.svg"
        },
        "chatgpt_pro20": {
            "name": "🚀 ChatGPT Pro ×20 Accounts", 
            "price": 30.80, 
            "stock": random.randint(1, 4), 
            "sold": random.randint(1, 5),
            "image": "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo_%282023%29.svg"
        },
        "grok": {
            "name": "🧠 Grok AI Premium 1 Month", 
            "price": 5.99, 
            "stock": random.randint(3, 8), 
            "sold": random.randint(8, 22),
            "image": "https://pbs.twimg.com/profile_images/1813959929828552704/81d45s8o_400x400.jpg"
        },
        "deepseek": {
            "name": "🔬 DeepSeek Pro 1 Month", 
            "price": 9.99, 
            "stock": random.randint(4, 9), 
            "sold": random.randint(5, 15),
            "image": "https://images.seeklogo.com/logo-png/52/2/deepseek-logo-png_seeklogo-526978.png"
        },
        "claude_max_5x": {
            "name": "🔥 Claude Max ×5 Accounts", 
            "price": 14.50, 
            "stock": random.randint(2, 5), 
            "sold": random.randint(5, 15),
            "image": "https://anthropic.com/images/icons/apple-touch-icon.png"
        },
        "claude_max_20x": {
            "name": "🌟 Claude Max ×20 Accounts", 
            "price": 35.00, 
            "stock": random.randint(1, 3), 
            "sold": random.randint(1, 8),
            "image": "https://anthropic.com/images/icons/apple-touch-icon.png"
        }
    },
    "entertainment": {
        "spotify": {
            "name": "🎧 Spotify Premium 1 Month", 
            "price": 1.99, 
            "stock": random.randint(5, 12), 
            "sold": random.randint(35, 60),
            "image": "https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg"
        },
        "netflix": {
            "name": "🍿 Netflix Premium 1 Month", 
            "price": 3.49, 
            "stock": random.randint(4, 10), 
            "sold": random.randint(18, 42),
            "image": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg"
        }
    }
}

user_data = {}
admin_states = {}
recent_sales_ticker = "🔥 Recent Sale: Rahul (Delhi) bought ChatGPT Plus 1M"

def fake_sales_ticker_updater():
    global recent_sales_ticker
    names = ["Rahul", "Aman", "Alex", "David", "Vikram", "John", "Sameer"]
    cities = ["Mumbai", "New York", "London", "Delhi", "Toronto", "Dubai"]
    products = ["ChatGPT Plus 1M", "Claude Max", "Spotify Premium", "Netflix Premium"]
    while True:
        time.sleep(random.randint(50, 90))
        recent_sales_ticker = f"🔥 Recent Sale: {random.choice(names)} ({random.choice(cities)}) bought {random.choice(products)}"

def get_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0}
    return user_data[user_id]

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
    return "Bot is running successfully!"

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🤖 AI SERVICES", callback_data="cat_ai"),
        types.InlineKeyboardButton("🎬 ENTERTAINMENT", callback_data="cat_entertainment"),
        types.InlineKeyboardButton("💳 TOP-UP WALLET", callback_data="add_funds"),
        types.InlineKeyboardButton("👤 MY DASHBOARD", callback_data="my_account"),
        types.InlineKeyboardButton("📞 SUPPORT", url="https://t.me/ZhiGeAI")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    user = get_user(user_id)

    text = f"""⚡ **XIAO ELITE STORE** ⚡

Welcome, **{name}**! Get premium accounts instantly with automated delivery.

👤 **ACCOUNT ID:** `{user_id}`
💰 **WALLET BALANCE:** `${user['balance']:.2f}`
🛒 **TOTAL ORDERS:** `{user['orders']}`

✨ **Select a category below to browse products:**"""
    
    bot.send_message(message.chat.id, text, reply_markup=get_main_menu(), parse_mode="Markdown")

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
            bot.send_message(ADMIN_ID, f"✅ Successfully sent to user `{target_user_id}`!")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"❌ Failed: `{e}`")
        del admin_states[ADMIN_ID]
        return

    bot.send_message(message.chat.id, "✅ **Payment proof received!** Pending admin verification.", parse_mode="Markdown")
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{user_id}"),
            types.InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{user_id}")
        )
        bot.send_message(
            ADMIN_ID, 
            f"🔔 **New Payment Proof!**\n\n👤 User: {name} ({username_str})\n🆔 ID: `{user_id}`\n💳 Details:\n`{text}`", 
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
    
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if call.data.startswith("approve_") or call.data.startswith("reject_"):
        if user_id != ADMIN_ID:
            return
        action, target_id = call.data.split("_")
        target_id = int(target_id)
        
        if action == "approve":
            try:
                bot.edit_message_text(f"{call.message.text}\n\n✅ **STATUS: APPROVED**", chat_id=chat_id, message_id=message_id, parse_mode="Markdown")
            except:
                bot.send_message(chat_id, "✅ **STATUS: APPROVED**")
            try:
                bot.send_message(target_id, "🎉 Your payment has been approved by the admin!")
            except:
                pass
            admin_states[ADMIN_ID] = {"action": "awaiting_reply_msg", "target_user": target_id}
            bot.send_message(ADMIN_ID, f"✍️ Now send the product details or message for user `{target_id}`:")
        else:
            try:
                bot.edit_message_text(f"{call.message.text}\n\n❌ **STATUS: REJECTED**", chat_id=chat_id, message_id=message_id, parse_mode="Markdown")
            except:
                bot.send_message(chat_id, "❌ **STATUS: REJECTED**")
            try:
                bot.send_message(target_id, "❌ Your payment verification was rejected.")
            except:
                pass
        return
        
    elif call.data == "cat_ai" or call.data == "cat_entertainment":
        cat_key = call.data.split("_")[1]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, item in inventory[cat_key].items():
            stock_label = f"In Stock ({item['stock']})" if item['stock'] > 0 else "Sold Out"
            markup.add(types.InlineKeyboardButton(f"{item['name']} | ${item['price']:.2f} [{stock_label}]", callback_data=f"item_{cat_key}_{key}"))
        markup.add(types.InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="main_menu"))
        
        cat_text = f"📌 **SELECT A PRODUCT FROM {cat_key.upper()} CATEGORY:**"
        try:
            bot.edit_message_text(cat_text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.send_message(chat_id, cat_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("item_"):
        parts = call.data.split("_")
        cat_key = parts[1]
        prod_key = "_".join(parts[2:])
        item = inventory[cat_key].get(prod_key)
        if not item: return
        
        text = f"""📌 **{item['name']}**

💵 **Price:** `${item['price']:.2f}`
📦 **Stock:** `{item['stock']} available`
🔥 **Total Sold:** `{item['sold']}+ units`

Select quantity below:"""

        markup = types.InlineKeyboardMarkup(row_width=5)
        qty_buttons = []
        for q in range(1, 6):
            if item['stock'] >= q:
                qty_buttons.append(types.InlineKeyboardButton(str(q), callback_data=f"qty_{cat_key}_{prod_key}_{q}"))
        if qty_buttons:
            markup.add(*qty_buttons)
        markup.add(types.InlineKeyboardButton("🔙 BACK TO CATALOG", callback_data=f"cat_{cat_key}"))
        
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
        try:
            bot.send_photo(chat_id, item['image'], caption=text, reply_markup=markup, parse_mode="Markdown")
        except Exception:
            bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

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

🏷️ **Product:** {item['name']}
🔢 **Quantity:** `{qty}`
💵 **Total Price:** `${total_price:.2f}`

Click confirm to proceed:"""
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        if item['stock'] >= qty:
            markup.add(types.InlineKeyboardButton(f"⚡ CONFIRM & BUY ({qty}x) - ${total_price:.2f}", callback_data=f"buy_{cat_key}_{prod_key}_{qty}"))
        markup.add(types.InlineKeyboardButton("🪙 TOP-UP WALLET", callback_data="add_funds"))
        markup.add(types.InlineKeyboardButton("🔙 BACK", callback_data=f"item_{cat_key}_{prod_key}"))
        
        try:
            bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

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
            
            text = f"""🎉 **ORDER SUCCESSFUL!**

📦 **Item:** {item['name']} (x{qty})
💸 **Deducted:** `${total_price:.2f}`
💰 **New Balance:** `${user['balance']:.2f}`

Admin notified for instant delivery."""

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🏠 MAIN MENU", callback_data="main_menu"))
            
            try:
                bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup, parse_mode="Markdown")
            except:
                bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
            
            try:
                username = call.from_user.username
                username_str = f"@{username}" if username else "No Username"
                bot.send_message(
                    ADMIN_ID, 
                    f"🛒 **NEW ORDER!**\n\n👤 Buyer: {name} ({username_str})\n🆔 ID: `{user_id}`\n📦 Product: {item['name']} (x{qty})\n💵 Total: `${total_price:.2f}`", 
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Admin order notification error: {e}")
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🪙 TOP-UP VIA CRYPTO", callback_data="crypto_menu"),
                types.InlineKeyboardButton("🏠 MAIN MENU", callback_data="main_menu")
            )
            text = f"""❌ **INSUFFICIENT BALANCE!**

💵 **Required:** `${total_price:.2f}` | 💰 **Your Balance:** `${user['balance']:.2f}`"""
            try:
                bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text, reply_markup=markup, parse_mode="Markdown")
            except:
                bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_funds":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🪙 CRYPTO CURRENCIES", callback_data="crypto_menu"),
            types.InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu")
        )
        funds_text = "💳 **SELECT PAYMENT METHOD:**\n\nChoose your crypto currency to fund your wallet:"
        try:
            bot.edit_message_text(funds_text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.send_message(chat_id, funds_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "crypto_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, wallet in CRYPTO_WALLETS.items():
            markup.add(types.InlineKeyboardButton(wallet["name"], callback_data=f"crypto_pay_{key}"))
        markup.add(types.InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu"))
        try:
            bot.edit_message_text("🪙 **SELECT CRYPTO:**", chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.send_message(chat_id, "🪙 **SELECT CRYPTO:**", reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("crypto_pay_"):
        coin_key = call.data.split("_")[2]
        wallet = CRYPTO_WALLETS.get(coin_key)
        if wallet:
            text = f"""🪙 **PAY VIA {wallet['name']}:**

📍 **Deposit Address:**
`{wallet['address']}`

Send payment and click below to send your TXID."""
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("✅ I HAVE PAID (SEND TXID)", callback_data="tx_submitted"),
                types.InlineKeyboardButton("🔙 BACK", callback_data="crypto_menu")
            )
            try:
                bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")
            except:
                bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "tx_submitted":
        bot.send_message(chat_id, "✍️ Please send your transaction reference / TXID or screenshot details in the chat:", parse_mode="Markdown")

    elif call.data == "my_account":
        text = f"👤 **USER DASHBOARD:**\n\n🆔 ID: `{user_id}`\n💰 Balance: `${user['balance']:.2f}`\n🛒 Total Orders: `{user['orders']}`\n\n{recent_sales_ticker}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 MAIN MENU", callback_data="main_menu"))
        try:
            bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "main_menu":
        text = f"""⚡ **XIAO ELITE STORE** ⚡

Welcome, **{name}**! Get premium accounts instantly with automated delivery.

👤 **ACCOUNT ID:** `{user_id}`
💰 **WALLET BALANCE:** `${user['balance']:.2f}`
🛒 **TOTAL ORDERS:** `{user['orders']}`

✨ **Select a category below to browse products:**"""
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass
        bot.send_message(chat_id, text, reply_markup=get_main_menu(), parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(timeout=60, long_polling_timeout=60), daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    threading.Thread(target=fake_sales_ticker_updater, daemon=True).start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
