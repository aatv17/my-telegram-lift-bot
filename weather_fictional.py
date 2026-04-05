import logging
import os
import random
import asyncio
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN_WEATHER')
# PASTI KAN ID GROUP BETUL (Mesti ada -100 di depan)
TARGET_GROUP_ID = -1001234567890 # <--- GANTI DENGAN ID GROUP ANDA
TOPIC_ID = 143221

WEATHER_OPTIONS = [
    {"status": "Hujan Berlian 💎", "temp": "-50°C", "desc": "Sila bawa payung besi!"},
    {"status": "Panas Mentari Biru ☀️", "temp": "85°C", "desc": "Cuaca sangat terik, air laut mendidih."},
    {"status": "Ribut Gula-Gula 🍭", "temp": "24°C", "desc": "Angin kencang membawa awan kapas."},
    {"status": "Kabut Neon 🌫️", "temp": "15°C", "desc": "Semua nampak warna-warni neon."},
    {"status": "Salji Coklat ❄️", "temp": "-5°C", "desc": "Sesuai untuk buat milo ais percuma."},
    {"status": "Angin Berbisik 🌬️", "temp": "20°C", "desc": "Angin membisikkan kata-kata semangat."}
]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def post_init(application: Application):
    await application.bot.set_my_commands([BotCommand("start", "Mula Bot Cuaca")])

async def send_weather_update(context: ContextTypes.DEFAULT_TYPE):
    """Fungsi hantar mesej cuaca."""
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
        # Hantar ke group dan topik yang spesifik
        await context.bot.send_message(
            chat_id=TARGET_GROUP_ID,
            message_thread_id=TOPIC_ID,
            text=text,
            parse_mode='Markdown'
        )
        logging.info("Mesej cuaca berjaya dihantar!")
    except Exception as e:
        logging.error(f"Gagal hantar mesej: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /start untuk hantar SEKARANG dan mula JADUAL."""
    if context.job_queue:
        await update.message.reply_text("🚀 **Bot Cuaca Aktif!**\nHantar laporan pertama sekarang...")
        
        # 1. HANTAR SERTA-MERTA (Tak payah tunggu)
        await send_weather_update(context)

        # 2. SET JADUAL (Sekarang set 60 saat untuk test)
        # UNTUK 24 JAM: Tukar 60 kepada 86400
        MASA_MENUNGGU = 60 

        # Buang jadual lama supaya tak bertindih
        current_jobs = context.job_queue.get_jobs_by_name("weather_job")
        for job in current_jobs:
            job.schedule_removal()

        context.job_queue.run_repeating(
            send_weather_update, 
            interval=MASA_MENUNGGU, 
            first=MASA_MENUNGGU, 
            name="weather_job"
        )
        
        await update.message.reply_text(f"✅ Jadual bermula! Mesej seterusnya setiap {MASA_MENUNGGU} saat.")
    else:
        await update.message.reply_text("❌ Ralat: JobQueue tidak berfungsi.")

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN_WEATHER not found!")
        return

    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot Cuaca sedang berjalan...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
