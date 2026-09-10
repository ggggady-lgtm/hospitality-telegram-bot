"""
Конфигурация Telegram бота
"""
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Основные настройки
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', 0))
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID', 0))

# База данных
DATABASE_PATH = os.getenv('DATABASE_PATH', './bot_database.db')

# Информация об объекте гостеприимства
PROPERTY = {
    'name': os.getenv('PROPERTY_NAME', 'Объект размещения'),
    'address': os.getenv('PROPERTY_ADDRESS', 'Адрес не указан'),
    'phone': os.getenv('PROPERTY_PHONE', 'Телефон не указан'),
    'website': os.getenv('PROPERTY_WEBSITE', ''),
    'telegram': os.getenv('PROPERTY_TELEGRAM', ''),
}

# Услуги и цены (можно редактировать)
SERVICES = {
    'main_house_14': {
        'name': 'Основной дом (14 человек)',
        'price': 40000,
        'currency': '₽',
        'unit': 'сутки'
    },
    'main_house_7': {
        'name': 'Часть дома (7 человек)',
        'price': 20000,
        'currency': '₽',
        'unit': 'сутки'
    },
    'main_house_2': {
        'name': 'Дом на 2 человека',
        'price': 12000,
        'currency': '₽',
        'unit': 'сутки'
    },
    'fireplace_hall': {
        'name': 'Каминный зал',
        'price': 3000,
        'currency': '₽',
        'unit': 'час'
    },
    'sauna': {
        'name': 'Баня Скандинавской рубки',
        'price': 5000,
        'currency': '₽',
        'unit': 'час'
    },
    'hot_tub': {
        'name': 'Купель на дровах',
        'price': 4000,
        'currency': '₽',
        'unit': 'час'
    },
}

# Параметры мониторинга
MONITORING = {
    'enable_availability': os.getenv('ENABLE_AVAILABILITY_MONITORING', 'true').lower() == 'true',
    'enable_reviews': os.getenv('ENABLE_REVIEW_MONITORING', 'true').lower() == 'true',
    'interval_hours': int(os.getenv('MONITORING_INTERVAL_HOURS', 6)),
}

# Параметры уведомлений
NOTIFICATIONS = {
    'booking': os.getenv('SEND_BOOKING_NOTIFICATIONS', 'true').lower() == 'true',
    'availability': os.getenv('SEND_AVAILABILITY_ALERTS', 'true').lower() == 'true',
    'reviews': os.getenv('SEND_REVIEW_ALERTS', 'true').lower() == 'true',
}

# Часовой пояс
TIMEZONE = 'Asia/Irkutsk'
