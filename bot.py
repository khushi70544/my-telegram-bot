
import os
import random
import time
import threading
from telebot import TeleBot, types

# Bot Token
BOT_TOKEN = "8888661139:AAFfUeYVLG8kwQ4tDp1TWs_a9wWmqEyVuGQ" # Apna bot token yahan dalein
bot = TeleBot(8888661139)

# Dynamic Inventory Data - Updated Prices & Plans
inventory = {
"chatgpt_1m": {
"name": "ChatGPT Plus 1 Month",
"price": 3.00,
"stock": 5,
"sold": 27
},
"chatgpt_6m": {
"name": "ChatGPT Plus 6 Month",
"price": 5.50,
"stock": 5,
"sold": 27
},
"spotify": {
"name": "Spotify Premium 1 Month",
"price": 0.50,
"stock": 5,
"sold": 27
},
"netflix": {
"name": "Netflix Premium 1 Month",
"price": 0.80,
"stock": 5,
"sold": 27
},
"grok": {
"name": "Grok AI Premium 1 Month",
"price": 4.85,
"stock": 5,
"sold": 27
},
"deepseek": {
"name": "DeepSeek Pro 1 Month",
"price": 12.00,
"stock": 5,
"sold": 27
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

# Broadcast function to all registered users
def broadcast_to_users(msg_text):
for user_id in list(registered_users):
try:
bot.send_message(user_id, msg_text, parse_mode="Markdown")
except Exception:
pass

# Automated Inventory Manager for All Products
def multi_product_inventory_manager():
# PHASE 1: Initial 10-Minute Rush (Stock 5 to 0)
time.sleep(600) # Wait 10 mins
for key in inventory:
if inventory[key]["stock"] > 0:
inventory[key]["sold"] += inventory[key]["stock"]
inventory[key]["stock"] = 0

# PHASE 2 & 3: Out of Stock Notification -> 30 Min Delay -> Restock Loop
while True:
for key, item in inventory.items():
if item["stock"] <= 0:
out_of_stock_msg = (
"⚠️ **OUT OF STOCK!**\n\n"
f"📦 **{item['name']}** is currently completely sold out!\n\n"
f"📊 **Total Sold:** `{item['sold']}`\n"
"⏳ *New stock will be added in exactly 30 minutes. Stay tuned!*"
)
broadcast_to_users(out_of_stock_msg)

# Wait 30 minutes
time.sleep(1800)

# Restock strictly 40 to 50 items max
new_stock = random.randint(40, 50)
item["stock"] += new_stock

restock_msg = (
"📢 **NEW STOCK ADDED!**\n\n"
f"📦 **{item['name']}** is back in stock now!\n\n"
f"🔔 **Current Stock:** `{item['stock']}`\n"
f"📊 **Total Sold:** `{item['sold']}`\n\n"
"🛒 *Order now before it sells out again!* /start"
)
broadcast_to_users(restock_msg)

# Auto-Sales Phase (Every 1-2 hours)
time.sleep(random.randint(3600, 7200))
for key, item in inventory.items():
if item["stock"] > 0:
sold_qty = random.randint(2, 5)
actual_sold = min(item["stock"], sold_qty)
item["stock"] -= actual_sold
item["sold"] += actual_sold # Sold count never decreases

# Main Menu Keyboard
def main_keyboard():
markup = types.InlineKeyboardMarkup(row_width=2)
b1 = types.InlineKeyboardButton("🛒 Product list", callback_data="prod_list")
b2 = types.InlineKeyboardButton("🏦 Top up balance", callback_data="topup")
b3 = types.InlineKeyboardButton("✈️ Purchase history", callback_data="history")
b4 = types.InlineKeyboardButton("🔑 API Key", callback_data="apikey")
b5 = types.InlineKeyboardButton("🌐 Language", callback_data="lang")
b6 = types.InlineKeyboardButton("👤 Referral", callback_data="referral")
b7 = types.InlineKeyboardButton("🚨 Support", callback_data="support")
b8 = types.InlineKeyboardButton("🗣️ Terms of Use", callback_data="terms")

markup.add(b1)
markup.add(b2, b3)
markup.add(b4, b5)
markup.add(b6, b7)
markup.add(b8)
return markup

# Product List Keyboard - All Products with Updated Pricing
def products_keyboard():
markup = types.InlineKeyboardMarkup(row_width=1)

for key, item in inventory.items():
btn_text = f"🤖 {item['name']} | ${item['price']:.2f} | 📦 {item['stock']}"
markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"buy_{key}"))

