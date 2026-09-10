"""
Обработчик команды /start
"""
from telegram import Update
from telegram.ext import ContextTypes
from database import db
from keyboards import get_main_menu
from config import PROPERTY


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    # Добавляем пользователя в БД
    await db.add_user(
        user.id,
        user.username,
        user.first_name,
        user.last_name
    )
    
    welcome_message = f"""
🏨 Добро пожаловать в {PROPERTY['name']}!

Мы предлагаем:
✅ Уютные номера для отдыха
🔥 Русскую баню на дровах
🎉 Каминный зал для мероприятий
🌲 Красивую территорию среди соснового леса

Выберите, что вас интересует:
"""
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_menu()
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
📖 Справка по командам:

/start - Главное меню
/info - Информация об объекте
/prices - Прайс-лист услуг
/book - Форма бронирования
/availability - Проверить доступность
/notifications - Управление уведомлениями
/contacts - Контактная информация
/help - Справка

❓ Если возникли вопросы, свяжитесь с нами через контакты.
"""
    
    await update.message.reply_text(help_text)
