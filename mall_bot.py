import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN_MALL')
TARGET_GROUP_ID = -1002477011468
TOP_ID = 7565

# Log sistem
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def post_init(application: Application):
    await application.bot.set_my_commands([BotCommand("start", "Masuk ke Mall")])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hantar menu mall ke topik spesifik di group."""
    keyboard = [
        [
            InlineKeyboardButton("🍔 Makanan", callback_data='buy_makanan'),
            InlineKeyboardButton("🥤 Minuman", callback_data='buy_minuman')
        ],
        [
            InlineKeyboardButton("👕 Pakaian", callback_data='buy_pakaian'),
            InlineKeyboardButton("👟 Kasut", callback_data='buy_kasut')
        ],
        [
            InlineKeyboardButton("🎬 Wayang", callback_data='buy_wayang'),
            InlineKeyboardButton("🧸 Mainan", callback_data='buy_mainan')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "🏢 <b>Selamat Datang ke Fam Ravlyn Mall!</b>\nSila pilih kategori barang yang anda cari:"
    
    # Menghantar mesej ke Group dan Topik yang ditetapkan
    await context.bot.send_message(
        chat_id=TARGET_GROUP_ID,
        message_thread_id=TOP_ID,
        text=text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    responses = {
        'buy_makanan': "🍔 Sila ke <b>Food Court</b> untuk pelbagai pilihan makanan!",
        'buy_minuman': "🥤 <b>Starbucks & Tealive</b> sedia menghidangkan minuman segar!",
        'buy_pakaian': "👕 Butik <b>Urban Wear</b> (Baggy & Straight Cut) di Tingkat 1!",
        'buy_kasut': "👟 Kedai sneakers terletak bersebelahan dengan eskalator utama.",
        'buy_wayang': "🎬 <b>Cinema</b> sedang menayangkan filem terbaru hari ini!",
        'buy_mainan': "🧸 <b>Toy Zone</b> adalah syurga untuk kanak-kanak!"
    }
    
    msg = responses.get(data, "Pilihan tidak dikesan.")
    back_keyboard = [[InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data='back_main')]]
    
    await query.edit_message_text(
        text=f"{msg}\n\nAda apa-apa lagi yang anda perlukan?",
        reply_markup=InlineKeyboardMarkup(back_keyboard),
        parse_mode='HTML'
    )

async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🍔 Makanan", callback_data='buy_makanan'), InlineKeyboardButton("🥤 Minuman", callback_data='buy_minuman')],
        [InlineKeyboardButton("👕 Pakaian", callback_data='buy_pakaian'), InlineKeyboardButton("👟 Kasut", callback_data='buy_kasut')],
        [InlineKeyboardButton("🎬 Wayang", callback_data='buy_wayang'), InlineKeyboardButton("🧸 Mainan", callback_data='buy_mainan')]
    ]
    await query.edit_message_text(
        "🏢 <b>Fam Ravlyn Mall</b>\nSila pilih kategori:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

def main():
    if not TOKEN: return
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_back, pattern='back_main'))
    app.add_handler(CallbackQueryHandler(button_handler, pattern='^buy_'))
    
    print("Mall Bot Emoji (Topic Mode) sedang berjalan...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
