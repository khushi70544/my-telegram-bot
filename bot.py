import os
import random
import time
import threading
from flask import Flask
from telebot import TeleBot, types

# Bot Token
BOT_TOKEN = "8888661139:AAFluKA60FPKddBVI1WlZskX3s2W5W6i-XU" 
bot = TeleBot(BOT_TOKEN)

# Admin Telegram ID
ADMIN_ID = 8852375598

# Crypto Wallets
CRYPTO_WALLETS = {
    "btc": {"name": "🪙 Bitcoin (BTC)", "address": "bc1pj9u898umy3r7fhgrq8w6nemvepcjr0pwl89z6nn66ghqzh9wz9nqudqsla"},
    "usdt": {"name": "💵 USDT (ERC20/BEP20)", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "eth": {"name": "💎 Ethereum (ETH)", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "sol": {"name": "🟣 Solana (SOL)", "address": "H4cw8xf8A9pg6RTGBbAj2eobWM5HFNhxDKKroLQ1aEVq"},
    "trx": {"name": "🔴 Tron (TRX)", "address": "THs69sCwiGDCDU1sWBA93tL2ct1ynQ6jyF"}
}

# Inventory with Updated Prices
inventory = {
    "ai": {
        "chatgpt_1m": {"name": "🤖 ChatGPT Plus 1 Month", "price": 3.40, "stock": random.randint(5, 10), "sold": random.randint(20, 35)},
        "chatgpt_6m": {"name": "🤖 ChatGPT Plus 6 Month", "price": 13.90, "stock": random.randint(5, 10), "sold": random.randint(12, 28)},
        "chatgpt_pro5": {"name": "⚡ ChatGPT Pro ×5", "price": 12.65, "stock": random.randint(5, 10), "sold": random.randint(3, 10)},
        "chatgpt_pro20": {"name": "🚀 ChatGPT Pro ×20", "price": 30.80, "stock": random.randint(5, 10), "sold": random.randint(1, 5)},
        "grok": {"name": "🧠 Grok AI Premium 1 Month", "price": 5.99, "stock": random.randint(5, 10), "sold": random.randint(8, 22)},
        "deepseek": {"name": "🔬 DeepSeek Pro 1 Month", "price": 9.99, "stock": random.randint(5, 10), "sold": random.randint(5, 15)},
        "claude_max_5x": {"name": "🔥 Claude Max ×5", "price": 14.50, "stock": random.randint(5, 10), "sold": random.randint(5, 15)},
        "claude_max_20x": {"name": "🌟 Claude Max ×20", "price": 35.00, "stock": random.randint(5, 10), "sold": random.randint(1, 8)}
    },
    "entertainment": {
        "spotify": {"name": "🎧 Spotify Premium 1 Month", "price": 1.99, "stock": random.randint(5, 10), "sold": random.randint(35, 60)},
        "netflix": {"name": "🍿 Netflix Premium 1 Month", "price": 3.49, "stock": random.randint(5, 10), "sold": random.randint(18, 42)}
    }
}

user_data = {}
admin_states = {}

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

# Flask app for Render Web Service
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running successfully!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    user = get_user(user_id)

    text = f"⚡ **WELCOME TO XIAO ELITE STORE, {name.upper()}!** ⚡\n\n👤 **ACCOUNT ID:** `{user_id}`\n💰 **WALLET BALANCE:** `${user['balance']:.2f}`\n🛒 **TOTAL ORDERS:** `{user['orders']}`\n\n✨ **PLEASE SELECT AN OPTION BELOW:**"
    
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
        bot.edit_message_text("✨ **STORE CATALOG:**\n\n📌 **CHOOSE A CATEGORY BELOW:**", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("item_"):
        parts = call.data.split("_")
        cat_key = parts[1]
        prod_key = "_".join(parts[2:])
        item = inventory[cat_key].get(prod_key)
        if not item: return
        
        text = f"📌 **PRODUCT DETAILS:**\n\n🏷️ **NAME:** {item['name']}\n💵 **PRICE:** `${item['price']:.2f}`\n📦 **STOCK:** `{item['stock']}`\n\n🔢 **SELECT QUANTITY BELOW:**"
        markup = types.InlineKeyboardMarkup(row_width=5)
        qty_buttons = []
        for q in range(1, 6):
            if item['stock'] >= q:
                qty_buttons.append(types.InlineKeyboardButton(str(q), callback_data=f"qty_{cat_key}_{prod_key}_{q}"))
        markup.add(*qty_buttons)
        markup.add(types.InlineKeyboardButton("🔙 BACK TO CATALOG", callback_data=f"cat_{cat_key}"))
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("qty_"):
        parts = call.data.split("_")
        qty_str = parts[-1]
        cat_key = parts[1]
        prod_key = "_".join(parts[2:-1])
        
        qty = int(qty_str)
        item = inventory[cat_key].get(prod_key)
        if not item: return

        total_price = item["price"] * qty
        text = f"📌 **ORDER SUMMARY:**\n\n🏷️ **PRODUCT:** {item['name']}\n🔢 **QUANTITY:** `{qty}`\n💵 **TOTAL PRICE:** `${total_price:.2f}`\n📦 **AVAILABLE STOCK:** `{item['stock']}`"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        if item['stock'] >= qty:
            markup.add(types.InlineKeyboardButton(f"⚡ CONFIRM & BUY ({qty}x)", callback_data=f"buy_{cat_key}_{prod_key}_{qty}"))
        markup.add(types.InlineKeyboardButton("🪙 TOP-UP WALLET", callback_data="add_funds"))
        markup.add(types.InlineKeyboardButton("🔙 BACK TO PRODUCT", callback_data=f"item_{cat_key}_{prod_key}"))
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
            
            text = f"🎉 **ORDER PLACED SUCCESSFULLY!**\n\n📦 **ITEM:** {item['name']} (Qty: {qty})\n💸 **TOTAL DEDUCTED:** `${total_price:.2f}`\n💰 **NEW BALANCE:** `${user['balance']:.2f}`\n\n⏳ **ADMIN HAS BEEN NOTIFIED.**"
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🏠 BACK TO MAIN MENU", callback_data="main_menu"))
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
            text = f"❌ **INSUFFICIENT WALLET BALANCE!**\n\n💵 **REQUIRED:** `${total_price:.2f}` | 💰 **YOUR BALANCE:** `${user['balance']:.2f}`\n\n📍 **CHOOSE TOP-UP METHOD BELOW:**"
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_funds":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🪙 CRYPTO CURRENCIES", callback_data="crypto_menu"),
            types.InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="main_menu")
        )
        bot.edit_message_text("💳 **SELECT PAYMENT GATEWAY:**\n\n📌 **CHOOSE YOUR PREFERRED CRYPTO CURRENCY BELOW:**", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

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
            text = f"🪙 **PAY VIA {wallet['name']}:**\n\n📍 **DEPOSIT ADDRESS:**\n`{wallet['address']}`\n\n📌 **SEND PAYMENT, THEN CLICK 'I HAVE PAID' OR TYPE YOUR TXID.**"
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
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "main_menu":
        text = f"⚡ **WELCOME TO XIAO ELITE STORE, {name.upper()}!** ⚡\n\n👤 **ACCOUNT ID:** `{user_id}`\n💰 **WALLET BALANCE:** `${user['balance']:.2f}`\n🛒 **TOTAL ORDERS:** `{user['orders']}`\n\n✨ **PLEASE SELECT AN OPTION BELOW:**"
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🤖 AI SERVICES", callback_data="cat_ai"),
            types.InlineKeyboardButton("🎬 ENTERTAINMENT", callback_data="cat_entertainment"),
            types.InlineKeyboardButton("💳 TOP-UP WALLET", callback_data="add_funds"),
            types.InlineKeyboardButton("👤 MY DASHBOARD", callback_data="my_account"),
            types.InlineKeyboardButton("📞 SUPPORT", url="https://t.me/ZhiGeAI")
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    bot_thread = threading.Thread(target=lambda: bot.infinity_polling(timeout=60, long_polling_timeout=60), daemon=True)
    bot_thread.start()
    
    stock_thread = threading.Thread(target=auto_stock_updater, daemon=True)
    stock_thread.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
            