back = types.InlineKeyboardButton("⬅️ Menu", callback_data="main_menu")
markup.add(back)
return markup

# Cancel/Menu Keyboard
def sub_keyboard():
markup = types.InlineKeyboardMarkup(row_width=2)
b1 = types.InlineKeyboardButton("❌ Cancel", callback_data="prod_list")
b2 = types.InlineKeyboardButton("⬅️ Menu", callback_data="main_menu")
markup.add(b1, b2)
return markup

# /start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
u = get_user(message.from_user.id, message.from_user.first_name)
caption = f"🌙 **Good evening, {message.from_user.first_name}**\n\n🤑 Balance: **${u['balance']:.2f}**\n🏪 Total orders: **{u['orders']}**"
banner_url = "
https://picsum.photos/800/400
"

try:
bot.send_photo(message.chat.id, banner_url, caption=caption, parse_mode="Markdown", reply_markup=main_keyboard())
except Exception:
bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=main_keyboard())

# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
u = get_user(call.from_user.id, call.from_user.first_name)

if call.data == "main_menu":
text = f"🌙 **Good evening, {call.from_user.first_name}**\n\n🤑 Balance: **${u['balance']:.2f}**\n🏪 Total orders: **{u['orders']}**"
bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, parse_mode="Markdown", reply_markup=main_keyboard())

elif call.data == "prod_list":
text = f"🛒 **CATEGORIES & PRODUCTS**\n\n🤑 Balance: **${u['balance']:.2f}**\n\nChoose a product:"
bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, parse_mode="Markdown", reply_markup=products_keyboard())

elif call.data.startswith("buy_"):
prod_key = call.data.replace("buy_", "")
if prod_key in inventory:
u['state'] = 'awaiting_quantity'
u['selected_prod'] = prod_key
item = inventory[prod_key]

max_buy = min(3, item['stock']) if item['stock'] > 0 else 0
desc = (
f"🤖 **{item['name']}**\n"
f"💲 Price: **${item['price']:.2f}**\n"
f"🔔 Stock: **{item['stock']}**\n"
f"📊 Sold: **{item['sold']}**\n"
f"🔔 Buy: **1-{max_buy}**\n\n"
"🗣️ **Description:**\n"
"```\n🔒 Product delivery Method:\nMail--Pass--2FA\n"
"🎁 Bulk Price: Direct DM to Admin\n@aitoolsandnewsbydavid\n"
"👍 Only Login Warranty is Provided.\n```\n\n"
f"✏️ **Enter quantity (1-{max_buy}):**" if max_buy > 0 else "\n❌ **Currently Out of Stock!**"
)
bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=desc, parse_mode="Markdown", reply_markup=sub_keyboard())

# Text Handler for Quantity Input
@bot.message_handler(func=lambda m: True)
def handle_text(message):
u = get_user(message.from_user.id, message.from_user.first_name)
if u.get('state') == 'awaiting_quantity':
prod_key = u.get('selected_prod')
item = inventory.get(prod_key)

if not item or item['stock'] <= 0:
bot.send_message(message.chat.id, "❌ Sorry, this item is out of stock right now.")
u['state'] = None
return

if message.text.isdigit():
qty = int(message.text)
max_buy = min(3, item['stock'])
if 1 <= qty <= max_buy:
u['state'] = None
bot.send_message(message.chat.id, f"✅ Order placed for **{qty}x {item['name']}**! Please add balance to proceed.", parse_mode="Markdown")
else:
bot.send_message(message.chat.id, f"❌ Invalid quantity. Enter between 1 and {max_buy}:")
else:
bot.send_message(message.chat.id, "❌ Please enter a valid number.")

# Port listener and background threads execution
if __name__ == '__main__':
import http.server, socketserver

# Start Dummy HTTP Server for Render Port Check
def run_dummy_server():
port = int(os.environ.get("PORT", 10000))
handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", port), handler) as httpd:
httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# Start Multi-Product Inventory Manager Thread
threading.Thread(target=multi_product_inventory_manager, daemon=True).start()

bot.infinity_polling()
