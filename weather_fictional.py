import logging
import os
import random
import asyncio
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN_WEATHER')
# ID Group & Topic anda
TARGET_GROUP_ID = -1001234567890 # GANTI kepada ID Group anda (WAJIB)
TOPIC_ID = 143221

# Senarai Cuaca Rekaan
WEATHER_OPTIONS = [
    {"status": "Hujan Berlian 💎", "temp": "-50°C", "desc": "Sila bawa payung besi, berlian tajam sedang turun dari langit!"},
    {"status": "Panas Mentari Biru ☀️", "temp": "85°C", "desc": "Cuaca sangat terik, air laut pun rasa macam kopi panas."},
    {"status": "Ribut Gula-Gula 🍭", "temp": "24°C", "desc": "Angin kencang membawa awan kapas dan hujan lollipop."},
    {"status": "Kabut Neon 🌫️", "temp": "15°C", "desc": "Semua nampak warna-warni, hati-hati semasa memandu kuda terbang."},
    {"status": "Salji Coklat ❄️", "temp": "-5°C", "desc": "Sesuai untuk buat milo ais terus dari langit."},
    {"status": "Angin Berbisik 🌬️", "temp": "20°C", "desc": "Angin sepoi-sepoi bahasa yang membisikkan kata-kata semangat."}
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def post_init(application: Application):
    """Set menu command secara automatik."""
    await application.bot.set_my_commands([BotCommand("start", "Mula Bot Cuaca")])

async def send_weather_update(context: ContextTypes.DEFAULT_TYPE):
    """Fungsi yang akan dipanggil setiap 24 jam."""
    weather = random.choice(WEATHER_OPTIONS)
    text = (
        f"📅 **Laporan Cuaca Fam Ravlyn**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🌍 **Status:** {weather['status']}\n"
        f"🌡️ **Suhu:** {weather['temp']}\n"
        f"📝 **Info:** {weather['desc']}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"📍 *Lokasi: Digital Realm*"
    )
    
    try:
        await context.bot.send_message(
            chat_id=TARGET_GROUP_ID,
            message_thread_id=TOPIC_ID,
            text=text,
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Gagal hantar mesej: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /start untuk aktifkan jadual."""
    if context.job_queue:
        # Buang jadual lama jika ada untuk elakkan double chat
        current_jobs = context.job_queue.get_jobs_by_name("daily_weather")
        for job in current_jobs:
            job.schedule_removal()

        # Set jadual baru setiap 24 jam (86400 saat)
        context.job_queue.run_repeating(
            send_weather_update, 
            interval=60, 
            first=10, 
            name="daily_weather"
        )
        await update.message.reply_text("✅ **Bot Cuaca Aktif!**\nLaporan rawak akan dihantar ke topik setiap 24 jam.")
    else:
        await update.message.reply_text("❌ **Ralat:** JobQueue tidak dikesan. Sila semak pemasangan library.")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN_WEATHER not found!")
        return

    # Bina aplikasi dengan JobQueue aktif
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("Fictional Weather Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
