"""
Управление базой данных SQLite
"""
import aiosqlite
import json
from datetime import datetime
from config import DATABASE_PATH


class Database:
    """Класс для работы с базой данных"""
    
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
    
    async def init_db(self):
        """Инициализация базы данных"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_subscribed BOOLEAN DEFAULT 1,
                    notification_type TEXT DEFAULT 'all'
                );
                
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    service_id TEXT,
                    check_in_date DATE,
                    check_out_date DATE,
                    guests_count INTEGER,
                    phone TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                );
                
                CREATE TABLE IF NOT EXISTS availability (
                    availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_id TEXT,
                    date DATE,
                    available BOOLEAN,
                    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS reviews (
                    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rating REAL,
                    text TEXT,
                    source TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed BOOLEAN DEFAULT 0
                );
                
                CREATE TABLE IF NOT EXISTS notifications (
                    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT,
                    notification_type TEXT,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                );
                
                CREATE TABLE IF NOT EXISTS admin_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await db.commit()
    
    # ===== Пользователи =====
    async def add_user(self, user_id, username, first_name, last_name):
        """Добавить нового пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT OR IGNORE INTO users 
                   (user_id, username, first_name, last_name) 
                   VALUES (?, ?, ?, ?)""",
                (user_id, username, first_name, last_name)
            )
            await db.commit()
    
    async def get_user(self, user_id):
        """Получить информацию о пользователе"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT * FROM users WHERE user_id = ?", 
                (user_id,)
            )
            return await cursor.fetchone()
    
    async def get_all_users(self):
        """Получить всех пользователей"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT user_id FROM users")
            return await cursor.fetchall()
    
    async def toggle_subscription(self, user_id, is_subscribed):
        """Изменить статус подписки пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET is_subscribed = ? WHERE user_id = ?",
                (is_subscribed, user_id)
            )
            await db.commit()
    
    # ===== Бронирования =====
    async def add_booking(self, user_id, service_id, check_in, check_out, guests, phone):
        """Добавить бронирование"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO bookings 
                   (user_id, service_id, check_in_date, check_out_date, guests_count, phone) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, service_id, check_in, check_out, guests, phone)
            )
            await db.commit()
    
    async def get_bookings(self, start_date=None, end_date=None):
        """Получить бронирования"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            
            if start_date and end_date:
                cursor = await db.execute(
                    """SELECT * FROM bookings 
                       WHERE check_in_date >= ? AND check_out_date <= ?
                       ORDER BY check_in_date""",
                    (start_date, end_date)
                )
            else:
                cursor = await db.execute(
                    "SELECT * FROM bookings ORDER BY check_in_date DESC LIMIT 50"
                )
            
            return await cursor.fetchall()
    
    async def update_booking_status(self, booking_id, status):
        """Обновить статус бронирования"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE bookings SET status = ? WHERE booking_id = ?",
                (status, booking_id)
            )
            await db.commit()
    
    # ===== Доступность =====
    async def set_availability(self, service_id, date, available):
        """Установить доступность услуги"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO availability (service_id, date, available) 
                   VALUES (?, ?, ?)
                   ON CONFLICT(service_id, date) DO UPDATE SET available = ?""",
                (service_id, date, available, available)
            )
            await db.commit()
    
    async def get_availability(self, service_id, start_date, end_date):
        """Получить доступность услуги на период"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """SELECT * FROM availability 
                   WHERE service_id = ? AND date BETWEEN ? AND ?
                   ORDER BY date""",
                (service_id, start_date, end_date)
            )
            return await cursor.fetchall()
    
    # ===== Отзывы =====
    async def add_review(self, rating, text, source):
        """Добавить отзыв"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO reviews (rating, text, source) VALUES (?, ?, ?)",
                (rating, text, source)
            )
            await db.commit()
    
    async def get_unprocessed_reviews(self):
        """Получить необработанные отзывы"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM reviews WHERE processed = 0"
            )
            return await cursor.fetchall()
    
    async def mark_review_processed(self, review_id):
        """Отметить отзыв как обработанный"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE reviews SET processed = 1 WHERE review_id = ?",
                (review_id,)
            )
            await db.commit()
    
    # ===== Уведомления =====
    async def add_notification(self, user_id, message, notification_type):
        """Добавить уведомление"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO notifications 
                   (user_id, message, notification_type) 
                   VALUES (?, ?, ?)""",
                (user_id, message, notification_type)
            )
            await db.commit()
    
    # ===== Логи =====
    async def add_log(self, action, details):
        """Добавить запись в лог"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO admin_logs (action, details) VALUES (?, ?)",
                (action, details)
            )
            await db.commit()


# Глобальный объект базы данных
db = Database()
