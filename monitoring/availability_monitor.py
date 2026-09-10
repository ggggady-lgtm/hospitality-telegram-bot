"""
Мониторинг доступности услуг
"""
import aiohttp
from datetime import datetime, timedelta
from database import db
from config import MONITORING, NOTIFICATIONS
import logging

logger = logging.getLogger(__name__)


class AvailabilityMonitor:
    """Класс для мониторинга доступности"""
    
    def __init__(self):
        self.last_check = None
    
    async def check_availability(self):
        """Проверить доступность услуг"""
        if not MONITORING['enable_availability']:
            return
        
        try:
            # Здесь можно добавить логику проверки доступности
            # Например, парсинг сайта или API
            logger.info('Availability check completed')
            self.last_check = datetime.now()
        except Exception as e:
            logger.error(f'Availability check failed: {e}')
    
    async def notify_users_about_availability(self, service_id, is_available):
        """Отправить уведомления о доступности"""
        if not NOTIFICATIONS['availability']:
            return
        
        users = await db.get_all_users()
        status = '✅ Доступно' if is_available else '❌ Недоступно'
        
        for user in users:
            message = f"{status}\n\nУслуга {service_id} теперь {status.lower()}"
            await db.add_notification(
                user[0],
                message,
                'availability'
            )
