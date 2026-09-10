"""
Обработчик информации об объекте
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import PROPERTY
from keyboards import get_main_menu
import re


def _clean_phone_for_tel(phone):
    """Очистить номер телефона для tel: URL (только цифры и +)"""
    return re.sub(r'[^\d+]', '', phone)


async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Информация об объекте"""
    info_text = f"""
🏨 {PROPERTY['name']}

📍 Адрес:
{PROPERTY['address']}

📋 Описание:
Уютный коттедж в лесу с баней, купелью и шикарной большой территорией среди реликтового соснового леса. 
Идеальное место для уединённого отдыха с видом на горы и уникальную природу Байкала.

✨ Что включено в проживание:
✓ Wi-Fi и телевидение
✓ Современная кухня с техникой
✓ Джакузи и ванная комната
✓ Комплект постельного белья и полотенец
✓ Гигиенические принадлежности
✓ Большая парковка
✓ Терраса с видом на природу

🏊 Дополнительные услуги:
🔥 Русская парная баня на дровах
🛁 Уличная купель с горячей водой
🎉 Каминный зал с караоке
🍖 Мангальная зона для шашлыков

👍 Рейтинг: ⭐⭐⭐⭐⭐ (5.0 звёзд на Яндекс.Картах)
"""
    
    # Создаём клавиатуру с контактами
    keyboard = []
    if PROPERTY.get('phone') and PROPERTY['phone'].strip():
        clean_phone = _clean_phone_for_tel(PROPERTY['phone'])
        keyboard.append([InlineKeyboardButton(
            f'☎️ {PROPERTY["phone"]}',
            url=f'tel:{clean_phone}'
        )])
    if PROPERTY.get('website') and PROPERTY['website'].strip():
        keyboard.append([InlineKeyboardButton(
            '🌐 Сайт',
            url=PROPERTY['website']
        )])
    if PROPERTY.get('telegram') and PROPERTY['telegram'].strip():
        keyboard.append([InlineKeyboardButton(
            '📱 Telegram',
            url=PROPERTY['telegram']
        )])
    keyboard.append([InlineKeyboardButton('🔙 Назад', callback_data='back_to_main')])
    
    await update.message.reply_text(
        info_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def contacts_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Контактная информация"""
    contact_text = f"""
📱 Контактная информация:

☎️ Телефон: {PROPERTY['phone']}

🌐 Веб-сайт: {PROPERTY['website']}

📧 Telegram: {PROPERTY['telegram']}

🏠 Адрес:
{PROPERTY['address']}

⏰ Режим работы: Круглосуточно

Желаете связаться с нами?
"""
    
    # Создаём клавиатуру с контактами
    keyboard = []
    if PROPERTY.get('phone') and PROPERTY['phone'].strip():
        clean_phone = _clean_phone_for_tel(PROPERTY['phone'])
        keyboard.append([InlineKeyboardButton(
            f'☎️ {PROPERTY["phone"]}',
            url=f'tel:{clean_phone}'
        )])
    if PROPERTY.get('website') and PROPERTY['website'].strip():
        keyboard.append([InlineKeyboardButton(
            '🌐 Сайт',
            url=PROPERTY['website']
        )])
    if PROPERTY.get('telegram') and PROPERTY['telegram'].strip():
        keyboard.append([InlineKeyboardButton(
            '📱 Telegram',
            url=PROPERTY['telegram']
        )])
    keyboard.append([InlineKeyboardButton('🔙 Назад', callback_data='back_to_main')])
    
    await update.message.reply_text(
        contact_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
