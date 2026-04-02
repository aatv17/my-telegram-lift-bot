import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- KONFIGURASI ---
# Kod ini akan cuba membaca token dari GitHub Secrets. 
# Jika tiada (masa test di PC), ia akan guna token manual di bawah.
TOKEN = os.getenv('BOT_TOKEN', '8652495747:AAHYO4Wm3q6deQCHw6Lplzq-CAbrRl8Te6M')

# Simpan status lif (tingkat semasa)
current_lift_state = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Database Fail Gambar & Pautan
FLOOR_FILES = {
    "B": "AgACAgUAAxkBAAMWaa7T3Xu_pIPAFgMaaeGXnt-30VAAAr4NaxsMx3hV6gjo3f5ukKsBAAMCAAN5AAM6BA",
    "1": "AgACAgUAAxkBAAMPaa4F2r0XSk-EcqwPrz589jwMLz0AAmINaxsMx3BVjhMpURTpYu8BAAMCAAN5AAM6BA",
    "2": "AgACAgUAAxkBAAMIaa4Ehxxhpz37XzMX8FEenX8hdXMAAmENaxsMx3BVMc6abeDrYZkBAAMCAAN5AAM6BA",
    "3": "AgACAgUAAxkBAAMRaa4F5n85SG2vQ-7yDr7In5KlHSQAAmMNaxsMx3BVAjxPDdEds6cBAAMCAAN4AAM6BA",
    "R": "AgACAgUAAxkBAAMYaa7T9SCrdPiEFNhl1s6rQ4RFfJkAAr8NaxsMx3hV8nRtWCVKP1kBAAMCAAN5AAM6BA"
}

FLOOR_LINKS = {
    "B": "https://t.me/famsravlyn/196282",
    "1": "https://t.me/famsravlyn/7531",
    "2": "https://t.me/famsravlyn/196316",
    "3": "https://t.me/famsravlyn/196329",
    "R": "https://t.me/famsravlyn/103291"
}

FLOOR_NAMES = {
    "B": "Basement Floor 🚗",
    "1": "Tingkat 1 (Living Room)",
    "2": "Tingkat 2 (Lorong 2)",
    "3": "Tingkat 3 (Lorong 3)",
    "R": "Rooftop Garden 🌿"
}

SHORT_NAMES = {"B": "Basement 🚗", "1": "Tingkat 1 🔽", "2": "Tingkat 2 ↕️", "3": "Tingkat 3 🔼", "R": "Rooftop 🌿"}
FLOOR_LEVELS = {"B": 0, "1": 1, "2": 2, "3": 3, "R": 4}

# --- FUNGSI BANTUAN ---

def get_state_key(update: Update):
    chat_id = update.effective_chat.id
    thread_id = update.effective_message.message_thread_id if update.effective_message else None
    return f"{chat_id}_{thread_id}"

async def post_init(application: Application):
    """Menetapkan menu 'Commands' secara automatik dalam Telegram."""
    commands = [
        BotCommand("start", "Mula & Papar Panel Lif"),
        BotCommand("lift", "Panggil Lif"),
    ]
    await application.bot.set_my_commands(commands)

async def send_lift_photo(update, context, floor_key):
    chat_id = update.effective_chat.id
    thread_id = update.effective_message.message_thread_id
    user_name = update.effective_user.first_name
    state_key = get_state_key(update)

    # Logik pergerakan lif
    old_floor = current_lift_state.get(state_key, "1")
    if FLOOR_LEVELS[floor_key] < FLOOR_LEVELS[old_floor]:
        action = "Turun ke"
    elif FLOOR_LEVELS[floor_key] > FLOOR_LEVELS[old_floor]:
        action = "Naik ke"
    else:
        action = "Anda berada di"
    
    current_lift_state[state_key] = floor_key
    caption_text = f"🛗 *Ding!* {action} {FLOOR_NAMES[floor_key]}\n\n👤 **Penumpang:** {user_name}"

    # Bina butang navigasi (Tapis tingkat semasa)
    nav_buttons = []
    for code in ["R", "3", "2", "1", "B"]:
        if code != floor_key:
            nav_buttons.append([InlineKeyboardButton(SHORT_NAMES[code], callback_data=code)])

    keyboard = [[InlineKeyboardButton(f"🚪 Masuk ke {FLOOR_NAMES[floor_key]}", url=FLOOR_LINKS[floor_key])]] + nav_buttons
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_photo(
        chat_id=chat_id, 
        message_thread_id=thread_id, 
        photo=FLOOR_FILES[floor_key], 
        caption=caption_text, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

# --- HANDLERS ---

async def show_lift_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Rooftop Garden 🌿", callback_data='R')],
        [InlineKeyboardButton("Tingkat 3 🔼", callback_data='3')],
        [InlineKeyboardButton("Tingkat 2 ↕️", callback_data='2')],
        [InlineKeyboardButton("Tingkat 1 🔽", callback_data='1')],
        [InlineKeyboardButton("Basement 🚗", callback_data='B')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_message.reply_text(
        "🛎️ **Panel Lif Rumah**\nSila pilih tingkat:", 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def handle_shorthand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text.upper()
    if text in FLOOR_LEVELS: 
        await send_lift_photo(update, context, text)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await send_lift_photo(update, context, query.data)

# --- MAIN ---

def main():
    if not TOKEN:
        print("Ralat: BOT_TOKEN tidak dijumpai!")
        return

    # post_init digunakan untuk set menu command secara automatik
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler(["start", "lift"], show_lift_menu))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_shorthand))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    print("Bot sedang berjalan...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()