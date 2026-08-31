import telebot
from telebot import types

API_TOKEN = "8888661139:AAFfUeYVLG8kwQ4tDp1TWs_a9wWmqEyVuGQ"  # Yahan apna Bot Token daalein
ADMIN_ID = 8852375598

# ----------------- PAYMENT ADDRESSES -----------------
BTC_ADDR = "bc1pj9u898umy3r7fhgrq8w6nemvepcjr0pwl89z6nn66ghqzh9wz9nqudqsla"
USDT_ADDR = "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"
ETH_ADDR = "0x43Be5B53249d33C7A77ab012c6E3508937b87d5A"
SOL_ADDR = "H4cw8xf8A9pg6RTGBbAj2eobWM5HFNhxDKKroLQ1aEVq"
TRX_ADDR = "THs69sCwiGDCDU1sWBA93tL2ct1ynQ6jyF"

bot = telebot.TeleBot(API_TOKEN)
user_data = {}

def main_menu_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🤖 AI Services", callback_data="cat_ai"),
        types.InlineKeyboardButton("🎬 Entertainment & Apps", callback_data="cat_apps"),
        types.InlineKeyboardButton("💬 Official Support", url="https://t.me/ZhiGeAI")
    )
    return markup

def ai_services_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🤖 ChatGPT Pro", callback_data="service_chatgpt"),
        types.InlineKeyboardButton("✨ Gemini Advanced", callback_data="service_gemini"),
        types.InlineKeyboardButton("🔥 Grok AI", callback_data="service_grok"),
        types.InlineKeyboardButton("🧠 DeepSeek V4 API", callback_data="service_deepseek"),
        types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu")
    )
    return markup

def app_services_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎵 Spotify Premium", callback_data="service_spotify"),
        types.InlineKeyboardButton("🎬 Netflix UHD", callback_data="service_netflix"),
        types.InlineKeyboardButton("✂️ CapCut (Out of Stock)", callback_data="service_capcut"),
        types.InlineKeyboardButton("« Back to Main Menu", callback_data="main_menu")
    )
    return markup

