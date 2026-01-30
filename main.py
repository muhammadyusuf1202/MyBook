import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- SOZLAMALAR ---
# BotFather bergan tokenni shu yerga yozing
TOKEN = "8322766291:AAELadOu66xZUCtH4qbEg5ipgRcpEv-yBQo" 

# Saytingiz manzili (Web App shu manzilni ochadi)
WEB_APP_URL = "https://sizning-saytingiz.uz" 

# Bot va Dispatcher obyektlari
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- KLAVIATURA ---
def main_menu_kb():
    builder = InlineKeyboardBuilder()
    
    # Web App tugmasi - Saytni Telegram ichida ochadi
    builder.row(InlineKeyboardButton(
        text="📚 Kitobxonani ochish", 
        web_app=WebAppInfo(url=WEB_APP_URL))
    )
    
    # Qo'shimcha tugmalar
    builder.row(
        InlineKeyboardButton(text="💰 Hamyon", callback_data="wallet"),
        InlineKeyboardButton(text="👑 Premium", callback_data="premium")
    )
    
    builder.row(InlineKeyboardButton(text="📢 Kanalimiz", url="https://t.me/mykitob_uz"))
    
    return builder.as_markup()

# --- HANDLERLAR ---

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    """
    /start buyrug'i kelganda ishlaydi. 
    Lokal papkadagi icon.png faylini yuboradi.
    """
    welcome_text = (
        f"👋 **Assalomu alaykum, {message.from_user.full_name}!**\n\n"
        f"📖 **MyKitob.UZ** botiga xush kelibsiz.\n"
        f"Bu yerda siz eng sara kitoblarni o'qishingiz, audio eshitishingiz "
        f"va testlar yechib coin yig'ishingiz mumkin."
    )

    try:
        # Rasmni lokal papkadan o'qish (HTTP URL xatosini oldini oladi)
        photo_file = FSInputFile("icon.png")
        await message.answer_photo(
            photo=photo_file,
            caption=welcome_text,
            parse_mode="Markdown",
            reply_markup=main_menu_kb()
        )
    except Exception as e:
        # Agar rasm papkada bo'lmasa, faqat matnni yuboradi
        logging.error(f"Rasm yuborishda xato: {e}")
        await message.answer(
            text=welcome_text,
            parse_mode="Markdown",
            reply_markup=main_menu_kb()
        )

# Callback (tugma bosilganda) mantiqi
@dp.callback_query(F.data == "wallet")
async def process_wallet(callback: types.CallbackQuery):
    await callback.answer() # Tugma bosilgandagi yuklanishni to'xtatadi
    await callback.message.answer("💳 Sizning balansingiz: **110 coin**")

@dp.callback_query(F.data == "premium")
async def process_premium(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("👑 **Premium** rejimida barcha kitoblar reklamasiz va bepul!")

# --- ISHGA TUSHIRISH ---
async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")