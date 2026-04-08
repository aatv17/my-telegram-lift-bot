import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN_MALL')
TARGET_GROUP_ID = -1002477011468
TOPIC_ID = 7565

# Log sistem
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- DATA MALL ---
# Sila ganti link 'img' dengan File ID yang anda dapat nanti untuk kelajuan maksimum.
MALL_DATA = {
    "food": {
        "text": "<b>🍴 Food & Relaxation</b>",
        "items": [
            {"name": "Food Court", "img": "https://i.pinimg.com/1200x/1f/e1/e7/1fe1e71db44391066b1c9d4b18b32d1f.jpg", "pin": "https://pin.it/4kR5X6Z0H"},
            {"name": "Roof Garden", "img": "https://i.pinimg.com/736x/1b/68/de/1b68dedbb98a3ad38dded21f6181d126.jpg", "pin": "https://pin.it/6YyXJz8qB"}
        ]
    },
    "clothing": {
        "text": "<b>👕 Clothing & Fashion</b>",
        "items": [
            {"name": "Urban Wear (Baggy)", "img": "https://i.pinimg.com/736x/49/96/51/499651406e9c5aa2376e5f08725ec424.jpg", "pin": "https://pin.it/2mZ7O4L9P"},
            {"name": "Classic Tailor", "img": "https://i.pinimg.com/736x/bc/d3/04/bcd3047af1ff9b8fe6e003b3c39d4a66.jpg", "pin": "https://pin.it/3nK9R2V5X"}
        ]
    }
}

async def post_init(application: Application):
    await application.bot.set_my_commands([BotCommand("start", "Masuk ke Mall")])

# --- 1. FUNGSI GRAB ID GAMBAR ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bila anda hantar gambar, bot akan balas dengan File ID."""
    photo_file = update.message.photo[-1]
    file_id = photo_file.file_id
    
    msg = (
        "📸 <b>ID GAMBAR DIKESAN!</b>\n\n"
        "Copy ID di bawah dan paste dalam kod Python anda:\n\n"
        f"<code>{file_id}</code>"
    )
    await update.message.reply_text(msg, parse_mode='HTML')

# --- 2. FUNGSI MENU MALL ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🍴 Food & Relaxation", callback_data='menu_food')],
        [InlineKeyboardButton("👕 Clothing & Fashion", callback_data='menu_clothing')],
        [InlineKeyboardButton("🚽 Basic Facilities", callback_data='menu_basic')],
        [InlineKeyboardButton("🎬 Entertainment", callback_data='menu_fun')]
    ]
    
    # Gunakan query.message jika dipanggil dari butang, update.message jika dipanggil dari command
    target = update.message if update.message else update.callback_query.message
    
    await target.reply_text(
        "🏢 <b>Selamat Datang ke Fam Ravlyn Mall!</b>\n\n"
        "Hantar gambar di sini untuk dapatkan <b>File ID</b>, "
        "atau pilih kategori di bawah:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("menu_"):
        cat = query.data.split("_")[1]
        if cat not in MALL_DATA:
            await query.answer("Kategori ini akan dibuka tidak lama lagi!", show_alert=True)
            return
            
        items = MALL_DATA[cat]['items']
        keyboard = [[InlineKeyboardButton(i['name'], callback_data=f"item_{cat}_{items.index(i)}")] for i in items]
        keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data='back_main')])
        
        await query.edit_message_text(MALL_DATA[cat]['text'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

    elif query.data.startswith("item_"):
        _, cat, idx = query.data.split("_")
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
                caption=f"🏬 <b>{item['name']}</b>\nSelamat datang!",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='HTML'
            )
        except Exception as e:
            await query.edit_message_text(f"❌ Gagal hantar gambar: {e}\n\n[Klik Pinterest]({item['pin']})", 
                                         reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

    elif query.data == "back_main":
        keyboard = [
            [InlineKeyboardButton("🍴 Food & Relaxation", callback_data='menu_food')],
            [InlineKeyboardButton("👕 Clothing & Fashion", callback_data='menu_clothing')],
            [InlineKeyboardButton("🚽 Basic Facilities", callback_data='menu_basic')],
            [InlineKeyboardButton("🎬 Entertainment", callback_data='menu_fun')]
        ]
        await query.edit_message_text("🏢 <b>Fam Ravlyn Mall</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

def main():
    if not TOKEN: return
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Mall Bot + ID Grabber sedang berjalan...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
