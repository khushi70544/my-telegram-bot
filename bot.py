import os
import random
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telebot import TeleBot, types

# Bot Token
BOT_TOKEN = "8888661139:AAHyELdLZdJJDoYEMyM4LiDjTJt9SodxTIU"
bot = TeleBot(BOT_TOKEN)

# Admin Telegram ID
ADMIN_ID = 8852375598

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

# Stock is strictly kept between 5 and 10
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
        "success": "🎉 **Order Placed Successfully!**\n\n📦 **Item:** {item_name}\n💸 **Deducted:** `${price:.2f}`\n💰 **New Balance:** `${balance:.2f}`\n\n⏳ Admin has been notified for approval."
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
        "success": "🎉 **订单提交成功！**\n\n📦 **商品:** {item_name}\n💸 **扣除:** `${price:.2f}`\n💰 **新余额:** `${balance:.2f}`\n\n⏳ 已通知管理员审核。"
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
        "success": "🎉 **Pesanan Berhasil Dibuat!**\n\n📦 **Item:** {item_name}\n💸 **Terpotong:** `${price:.2f}`\n💰 **Saldo Baru:** `${balance:.2f}`\n\n⏳ Admin telah diberitahu untuk persetujuan."
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
        "success": "🎉 **Заказ успешно оформлен!**\n\n📦 **Товар:** {item_name}\n💸 **Списано:** `${price:.2f}`\n💰 **Новый баланс:** `${balance:.2f}`\n\n⏳ Администратор уведомлен для подтверждения."
    }
}

user_data = {}
registered_users = set()

def get_user(user_id, name):
    registered_users.add(user_id)
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0.00, "orders": 0, "lang": "en"}
    return user_data[user_id]

def auto_hourly_sales():
    while True:
        time.sleep(3600)
        try:
            cat_key = random.choice(list(inventory.keys()))
            prod_key = random.choice(list(inventory[cat_key].keys()))
            item = inventory[cat_key][prod_key]
            
            if item["stock"] > 0:
                item["stock"] -= 1
                item["sold"] += 1
            
            if item["stock"] > 10:
                item["stock"] = random.randint(5, 10)
        except Exception:
            pass

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
    except Exception as e:
        print(f"Admin start notification error: {e}")

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
    except Exception as e:
        print(f"Admin payment proof notification error: {e}")

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
        langs = ["en", "zh", "id", "ru"]
        current_idx = langs.index(user["lang"]) if user["lang"] in langs else 0
        next_idx = (current_idx + 1) % len(langs)
        user["lang"] = langs[next_idx]
        
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
        except Exception:
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
            except Exception as e:
                print(f"Admin order notification error: {e}")
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🪙 Pay via Crypto", callback_data="crypto_menu"),
                types.InlineKeyboardButton(t["back_menu"], callback_data="main_menu")
            )
            bot.edit_message_text(t["insufficient"].format(price=item['price'], balance=user['balance']), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

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
    
    sales_thread = threading.Thread(target=auto_hourly_sales, daemon=True)
    sales_thread.start()
    
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            time.sleep(3)
