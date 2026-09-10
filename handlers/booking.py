"""
Обработчик бронирования
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ChatAction
from database import db
from keyboards import get_main_menu
from datetime import datetime, timedelta

# Состояния разговора
CHOOSE_SERVICE, INPUT_CHECKIN, INPUT_CHECKOUT, INPUT_GUESTS, INPUT_PHONE, CONFIRM = range(6)


async def booking_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало процесса бронирования"""
    from keyboards import get_services_keyboard
    
    message = "📅 Выберите услугу для бронирования:"
    await update.message.reply_text(
        message,
        reply_markup=get_services_keyboard()
    )
    
    return CHOOSE_SERVICE


async def get_checkin_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод даты заезда"""
    query = update.callback_query
    await query.answer()
    
    service_id = query.data.replace('service_', '')
    context.user_data['service_id'] = service_id
    
    message = "📅 Введите дату заезда (формат: дд.мм.гггг):\nНапример: 15.09.2026"
    await query.edit_message_text(message)
    
    return INPUT_CHECKIN


async def get_checkout_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод даты выезда"""
    try:
        checkin = datetime.strptime(update.message.text, '%d.%m.%Y').date()
        if checkin < datetime.now().date():
            await update.message.reply_text(
                "❌ Дата не может быть в прошлом. Попробуйте ещё раз:"
            )
            return INPUT_CHECKIN
        
        context.user_data['checkin_date'] = str(checkin)
        message = "📅 Введите дату выезда (формат: дд.мм.гггг):"
        await update.message.reply_text(message)
        
        return INPUT_CHECKOUT
    except ValueError:
        await update.message.reply_text(
            "❌ Неверный формат даты. Используйте дд.мм.гггг\nНапример: 15.09.2026"
        )
        return INPUT_CHECKIN


async def get_guests_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод количества гостей"""
    try:
        checkout = datetime.strptime(update.message.text, '%d.%m.%Y').date()
        checkin = datetime.strptime(context.user_data['checkin_date'], '%Y-%m-%d').date()
        
        if checkout <= checkin:
            await update.message.reply_text(
                "❌ Дата выезда должна быть позже даты заезда. Попробуйте ещё раз:"
            )
            return INPUT_CHECKOUT
        
        context.user_data['checkout_date'] = str(checkout)
        message = "👥 Введите количество гостей:"
        await update.message.reply_text(message)
        
        return INPUT_GUESTS
    except ValueError:
        await update.message.reply_text(
            "❌ Неверный формат даты. Используйте дд.мм.гггг"
        )
        return INPUT_CHECKOUT


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ввод номера телефона"""
    try:
        guests = int(update.message.text)
        if guests < 1 or guests > 50:
            await update.message.reply_text(
                "❌ Количество гостей должно быть от 1 до 50."
            )
            return INPUT_GUESTS
        
        context.user_data['guests_count'] = guests
        message = "☎️ Введите ваш номер телефона:\nНапример: +7 (999) 123-45-67"
        await update.message.reply_text(message)
        
        return INPUT_PHONE
    except ValueError:
        await update.message.reply_text(
            "❌ Введите число, пожалуйста."
        )
        return INPUT_GUESTS


async def confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение бронирования"""
    from config import SERVICES
    
    phone = update.message.text
    context.user_data['phone'] = phone
    
    service_id = context.user_data['service_id']
    service = SERVICES[service_id]
    
    confirmation_text = f"""
✅ Проверьте ваши данные:

🏨 Услуга: {service['name']}
📅 Заезд: {context.user_data['checkin_date']}
📅 Выезд: {context.user_data['checkout_date']}
👥 Гостей: {context.user_data['guests_count']}
☎️ Телефон: {phone}
💰 Цена: {service['price']}{service['currency']}/{service['unit']}

Всё верно?
"""
    
    from keyboards import get_confirmation_keyboard
    await update.message.reply_text(
        confirmation_text,
        reply_markup=get_confirmation_keyboard()
    )
    
    return CONFIRM


async def finalize_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершение бронирования"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'confirm':
        # Сохраняем бронирование в БД
        await db.add_booking(
            update.effective_user.id,
            context.user_data['service_id'],
            context.user_data['checkin_date'],
            context.user_data['checkout_date'],
            context.user_data['guests_count'],
            context.user_data['phone']
        )
        
        success_text = """
✅ Ваше бронирование успешно создано!

В скором времени с вами свяжется менеджер для подтверждения.

🙏 Спасибо за выбор нашего объекта!
"""
        await query.edit_message_text(
            success_text,
            reply_markup=get_main_menu()
        )
    else:
        await query.edit_message_text(
            "❌ Бронирование отменено.",
            reply_markup=get_main_menu()
        )
    
    return ConversationHandler.END


async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена бронирования"""
    await update.message.reply_text(
        "❌ Процесс бронирования отменен.",
        reply_markup=get_main_menu()
    )
    return ConversationHandler.END
