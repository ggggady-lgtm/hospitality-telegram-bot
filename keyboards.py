"""
Клавиатуры и кнопки для Telegram бота
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import SERVICES, PROPERTY
import re


def get_main_menu():
    """Главное меню"""
    keyboard = [
        [KeyboardButton('ℹ️ Информация'), KeyboardButton('💰 Цены')],
        [KeyboardButton('📅 Бронировать'), KeyboardButton('✅ Доступность')],
        [KeyboardButton('🔔 Уведомления'), KeyboardButton('⭐ Отзывы')],
        [KeyboardButton('📱 Контакты')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def get_admin_menu():
    """Админ меню"""
    keyboard = [
        [KeyboardButton('👥 Бронирования'), KeyboardButton('📊 Статистика')],
        [KeyboardButton('⚙️ Управление'), KeyboardButton('📤 Рассылка')],
        [KeyboardButton('🔙 Назад')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_services_keyboard():
    """Клавиатура выбора услуг"""
    keyboard = []
    for service_id, service in SERVICES.items():
        btn_text = f"{service['name']} - {service['price']}{service['currency']}/{service['unit']}"
        keyboard.append([
            InlineKeyboardButton(
                btn_text,
                callback_data=f"service_{service_id}"
            )
        ])
    keyboard.append([InlineKeyboardButton('🔙 Назад', callback_data='back_to_main')])
    return InlineKeyboardMarkup(keyboard)


def get_confirmation_keyboard():
    """Клавиатура подтверждения"""
    keyboard = [
        [InlineKeyboardButton('✅ Подтвердить', callback_data='confirm_booking'),
         InlineKeyboardButton('❌ Отмена', callback_data='cancel_booking')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_notification_settings_keyboard():
    """Клавиатура настроек уведомлений"""
    keyboard = [
        [InlineKeyboardButton('📅 Бронирования', callback_data='notif_booking'),
         InlineKeyboardButton('✅ Доступность', callback_data='notif_availability')],
        [InlineKeyboardButton('⭐ Отзывы', callback_data='notif_reviews'),
         InlineKeyboardButton('🔔 Все', callback_data='notif_all')],
        [InlineKeyboardButton('🔇 Отключить все', callback_data='notif_none'),
         InlineKeyboardButton('🔙 Назад', callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)


def _clean_phone_for_tel(phone):
    """Очистить номер телефона для tel: URL (только цифры и +)"""
    return re.sub(r'[^\d+]', '', phone)


def get_contact_keyboard():
    """Клавиатура с контактами"""
    keyboard = []
    if PROPERTY['phone']:
        clean_phone = _clean_phone_for_tel(PROPERTY['phone'])
        keyboard.append([InlineKeyboardButton(
            f'☎️ {PROPERTY["phone"]}',
            url=f'tel:{clean_phone}'
        )])
    if PROPERTY['website']:
        keyboard.append([InlineKeyboardButton(
            '🌐 Сайт',
            url=PROPERTY['website']
        )])
    if PROPERTY['telegram']:
        keyboard.append([InlineKeyboardButton(
            '📱 Telegram',
            url=PROPERTY['telegram']
        )])
    keyboard.append([InlineKeyboardButton('🔙 Назад', callback_data='back_to_main')])
    return InlineKeyboardMarkup(keyboard)
