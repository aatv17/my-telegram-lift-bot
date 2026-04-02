import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
# Menggunakan os.getenv supaya token anda selamat di GitHub Secrets
TOKEN = os.getenv('BOT_TOKEN', '8786168146:AAFpYoVW07bkHkZztq6YFW4zpsONHIpk5vk')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

DRINK_FILES = {
    "martini": "AgACAgUAAxkBAAMaaaW18F0Q_X6nf1QmlGpAVDB_I_cAAs0MaxuC6zFVrzXRNeyucR4BAAMCAAN5AAM6BA",
    "whiskey": "AgACAgUAAxkBAAMdaaW2ShVVRTKTTsyQiPDbhixj6igAAs4MaxuC6zFVZFBwBTvrGOkBAAMCAANtAAM6BA",
    "mojito": "AgACAgUAAxkBAAMhaaW2aA2J_rsAAWAxaAodd_9uhkDzAALRDGsbgusxVbhCV5XoektqAQADAgADbQADOgQ",
    "champagne": "AgACAgUAAxkBAAMtaaW3MukWLXhHpq1dfERrDV7B2JIAAtcMaxuC6zFVu45z-UZFB8gBAAMCAAN5AAM6BA",
    "cola": "AgACAgUAAxkBAAMfaaW2WfkzU3jLeo71jTxCi1nMmUgAAs8MaxuC6zFVLM5GBuk0OqEBAAMCAAN4AAM6BA",
    "wine": "AgACAgUAAxkBAAMjaaW28utBiCkVo93zdxv26QWarvIAAtIMaxuC6zFV2S5S75w0d5oBAAMCAAN4AAM6BA",
    "gin": "AgACAgUAAxkBAAMlaaW3AZCUo0eUJ-xtKFMRRk1ID6gAAtMMaxuC6zFVMXiM2D_-8GcBAAMCAANtAAM6BA",
    "margarita": "AgACAgUAAxkBAAMraaW3JSOIvrsuO1lJEdroUVrDH3gAAtYMaxuC6zFVCOMM65lX3TEBAAMCAANtAAM6BA",
    "water": "AgACAgUAAxkBAAMpaaW3GJ5kc1zrcOyA_eiNKUkAAXwqAALVDGsbgusxVQSioZ6TEidzAQADAgADbQADOgQ",
    "coffee": "AgACAgUAAxkBAAMnaaW3Dnt4OEwqIq5p3GdlJ6hRLJEAAtQMaxuC6zFVn5r8lTnikc4BAAMCAANtAAM6BA"
}

DRINKS_TEXT = {
    "martini": "🍸 The waiter glides over and hands a chilled Classic Martini to the customer.",
    "whiskey": "🥃 The waiter places a heavy glass of Aged Whiskey on the table with a nod.",
    "mojito": "🌿 The waiter serves a refreshing Mint Mojito. Stay cool!",
    "champagne": "🥂 Bubbles! The waiter pours a golden glass of Champagne.",
    "cola": "🥤 A cold Cola with ice is served to the man who ordered it.",
    "wine": "🍷 The waiter expertly pours a deep Red Wine.",
    "gin": "🍸 A crisp Gin and Tonic, served with a twist of lime.",
    "margarita": "🧂 A salty Margarita is placed carefully on your coaster.",
    "water": "💧 Pure, chilled sparkling water. Refreshing!",
    "coffee": "☕ A strong Espresso to keep the luck going at the table."
}

async def post_init(application: Application):
    """Menetapkan menu 'Menu' butang secara automatik dalam Telegram."""
    commands = [
        BotCommand("menu", "Papar Menu Bar Casino"),
        BotCommand("drink", "Pesan minuman (Contoh: /drink martini)"),
    ]
    await application.bot.set_my_commands(commands)

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Martini 🍸", callback_data='martini'), InlineKeyboardButton("Whiskey 🥃", callback_data='whiskey')],
        [InlineKeyboardButton("Mojito 🌿", callback_data='mojito'), InlineKeyboardButton("Champagne 🥂", callback_data='champagne')],
        [InlineKeyboardButton("Cola 🥤", callback_data='cola'), InlineKeyboardButton("Wine 🍷", callback_data='wine')],
        [InlineKeyboardButton("Gin 🍸", callback_data='gin'), InlineKeyboardButton("Margarita 🧂", callback_data='margarita')],
        [InlineKeyboardButton("Water 💧", callback_data='water'), InlineKeyboardButton("Coffee ☕", callback_data='coffee')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    target = update.message if update.message else update.callback_query.message
    await target.reply_text("🛎️ **Casino Bar is Open!**\nSelect a drink below:", reply_markup=reply_markup, parse_mode='Markdown')

async def serve(update: Update, context: ContextTypes.DEFAULT_TYPE, drink_name: str, user, chat_id, message_to_reply):
    if drink_name in DRINK_FILES:
        caption_text = (
            f"{DRINKS_TEXT[drink_name]}\n\n"
            f"👤 **Ordered by:** {user.first_name}\n"
            f"🆔 **User ID:** `{user.id}`\n"
            f"🏢 **Room ID:** `{chat_id}`"
        )
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=DRINK_FILES[drink_name],
            caption=caption_text,
            parse_mode='Markdown',
            reply_to_message_id=message_to_reply
        )
    else:
        await context.bot.send_message(chat_id=chat_id, text="Sorry, we don't have that drink in our bar!")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await serve(update, context, query.data, query.from_user, update.effective_chat.id, query.message.message_id)

async def handle_drink_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /drink martini")
        return
    await serve(update, context, context.args[0].lower(), update.message.from_user, update.effective_chat.id, update.message.message_id)

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN not found!")
        return

    # post_init digunakan untuk set menu command secara automatik
    application = Application.builder().token(TOKEN).post_init(post_init).build()

    application.add_handler(CommandHandler("menu", show_menu))
    application.add_handler(CommandHandler("start", show_menu))
    application.add_handler(CommandHandler("drink", handle_drink_cmd))
    application.add_handler(CallbackQueryHandler(handle_button))

    print("Casino Bot is running...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()