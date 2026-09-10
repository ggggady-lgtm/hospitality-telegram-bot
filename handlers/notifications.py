"""
Обработчик уведомлений
"""
from telegram import Update
from telegram.ext import ContextTypes
from database import db
from keyboards import get_notification_settings_keyboard, get_main_menu


async def notifications_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управление уведомлениями"""
    message = """
🔔 Управление уведомлениями

Выберите, какие уведомления вы хотите получать:

📅 Бронирования - уведомления о статусе вашего бронирования
✅ Доступность - оповещения о доступности услуг
⭐ Отзывы - новые отзывы и предложения
🔔 Все - получать все уведомления
🔇 Отключить все - не получать никаких уведомлений
    """
    
    await update.message.reply_text(
        message,
        reply_markup=get_notification_settings_keyboard()
    )


async def notification_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора типа уведомлений"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    notification_types = {
        'notif_booking': 'bookings',
        'notif_availability': 'availability',
        'notif_reviews': 'reviews',
        'notif_all': 'all',
        'notif_none': 'none'
    }
    
    notif_type = notification_types.get(callback_data)
    
    if notif_type:
        # Обновляем настройки пользователя в БД
        # (требуется добавить в database.py)
        
        messages = {
            'bookings': '✅ Вы будете получать уведомления о бронированиях',
            'availability': '✅ Вы будете получать оповещения о доступности',
            'reviews': '✅ Вы будете получать уведомления об отзывах',
            'all': '✅ Вы будете получать все уведомления',
            'none': '✅ Вы отключили все уведомления'
        }
        
        text = messages.get(notif_type, 'Настройка обновлена')
        await query.edit_message_text(
            text,
            reply_markup=get_main_menu()
        )
