import logging
import os
import random
import asyncio
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN_WEATHER')
# Link yang anda beri: https://t.me/famsravlyn/143221
# 143221 adalah ID TOPIK (Message Thread ID)
TARGET_GROUP_ID = -1002477011468 # GANTI dengan ID Group anda (Guna @userinfobot untuk tahu ID group)
TOPIC_ID = 143221

# Senarai Cuaca Rekaan (Boleh tambah ikut kreativiti anda)
WEATHER_OPTIONS = [
    {"status": "Hujan Berlian 💎", "temp": "-50°C", "desc": "Sila bawa payung besi, berlian tajam sedang turun dari langit!"},
    {"status": "Panas Mentari Biru ☀️", "temp": "85°C", "desc": "Cuaca sangat terik, air laut pun rasa macam kopi panas."},
    {"status": "Ribut Gula-Gula 🍭", "temp": "24°C", "desc": "Angin kencang membawa awan kapas dan hujan lollipop."},
    {"status": "Kabut Neon 🌫️", "temp": "15°C", "desc": "Jarak penglihatan terhad, semua benda nampak warna-warni."},
    {"status": "Salji Coklat ❄️", "temp": "-5°C", "desc": "Sesuai untuk buat milo ais terus dari langit."},
    {"status": "Angin Berbisik 🌬️", "temp": "20°C", "desc": "Angin yang bertiup kedengaran seperti suara orang menyanyi."}
]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def post_init(application: Application):
    await application.bot.set_my_commands([BotCommand("start", "Mula Bot Cuaca")])

async def send_weather_update(context: ContextTypes.DEFAULT_TYPE):
    """Fungsi untuk hantar cuaca rawak."""
    weather = random.choice(WEATHER_OPTIONS)
    text = (
        f"📅 **Laporan Cuaca Hari Ini**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🌍 **Status:** {weather['status']}\n"
        f"🌡️ **Suhu:** {weather['temp']}\n"
        f"📝 **Info:** {weather['desc']}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📍 *Lokasi: Fam Ravlyn Estate*"
    )
    
    await context.bot.send_message(
        chat_id=TARGET_GROUP_ID,
        message_thread_id=TOPIC_ID,
        text=text,
        parse_mode='Markdown'
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /start untuk aktifkan jadual 24 jam."""
    chat_id = update.effective_chat.id
    
    # Set jadual setiap 24 jam (86400 saat)
    # Anda boleh tukar saat untuk testing (cth: 60 untuk 1 minit)
    context.job_queue.run_repeating(send_weather_update, interval=86400, first=10)
    
    await update.message.reply_text("✅ **Bot Cuaca Aktif!**\nLaporan akan dihantar ke topik setiap 24 jam.")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN_WEATHER not found!")
        return

    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("Fictional Weather Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
