import os
import random
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telebot import TeleBot, types

# Bot Token
BOT_TOKEN = "8888661139:AAFluKA60FPKddBVI1WlZskX3s2W5W6i-XU" # Apna token yahan dalein
bot = TeleBot(BOT_TOKEN)

# Admin Telegram ID
ADMIN_ID = 8852375598

# Your Real Crypto Addresses
CRYPTO_WALLETS = {
    "btc": {"name": "Bitcoin (BTC)", "address": "bc1pj9u898umy3r7fhgrq8w6nemvepcjr0pwl89z6nn66ghqzh9wz9nqudqsla"},
    "usdt": {"name": "USDT (ERC20/BEP20)", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "eth": {"name": "Ethereum (ETH)", "address": "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"},
    "sol": {"name": "Solana (SOL)", "address": "H4cw8xf8A9pg6RTGBbAj2eobWM5HFNhxDKKroLQ1aEVq"},
    "trx": {"name": "Tron (TRX)", "address": "THs69sCwiGDCDU1sWBA93tL2ct1ynQ6jyF"}
}

# Stock inventory
inventory = {
    "ai": {
        "chatgpt_1m": {"name": "ChatGPT Plus 1 Month", "price": 3.00, "stock": random.randint(5, 10), "sold": random.randint(20, 35)},
        "chatgpt_6m": {"name": "ChatGPT Plus 6 Month", "price": 5.50, "stock": random.randint(5, 10), "sold": random.randint(12, 28)},
        "chatgpt_pro5": {"name": "ChatGPT Pro ×5", "price": 30.00, "stock": random.randint(5, 10), "sold": random.randint(3, 10)},
        "chatgpt_pro20": {"name": "ChatGPT Pro ×20", "price": 70.00, "stock": random.randint(5, 10), "sold": random.randint(1, 5)},
        "grok": {"name": "Grok AI Premium 1 Month", "price": 4.85, "stock": random.randint(5, 10), "sold": random.randint(8, 22)},
        "deepseek": {"name": "DeepSeek Pro 1 Month", "price": 12.00, "stock": random.randint(5, 10), "sold": random.randint(5, 15)},
        "claude_max_5x": {"name": "Claude Max ×5", "price": 15.00, "stock": random.randint(5, 10), "sold": random.randint(5, 15)},
        "claude_max_20x": {"name": "Claude Max ×20", "price": 70.00, "stock": random.randint(5, 10), "sold": random.randint(1, 8)}
    },
    "entertainment": {
        "spotify": {"name": "Spotify Premium 1 Month", "price": 0.50, "stock": random.randint(5, 10), "sold": random.randint(35, 60)},
        "netflix": {"name": "Netflix Premium 1 Month", "price": 0.80, "stock": random.randint(5, 10), "sold": random.randint(18, 42)}
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
        "deposit_title": "🪙 **Select Payment Gateway:**\n\nChoose your preferred crypto currency below:",
        "crypto_menu": "🪙 **Select Crypto Currency:**\n\nChoose which crypto you want to send:",
        "crypto_text": "🪙 **Pay via {coin_name}:**\n\n📍 **Address:**\n`{address}`\n\n📌 Send payment, then click '✅ I HAVE PAID' or type your TxID.",
        "paid_btn": "✅ I HAVE PAID",
        "insufficient": "❌ **Insufficient Balance!**\n\nRequired: `${price:.2f}` | Balance: `${balance:.2f}`\n\n📍 **Choose top-up method:**",
        "success": "🎉 **Order Placed Successfully!**\n\n📦 **Item:** {item_name} (Qty: {qty})\n💸 **Total Deducted:** `${total_price:.2f}`\n💰 **New Balance:** `${balance:.2f}`\n\n⏳ Admin has been notified."
    },
    "zh": {
        "welcome": "⚡ **欢迎来到 Xiao Elite Store, {name}!** ⚡\n\n👤 **账户 ID:** `{user_id}`\n💰 **余额:** `${balance:.2f}`\n🛒 **订单:** `{orders}`\n\n✨ 请在下方选择一个选项：",
        "browse": "🤖 AI 服务",
        "entertainment": "🎬 娱乐服务",
        "topup": "💳 充值钱包",
        "dashboard": "👤 我的面板",
        "lang_btn": "🌐 语言: 中文",
        "support": "📞 客服支持",
        "catalog_title": "✨ **商店目录** ✨\n\n请选择分类：",
        "back_menu": "🔙 主菜单",
        "account_title": "👤 **面板:**\n\n🆔 ID: `{user_id}`\n💰 余额: `${balance:.2f}`\n🛒 订单: `{orders}`",
        "deposit_title": "🪙 **选择支付网关:**\n\n请在下方选择您偏好的加密货币：",
        "crypto_menu": "🪙 **选择加密货币:**\n\n请选择您要发送的加密货币：",
        "crypto_text": "🪙 **通过 {coin_name} 支付:**\n\n📍 **地址:**\n`{address}`\n\n📌 请发送付款，然后点击 '✅ 我已付款' 或发送交易哈希 (TxID)。",
        "paid_btn": "✅ 我已付款",
        "insufficient": "❌ **余额不足！**\n\n需要: `${price:.2f}` | 余额: `${balance:.2f}`\n\n📍 **请选择充值方法：**",
        "success": "🎉 **订单提交成功！**\n\n📦 **商品:** {item_name} (数量: {qty})\n💸 **总扣除:** `${total_price:.2f}`\n💰 **新余额:** `${balance:.2f}`\n\n⏳ 已通知管理员。"
    },
    "id": {
        "welcome": "⚡ **Selamat datang di Xiao Elite Store, {name}!** ⚡\n\n👤 **ID Akun:** `{user_id}`\n💰 **Saldo:** `${balance:.2f}`\n🛒 **Pesanan:** `{orders}`\n\n✨ Pilih opsi di bawah ini:",
        "browse": "🤖 Layanan AI",
        "entertainment": "🎬 Hiburan",
        "topup": "💳 Top-up Saldo",
        "dashboard": "👤 Dashboard Saya",
        "lang_btn": "🌐 Bahasa: Indonesia",
        "support": "📞 Dukungan",
        "catalog_title": "✨ **Katalog Toko** ✨\n\nPilih kategori:",
        "back_menu": "🔙 Menu Utama",
        "account_title": "👤 **Dashboard:**\n\n🆔 ID: `{user_id}`\n💰 Saldo: `${balance:.2f}`\n🛒 Pesanan: `{orders}`",
        "deposit_title": "🪙 **Pilih Metode Pembayaran:**\n\nPilih mata uang kripto pilihan Anda di bawah ini:",
        "crypto_menu": "🪙 **Pilih Mata Uang Kripto:**\n\nPilih kripto yang ingin Anda kirim:",
        "crypto_text": "🪙 **Bayar via {coin_name}:**\n\n📍 **Alamat:**\n`{address}`\n\n📌 Kirim pembayaran, lalu klik '✅ Saya Sudah Bayar' atau kirim TxID Anda.",
        "paid_btn": "✅ Saya Sudah Bayar",
        "insufficient": "❌ **Saldo Tidak Cukup!**\n\nDibutuhkan: `${price:.2f}` | Saldo: `${balance:.2f}`\n\n📍 **Pilih metode top-up:**",
        "success": "🎉 **Pesanan Berhasil Dibuat!**\n\n📦 **Item:** {item_name} (Jml: {qty})\n💸 **Total Terpotong:** `${total_price:.2f}`\n💰 **Saldo Baru:** `${balance:.2f}`\n\n⏳ Admin telah diberitahu."
    },
    "ru": {
        "welcome": "⚡ **Добро пожаловать в Xiao Elite Store, {name}!** ⚡\n\n👤 **ID аккаунта:** `{user_id}`\n💰 **Баланс:** `${balance:.2f}`\n🛒 **Заказы:** `{orders}`\n\n✨ Выберите вариант ниже:",
        "browse": "🤖 ИИ Сервисы",
        "entertainment": "🎬 Развлечения",
        "topup": "💳 Пополнить баланс",
        "dashboard": "👤 Мой кабинет",
        "lang_btn": "🌐 Язык: Русский",
        "support": "📞 Поддержка",
        "catalog_title": "✨ **Каталог товаров** ✨\n\nВыберите категорию:",
        "back_menu": "🔙 Главное меню",
        "account_title": "👤 **Кабинет:**\n\n🆔 ID: `{user_id}`\n💰 Баланс: `${balance:.2f}`\n🛒 Заказы: `{orders}`",
        "deposit_title": "🪙 **Выберите способ оплаты:**\n\nВыберите криптовалюту ниже:",
        "crypto_menu": "🪙 **Выберите криптовалюту:**\n\nВыберите нужную криптовалюту для отправки:",
        "crypto_text": "🪙 **Оплата через {coin_name}:**\n\n📍 **Адрес:**\n`{address}`\n\n📌 Отправьте платеж, затем нажмите '✅ Я оплатил' или отправьте TxID.",
        "paid_btn": "✅ Я оплатил",
        "insufficient": "❌ **Недостаточно средств!**\n\nТребуется: `${price:.2f}` | Баланс: `${balance:.2f}`\n\n📍 **Выберите способ пополнения:**",
        "success": "🎉 **Заказ успешно оформлен!**\n\n📦 **Товар:** {item_name} (Кол-во: {qty})\n💸 **Списано:** `${total_price:.2f}`\n💰 **Новый баланс:** `${balance:.2f}`\n\n⏳ Администратор уведомлен."
    }
}

user_data = {}
admin_states = {}

def get_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0, "lang": "en"}
    return user_data[user_id]

