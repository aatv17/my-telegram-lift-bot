import logging
import os
import random
import asyncio
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN_WEATHER')

# --- ARAHAN PENTING UNTUK ARKA ---
# 1. Pastikan ID bermula dengan -100 (Contoh: -100123456789)
# 2. Pastikan Bot sudah di-INVITE ke dalam Group
# 3. Pastikan Bot adalah ADMIN dalam Group
TARGET_GROUP_ID = -1002477011468  # <--- GANTI ID ANDA DI SINI
TOPIC_ID = 143221

WEATHER_OPTIONS = [
    {"status": "Hujan Berlian 💎", "temp": "-50°C", "desc": "Sila bawa payung besi!"},
    {"status": "Panas Mentari Biru ☀️", "temp": "85°C", "desc": "Cuaca sangat terik, air laut mendidih."},
    {"status": "Ribut Gula-Gula 🍭", "temp": "24°C", "desc": "Angin kencang membawa awan kapas."},
    {"status": "Kabut Neon 🌫️", "temp": "15°C", "desc": "Semua nampak warna-warni neon."},
    {"status": "Salji Coklat ❄️", "temp": "-5°C", "desc": "Sesuai untuk buat milo ais percuma."},
    {"status": "Angin Berbisik 🌬️", "temp": "20°C", "desc": "Angin sepoi-sepoi bahasa."}
]

logging.basicConfig(level=logging.INFO)

async def send_weather_update(context: ContextTypes.DEFAULT_TYPE):
    weather = random.choice(WEATHER_OPTIONS)
    text = (
        f"📅 **Laporan Cuaca Fam Ravlyn**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🌍 **Status:** {weather['status']}\n"
        f"🌡️ **Suhu:** {weather['temp']}\n"
        f"📝 **Info:** {weather['desc']}\n"
        f"━━━━━━━━━━━━━━━"
    )
    
    # CUBAAN 1: Hantar ke Topik Spesifik
    try:
        await context.bot.send_message(
            chat_id=TARGET_GROUP_ID,
            message_thread_id=TOPIC_ID,
            text=text,
            parse_mode='Markdown'
        )
        logging.info("✅ Berjaya hantar ke Topik!")
    except Exception as e:
        logging.warning(f"⚠️ Gagal ke Topik, ralat: {e}")
        
        # CUBAAN 2: Jika gagal ke topik, hantar ke Group Utama (General)
        try:
            await context.bot.send_message(
                chat_id=TARGET_GROUP_ID,
                text=f"⚠️ (Hantaran Kecemasan ke General)\n\n{text}",
                parse_mode='Markdown'
            )
            logging.info("✅ Berjaya hantar ke General Group!")
        except Exception as e2:
            logging.error(f"❌ Gagal total ke Group & Topik: {e2}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.job_queue:
        await update.message.reply_text("🚀 **Bot Diaktifkan!** Cuba hantar laporan sekarang...")
        
        # Hantar serta-merta untuk test
        await send_weather_update(context)

        # Set jadual harian (86400 saat)
        context.job_queue.run_repeating(
            send_weather_update, 
            interval=86400, 
            first=86400, 
            name="weather_daily"
        )
    else:
        await update.message.reply_text("❌ JobQueue Error.")

def main():
    if not TOKEN: return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
