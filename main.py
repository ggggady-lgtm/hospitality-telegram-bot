"""
Главный файл Telegram бота
"""
import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)
from telegram.constants import ChatAction

from config import TELEGRAM_BOT_TOKEN, ADMIN_USER_ID
from database import db

# Импортируем обработчики
from handlers.start import start_handler, help_handler
from handlers.info import info_handler, contacts_handler
from handlers.prices import prices_handler, service_callback
from handlers.booking import (
    booking_start, get_checkin_date, get_checkout_date,
    get_guests_count, get_phone, confirm_booking, finalize_booking,
    cancel_booking, CHOOSE_SERVICE, INPUT_CHECKIN, INPUT_CHECKOUT,
    INPUT_GUESTS, INPUT_PHONE, CONFIRM
)
from handlers.notifications import notifications_handler, notification_callback

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def text_handler(update, context):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    
    # Обработка кнопок главного меню
    if text == 'ℹ️ Информация':
        await info_handler(update, context)
    elif text == '💰 Цены':
        await prices_handler(update, context)
    elif text == '📅 Бронировать':
        return await booking_start(update, context)
    elif text == '✅ Доступность':
        await update.message.reply_text(
            "🔍 Проверка доступности услуг...\n\n"
            "К сожалению, функция в разработке.\n"
            "Пожалуйста, свяжитесь с нами по телефону для уточнения доступности."
        )
    elif text == '🔔 Уведомления':
        await notifications_handler(update, context)
    elif text == '⭐ Отзывы':
        await update.message.reply_text(
            "⭐ Спасибо за интерес к нашим отзывам!\n\n"
            "Оставляйте отзывы на:\n"
            "📍 Яндекс.Карты\n"
            "📍 2GIS\n"
            "📍 Zoon.ru\n\n"
            "Ваше мнение очень важно для нас! 😊"
        )
    elif text == '📱 Контакты':
        await contacts_handler(update, context)
    else:
        await update.message.reply_text(
            "Пожалуйста, используйте кнопки меню для навигации."
        )


async def back_to_main(update, context):
    """Вернуться в главное меню"""
    from keyboards import get_main_menu
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🏠 Главное меню",
        reply_markup=get_main_menu()
    )


async def admin_handler(update, context):
    """Обработчик админ-команд"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text(
            "❌ У вас нет прав доступа к админ-функциям."
        )
        return
    
    admin_menu = """
⚙️ Админ-панель

/bookings - Список бронирований
/stats - Статистика
/send_message - Отправить сообщение всем пользователям
/settings - Настройки бота
    """
    
    await update.message.reply_text(admin_menu)


async def bookings_admin(update, context):
    """Показать список бронирований для админа"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_USER_ID:
        return
    
    bookings = await db.get_bookings()
    
    if not bookings:
        await update.message.reply_text("📭 Нет бронирований.")
        return
    
    bookings_text = "📋 Список бронирований:\n\n"
    for booking in bookings:
        bookings_text += f"""
🔹 ID: {booking[0]}
   Услуга: {booking[2]}
   Заезд: {booking[3]}
   Выезд: {booking[4]}
   Гостей: {booking[5]}
   Телефон: {booking[6]}
   Статус: {booking[7]}
---
"""
    
    await update.message.reply_text(bookings_text)


async def post_init(app):
    """Инициализация бота"""
    await db.init_db()
    logger.info("✅ База данных инициализирована")


def main():
    """Главная функция"""
    logger.info("🚀 Запуск Telegram бота...")
    
    # Создание приложения
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Добавляем инициализацию БД
    app.post_init = post_init
    
    # Обработчик бронирования (ConversationHandler)
    booking_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^📅 Бронировать$'), booking_start)],
        states={
            CHOOSE_SERVICE: [CallbackQueryHandler(get_checkin_date, pattern=r'^service_')],
            INPUT_CHECKIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_checkout_date)],
            INPUT_CHECKOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_guests_count)],
            INPUT_GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            INPUT_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_booking)],
            CONFIRM: [CallbackQueryHandler(finalize_booking, pattern=r'^(confirm|cancel)_booking$')],
        },
        fallbacks=[CommandHandler('cancel', cancel_booking)],
    )
    
    # Добавляем обработчики
    app.add_handler(CommandHandler('start', start_handler))
    app.add_handler(CommandHandler('help', help_handler))
    app.add_handler(CommandHandler('info', info_handler))
    app.add_handler(CommandHandler('prices', prices_handler))
    app.add_handler(CommandHandler('contacts', contacts_handler))
    app.add_handler(CommandHandler('notifications', notifications_handler))
    app.add_handler(CommandHandler('admin', admin_handler))
    app.add_handler(CommandHandler('bookings', bookings_admin))
    
    # Обработчик бронирования
    app.add_handler(booking_conv_handler)
    
    # Обработчики callback кнопок (ДО обработчика текста!)
    app.add_handler(CallbackQueryHandler(service_callback, pattern=r'^service_'))
    app.add_handler(CallbackQueryHandler(notification_callback, pattern=r'^notif_'))
    app.add_handler(CallbackQueryHandler(back_to_main, pattern=r'^back_to_main$'))
    
    # Обработчик текстовых сообщений (ПОСЛЕДНИЙ!)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    # Запуск бота
    logger.info("✅ Бот запущен успешно!")
    app.run_polling()


if __name__ == '__main__':
    main()