# Har 10 se 20 minute me stock kam/jyada karne wala function
def auto_stock_updater():
    while True:
        sleep_time = random.randint(600, 1200) # 10 to 20 minutes (in seconds)
        time.sleep(sleep_time)
        try:
            cat_key = random.choice(list(inventory.keys()))
            prod_key = random.choice(list(inventory[cat_key].keys()))
            item = inventory[cat_key][prod_key]
            
            # Decide randomly whether to add stock (+2 to +4) or reduce (-1 to -2)
            action_type = random.choice(["add", "reduce"])
            
            if action_type == "add":
                added_qty = random.randint(2, 4)
                item["stock"] += added_qty
                msg = f"📈 **Stock Updated (Auto):**\n\n📦 Product: `{item['name']}`\n➕ Added: `+{added_qty}`\n📦 New Stock: `{item['stock']}`"
            else:
                reduced_qty = random.randint(1, 2)
                if item["stock"] >= reduced_qty:
                    item["stock"] -= reduced_qty
                msg = f"📉 **Stock Updated (Auto):**\n\n📦 Product: `{item['name']}`\n➖ Reduced: `-{reduced_qty}`\n📦 New Stock: `{item['stock']}`"
            
            # Admin ko update bhejo
            bot.send_message(ADMIN_ID, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"Stock updater error: {e}")

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
    user = get_user(user_id)
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
    username = message.from_user.username
    username_str = f"@{username}" if username else "No Username"
    text = message.text

    if text.startswith('/'):
        return

    # Admin reply to user after approval
    if user_id == ADMIN_ID and ADMIN_ID in admin_states and admin_states[ADMIN_ID].get("action") == "awaiting_reply_msg":
        target_user_id = admin_states[ADMIN_ID]["target_user"]
        try:
            bot.send_message(target_user_id, f"🎉 **Admin Message / Product Details:**\n\n{text}", parse_mode="Markdown")
            bot.send_message(ADMIN_ID, f"✅ Message successfully sent to user `{target_user_id}`!")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"❌ Failed to send message: {e}")
        del admin_states[ADMIN_ID]
        return

    bot.send_message(message.chat.id, f"✅ **Payment Proof / TxID Received:** `{text}`\n⏳ Verification pending by admin.", parse_mode="Markdown")
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
            types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}")
        )
        bot.send_message(
            ADMIN_ID, 
            f"🔔 **New Payment Proof Submitted!**\n\n👤 **User:** {name}\n🔗 **Username:** {username_str}\n🆔 **ID:** `{user_id}`\n💳 **Details:** `{text}`", 
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
    lang = user["lang"]
    t = lang_text[lang]
    
    bot.answer_callback_query(call.id)
    
    if call.data.startswith("approve_") or call.data.startswith("reject_"):
        if user_id != ADMIN_ID:
            return
        action, target_id = call.data.split("_")
        target_id = int(target_id)
        
        if action == "approve":
            bot.edit_message_text(f"{call.message.text}\n\n✅ **Status:** APPROVED", chat_id=call.message.chat.id, message_id=call.message.message_id)
            try:
                bot.send_message(target_id, "🎉 **Your payment has been APPROVED by the Admin!**")
            except:
                pass
            
            admin_states[ADMIN_ID] = {"action": "awaiting_reply_msg", "target_user": target_id}
            bot.send_message(ADMIN_ID, f"✍️ Now send the message/product details you want to send to User `{target_id}`:")
        else:
            bot.edit_message_text(f"{call.message.text}\n\n❌ **Status:** REJECTED", chat_id=call.message.chat.id, message_id=call.message.message_id)
            try:
                bot.send_message(target_id, "❌ **Your payment verification was rejected by Admin.**")
            except:
                pass
        return

    if call.data == "toggle_lang":
        langs = ["en", "zh", "id", "ru"]
        current_idx = langs.index(user["lang"]) if user["lang"] in langs else 0
        user["lang"] = langs[(current_idx + 1) % len(langs)]
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
        try:
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            pass
        return
        
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
        
        text = f"📌 **{item['name']}**\n💵 Price per item: `${item['price']:.2f}`\n📦 Stock available: `{item['stock']}`\n\n🔢 **Select Quantity:**"
        markup = types.InlineKeyboardMarkup(row_width=5)
        
        qty_buttons = []
        for q in range(1, 6):
            if item['stock'] >= q:
                qty_buttons.append(types.InlineKeyboardButton(str(q), callback_data=f"qty_{cat_key}_{prod_key}_{q}"))
        markup.add(*qty_buttons)
        markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data=f"cat_{cat_key}"))
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("qty_"):
        _, cat_key, prod_key, qty_str = call.data.split("_", 3)
        qty = int(qty_str)
        item = inventory[cat_key].get(prod_key)
        if not item: return

        total_price = item["price"] * qty
        text = f"📌 **{item['name']}**\n🔢 Quantity: `{qty}`\n💵 Total Price: `${total_price:.2f}`\n📦 Stock: `{item['stock']}`"
        markup = types.InlineKeyboardMarkup(row_width=1)
        if item['stock'] >= qty:
            markup.add(types.InlineKeyboardButton(f"⚡ Confirm & Buy ({qty}x)", callback_data=f"buy_{cat_key}_{prod_key}_{qty}"))
        markup.add(types.InlineKeyboardButton("🪙 Top-up Wallet", callback_data="add_funds"))
        markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data=f"item_{cat_key}_{prod_key}"))
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("buy_"):
        _, cat_key, prod_key, qty_str = call.data.split("_", 3)
        qty = int(qty_str)
        item = inventory[cat_key].get(prod_key)
        total_price = item["price"] * qty

        if user["balance"] >= total_price:
            user["balance"] -= total_price
            user["orders"] += 1
            item["stock"] -= qty
            item["sold"] += qty
            
            text = t["success"].format(item_name=item['name'], qty=qty, total_price=total_price, balance=user['balance'])
            markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu"))
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            
            try:
                username = call.from_user.username
                username_str = f"@{username}" if username else "No Username"
                bot.send_message(
                    ADMIN_ID, 
                    f"🛒 **New Order Placed!**\n\n👤 **Buyer:** {name}\n🔗 **Username:** {username_str}\n🆔 **ID:** `{user_id}`\n📦 **Product:** {item['name']} (x{qty})\n💵 **Total:** `${total_price:.2f}`", 
                    parse_mode="Markdown"
                )
            except Exception as e:
                print(f"Admin order notification error: {e}")
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🪙 Pay via Crypto", callback_data="crypto_menu"),
                types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu")
            )
            bot.edit_message_text(t["insufficient"].format(price=total_price, balance=user['balance']), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "add_funds":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🪙 Crypto Currencies", callback_data="crypto_menu"),
            types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu")
        )
        bot.edit_message_text(t["deposit_title"], chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "crypto_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, wallet in CRYPTO_WALLETS.items():
            markup.add(types.InlineKeyboardButton(wallet["name"], callback_data=f"crypto_pay_{key}"))
        markup.add(types.InlineKeyboardButton(t["back_menu"], callback_data="add_funds"))
        bot.edit_message_text
