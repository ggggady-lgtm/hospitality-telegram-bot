"""
Обработчик информации об объекте
"""
from telegram import Update
from telegram.ext import ContextTypes
from config import PROPERTY
from keyboards import get_contact_keyboard, get_main_menu


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
    
    await update.message.reply_text(
        info_text,
        reply_markup=get_contact_keyboard()
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
    
    await update.message.reply_text(
        contact_text,
        reply_markup=get_contact_keyboard()
    )
