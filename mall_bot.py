import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN_MALL')
TARGET_GROUP_ID = -1002477011468
TOPIC_ID = 7565

# --- DATA MALL (Ganti 'img' dengan File ID yang anda dapat nanti) ---
MALL_DATA = {
    "food": {
        "text": "🍴 **Food & Relaxation**",
        "items": [
            {"name": "Food Court", "img": "https://i.pinimg.com/1200x/1f/e1/e7/1fe1e71db44391066b1c9d4b18b32d1f.jpg", "pin": "https://pin.it/4kR5X6Z0H"},
            {"name": "Roof Garden", "img": "https://i.pinimg.com/736x/1b/68/de/1b68dedbb98a3ad38dded21f6181d126.jpg", "pin": "https://pin.it/6YyXJz8qB"}
        ]
    },
    "clothing": {
        "text": "👕 **Clothing & Fashion**",
        "items": [
            {"name": "Urban Wear (Baggy)", "img": "https://i.pinimg.com/736x/49/96/51/499651406e9c5aa2376e5f08725ec424.jpg", "pin": "https://pin.it/2mZ7O4L9P"},
            {"name": "Classic Tailor", "img": "https://i.pinimg.com/736x/bc/d3/04/bcd3047af1ff9b8fe6e003b3c39d4a66.jpg", "pin": "https://pin.it/3nK9R2V5X"}
        ]
    }
}

logging.basicConfig(level=logging.INFO)

# --- FUNGSI DETECT ID GAMBAR ---
async def get_image_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot akan balas dengan File ID bila anda hantar gambar."""
    file_id = update.message.photo[-1].file_id
    await update.message.reply_text(f"✅ **ID Gambar Dikesan!**\n\nSila copy ID di bawah dan paste ke dalam kod Python anda:\n\n`{file_id}`", parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🍴 Food & Relaxation", callback_data='menu_food')],
        [InlineKeyboardButton("👕 Clothing & Fashion", callback_data='menu_clothing')]
    ]
    await update.message.reply_text("🏢 **Fam Ravlyn Mall**", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("menu_"):
        cat = query.data.split("_")[1]
        items = MALL_DATA[cat]['items']
        keyboard = [[InlineKeyboardButton(i['name'], callback_data=f"item_{cat}_{items.index(i)}")] for i in items]
        keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data='back_main')])
        await query.edit_message_text(MALL_DATA[cat]['text'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data.startswith("item_"):
        _, cat, idx = query.data.split("_")
        item = MALL_DATA[cat]['items'][int(idx)]
        keyboard = [[InlineKeyboardButton("📍 Pinterest", url=item['pin'])], [InlineKeyboardButton("⬅️ Kembali", callback_data=f"menu_{cat}")]]
        
        # Bot hantar gambar (Guna File ID atau Link)
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            message_thread_id=TOP_ID,
            photo=item['img'],
            caption=f"🏬 **{item['name']}**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

def main():
    if not TOKEN: return
    app = Application.builder().token(TOKEN).build()
    
    # Handler untuk detect gambar
    app.add_handler(MessageHandler(filters.PHOTO, get_image_id))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    app.run_polling()

if __name__ == '__main__':
    main()
