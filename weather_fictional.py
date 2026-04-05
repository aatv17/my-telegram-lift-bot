import logging
import os
import random
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = os.getenv('BOT_TOKEN_WEATHER')
# Pastikan ID Group bermula dengan -100
TARGET_GROUP_ID = -1002477011468 # <--- GANTI ID GROUP ANDA
TOPIC_ID = 143221

# Koleksi Cuaca Rekaan
WEATHER_OPTIONS = [
    {"status": "Hujan Berlian 💎", "temp": "-50°C", "desc": "Sila bawa payung besi, berlian tajam sedang turun!"},
    {"status": "Panas Mentari Biru ☀️", "temp": "85°C", "desc": "Cuaca sangat terik, air laut mendidih."},
    {"status": "Ribut Gula-Gula 🍭", "temp": "24°C", "desc": "Angin kencang membawa awan kapas."},
    {"status": "Kabut Neon 🌫️", "temp": "15°C", "desc": "Semua nampak warna-warni neon."},
    {"status": "Salji Coklat ❄️", "temp": "-5°C", "desc": "Sesuai untuk buat milo ais percuma."},
    {"status": "Angin Berbisik 🌬️", "temp": "20°C", "desc": "Angin sepoi-sepoi bahasa."}
]

logging.basicConfig(level=logging.INFO)

async def post_init(application: Application):
    await application.bot.set_my_commands([BotCommand("start", "Mula Laporan Cuaca")])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bila tekan /start, bot TERUS hantar cuaca sekali."""
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
        # Cuba hantar ke Topik
        await context.bot.send_message(
            chat_id=TARGET_GROUP_ID,
            message_thread_id=TOPIC_ID,
            text=text,
            parse_mode='Markdown'
        )
        await update.message.reply_text("✅ Laporan cuaca telah dihantar ke topik!")
    except Exception as e:
        # Jika gagal ke topik, hantar terus ke group utama
        try:
            await context.bot.send_message(
                chat_id=TARGET_GROUP_ID,
                text=f"⚠️ (Hantaran ke General)\n\n{text}",
                parse_mode='Markdown'
            )
            await update.message.reply_text("✅ Berjaya hantar ke group utama!")
        except Exception as e2:
            await update.message.reply_text(f"❌ Gagal: {e2}")

def main():
    if not TOKEN:
        print("BOT_TOKEN_WEATHER tiada!")
        return

    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Bot Cuaca Manual sedang berjalan...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
