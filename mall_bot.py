import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN_MALL')
TARGET_GROUP_ID = -1002477011468
TOPIC_ID = 7565

# Data Mall (Kategori & Kedai)
MALL_DATA = {
    "food": {
        "text": "🍴 **Food & Relaxation**\nTempat untuk menjamu selera dan berehat.",
        "items": [
            {"name": "Food Court", "img": "https://i.pinimg.com/1200x/1f/e1/e7/1fe1e71db44391066b1c9d4b18b32d1f.jpg", "pin": "https://pin.it/4kR5X6Z0H"},
            {"name": "Roof Garden", "img": "https://i.pinimg.com/736x/1b/68/de/1b68dedbb98a3ad38dded21f6181d126.jpg", "pin": "https://pin.it/6YyXJz8qB"}
        ]
    },
    "clothing": {
        "text": "👕 **Clothing & Fashion**\nKoleksi pakaian terkini, dari gaya Straight Cut hingga Baggy.",
        "items": [
            {"name": "Urban Wear (Baggy Style)", "img": "https://i.pinimg.com/736x/49/96/51/499651406e9c5aa2376e5f08725ec424.jpg", "pin": "https://pin.it/2mZ7O4L9P"},
            {"name": "Classic Tailor (Straight Cut)", "img": "https://i.pinimg.com/736x/bc/d3/04/bcd3047af1ff9b8fe6e003b3c39d4a66.jpg", "pin": "https://pin.it/3nK9R2V5X"},
            {"name": "Aesthetic Boutique", "img": "https://i.pinimg.com/736x/9d/f8/56/9df85631e53cdb08a833d78c147974b1.jpg", "pin": "https://pin.it/5mB2L8K"}
        ]
    },
    "basic": {
        "text": "🚽 **Basic Facilities**\nKemudahan asas untuk keselesaan anda.",
        "items": [
            {"name": "Toilets", "img": "https://i.pinimg.com/736x/85/24/6b/85246be41933fdb50c75fdc24e5921a4.jpg", "pin": "https://pin.it/toilet"}
        ]
    },
    "fun": {
        "text": "🎬 **Entertainment & Leisure**\nHiburan dan kawasan permainan.",
        "items": [
            {"name": "Cinema (Indonesia)", "img": "https://i.pinimg.com/736x/14/d7/ec/14d7ecea6ac171775bd978d2a9b8dca4.jpg", "pin": "https://pin.it/cinema_indo"},
            {"name": "Arcade Center", "img": "https://i.pinimg.com/1200x/35/6c/f1/356cf1d433d7d94d6cbd887b28754cd8.jpg", "pin": "https://pin.it/arcade_game"}
        ]
    }
}

logging.basicConfig(level=logging.INFO)

async def post_init(application: Application):
    await application.bot.set_my_commands([BotCommand("start", "Masuk ke Mall")])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🍴 Food & Relaxation", callback_data='menu_food')],
        [InlineKeyboardButton("👕 Clothing & Fashion", callback_data='menu_clothing')],
        [InlineKeyboardButton("🚽 Basic Facilities", callback_data='menu_basic')],
        [InlineKeyboardButton("🎬 Entertainment", callback_data='menu_fun')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "🏢 **Selamat Datang ke Fam Ravlyn Mall!**\nSila pilih tingkat atau kategori yang ingin anda lawati:"
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("menu_"):
        category = data.split("_")[1]
        cat_info = MALL_DATA[category]
        keyboard = []
        for item in cat_info['items']:
            keyboard.append([InlineKeyboardButton(item['name'], callback_data=f"item_{category}_{cat_info['items'].index(item)}")])
        keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data='back_main')])
        await query.edit_message_text(cat_info['text'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data.startswith("item_"):
        _, cat, idx = data.split("_")
        item = MALL_DATA[cat]['items'][int(idx)]
        keyboard = [
            [InlineKeyboardButton("📍 Lihat di Pinterest", url=item['pin'])],
            [InlineKeyboardButton("⬅️ Kembali", callback_data=f"menu_{cat}")]
        ]
        try:
            await context.bot.send_photo(
                chat_id=query.message.chat_id,
                message_thread_id=TOP_ID,
                photo=item['img'],
                caption=f"🏬 **{item['name']}**\nSelamat datang ke butik kami!",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        except Exception as e:
            await query.edit_message_text(f"🏬 **{item['name']}**\n[Klik Pinterest]({item['pin']})", 
                                         reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif data == "back_main":
        keyboard = [
            [InlineKeyboardButton("🍴 Food & Relaxation", callback_data='menu_food')],
            [InlineKeyboardButton("👕 Clothing & Fashion", callback_data='menu_clothing')],
            [InlineKeyboardButton("🚽 Basic Facilities", callback_data='menu_basic')],
            [InlineKeyboardButton("🎬 Entertainment", callback_data='menu_fun')]
        ]
        await query.edit_message_text("🏢 **Selamat Datang ke Fam Ravlyn Mall!**", reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    if not TOKEN: return
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
