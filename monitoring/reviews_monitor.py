"""
Мониторинг отзывов
"""
import aiohttp
from database import db
from config import NOTIFICATIONS, ADMIN_CHAT_ID
import logging

logger = logging.getLogger(__name__)


class ReviewsMonitor:
    """Класс для мониторинга отзывов"""
    
    async def check_reviews(self):
        """Проверить новые отзывы"""
        try:
            # Здесь можно добавить логику парсинга отзывов
            # Например, с Яндекс.Карт, Zoon.ru, 2GIS
            logger.info('Reviews check completed')
        except Exception as e:
            logger.error(f'Reviews check failed: {e}')
    
    async def notify_admins_about_review(self, rating, text, source):
        """Отправить уведомление администраторам о новом отзыве"""
        if not NOTIFICATIONS['reviews']:
            return
        
        message = f"""
⭐ Новый отзыв на {source}!

Рейтинг: {'⭐' * int(rating)}

Текст: {text}
"""
        
        # Уведомление будет отправлено в админ чат
        return message