def payment_methods_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🪙 USDT (BEP20)", callback_data="pay_usdt"),
        types.InlineKeyboardButton("⚡ TRX (TRC20)", callback_data="pay_trx"),
        types.InlineKeyboardButton("🟣 Solana (SOL)", callback_data="pay_sol"),
        types.InlineKeyboardButton("🔷 Ethereum (ETH)", callback_data="pay_eth"),
        types.InlineKeyboardButton("🟠 Bitcoin (BTC)", callback_data="pay_btc"),
        types.InlineKeyboardButton("« Back", callback_data="main_menu")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "💎 *WELCOME TO XIAO GPT PREMIUM STORE* 💎\n"
        "───────────────────────────────\n"
        f"👋 *Hello, {message.from_user.first_name}!*\n\n"
        "⚡ *Why Choose Us?*\n"
        "├ 🚀 Instant Delivery System\n"
        "├ 🛡️ 100% Genuine Subscriptions\n"
        "└ 💬 24/7 Dedicated Support\n\n"
        "👇 *Please select a category below to continue:*"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("approve_"):
        target_user_id = data.split("_")[1]
        bot.send_message(target_user_id, "🎉 *ORDER APPROVED!*\n\nYour payment has been successfully verified. Credentials will be sent shortly.", parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Approved!")
        bot.edit_message_text(call.message.text + "\n\n✅ *STATUS: APPROVED BY ADMIN*", chat_id, call.message.message_id)
        return

    elif data.startswith("reject_"):
        target_user_id = data.split("_")[1]
        bot.send_message(target_user_id, "❌ *ORDER REJECTED*\n\nYour TxID could not be verified. Contact @ZhiGeAI for help.", parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Rejected!")
        bot.edit_message_text(call.message.text + "\n\n❌ *STATUS: REJECTED BY ADMIN*", chat_id, call.message.message_id)
        return

    if data == "main_menu":
        bot.edit_message_text("💎 *XIAO GPT STORE - MAIN MENU*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=main_menu_keyboard())

    elif data == "cat_ai":
        bot.edit_message_text("🤖 *SELECT AI SERVICE:*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=ai_services_keyboard())

    elif data == "cat_apps":
        bot.edit_message_text("🎬 *SELECT ENTERTAINMENT SERVICE:*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=app_services_keyboard())

    elif data == "service_chatgpt":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("1 Month - $3.5", callback_data="plan_ChatGPT 1 Month ($3.5)"),
            types.InlineKeyboardButton("3 Months - $6.0", callback_data="plan_ChatGPT 3 Months ($6.0)"),
            types.InlineKeyboardButton("« Back", callback_data="cat_ai")
        )
        bot.edit_message_text("🤖 *ChatGPT Plans:*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif data == "service_gemini":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("18 Months - $0.5", callback_data="plan_Gemini 18 Months ($0.5)"), types.InlineKeyboardButton("« Back", callback_data="cat_ai"))
        bot.edit_message_text("✨ *Gemini Plans:*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif data == "service_grok":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("1 Month - $2.0", callback_data="plan_Grok 1 Month ($2.0)"), types.InlineKeyboardButton("« Back", callback_data="cat_ai"))
        bot.edit_message_text("🔥 *Grok Plans:*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif data == "service_deepseek":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("30 Days - $12.0", callback_data="plan_DeepSeek 30 Days ($12.0)"), types.InlineKeyboardButton("« Back", callback_data="cat_ai"))
        bot.edit_message_text("🧠 *DeepSeek Plans:*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif data == "service_spotify":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("1 Month - $0.6", callback_data="plan_Spotify 1 Month ($0.6)"), types.InlineKeyboardButton("« Back", callback_data="cat_apps"))
        bot.edit_message_text("🎵 *Spotify Plans:*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif data == "service_netflix":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("1 Month - $0.8", callback_data="plan_Netflix 1 Month ($0.8)"), types.InlineKeyboardButton("« Back", callback_data="cat_apps"))
        bot.edit_message_text("🎬 *Netflix Plans:*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif data == "service_capcut":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("« Back", callback_data="cat_apps"))
        bot.edit_message_text("❌ *CapCut Out of Stock.*", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif data.startswith("plan_"):
        selected_plan = data.replace("plan_", "")
        user_data[chat_id] = {'plan': selected_plan}
        bot.edit_message_text(f"🧾 *Order:* `{selected_plan}`\n\nSelect Payment Method:", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=payment_methods_keyboard())

    elif data.startswith("pay_"):
        plan_name = user_data.get(chat_id, {}).get('plan', 'Subscription')
        pay_type = data.replace("pay_", "")

        if pay_type == "usdt":
            addr = USDT_ADDR
            coin = "USDT (BEP20)"
        elif pay_type == "trx":
            addr = TRX_ADDR
            coin = "TRX (TRC20)"
        elif pay_type == "sol":
            addr = SOL_ADDR
            coin = "Solana (SOL)"
        elif pay_type == "eth":
            addr = ETH_ADDR
            coin = "Ethereum (ETH)"
        else:
            addr = BTC_ADDR
            coin = "Bitcoin (BTC)"

        text = (
            f"💳 *PAYMENT INSTRUCTIONS*\n"
            f"───────────────────────────────\n"
            f"📦 *Item:* `{plan_name}`\n"
            f"🪙 *Coin:* `{coin}`\n\n"
            f"📍 *Deposit Address:*\n`{addr}`\n"
            f"───────────────────────────────\n"
            f"📌 Send payment and click **'✅ I HAVE PAID'** to submit TxID."
        )
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ I HAVE PAID", callback_data="submit_txid"))
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif data == "submit_txid":
        msg = bot.send_message(chat_id, "✍️ *Please send your Transaction Hash (TxID) in chat:*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_txid)

def process_txid(message):
    chat_id = message.chat.id
    txid = message.text
    user = message.from_user
    plan = user_data.get(chat_id, {}).get('plan', 'Not Specified')

    bot.send_message(chat_id, "⏳ *Verifying payment... You will be notified shortly.*", parse_mode="Markdown")

    admin_markup = types.InlineKeyboardMarkup(row_width=2)
    admin_markup.add(
        types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{chat_id}"),
        types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{chat_id}")
    )

    admin_msg = (
        f"🚨 *NEW ORDER RECEIVED!*\n"
        f"───────────────────────────────\n"
        f"👤 *User:* {user.first_name} (@{user.username})\n"
        f"🆔 *ID:* `{user.id}`\n"
        f"📦 *Plan:* `{plan}`\n"
        f"🧾 *TxID:* `{txid}`"
    )
    bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown", reply_markup=admin_markup)

bot.infinity_polling()
  
