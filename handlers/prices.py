"""
Обработчик информации о ценах
"""
from telegram import Update
from telegram.ext import ContextTypes
from config import SERVICES
from keyboards import get_services_keyboard, get_main_menu


async def prices_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать прайс-лист"""
    prices_text = "💰 Прайс-лист услуг:\n\n"
    
    # Услуги размещения
    prices_text += "🏨 Размещение:\n"
    for service_id in ['main_house_14', 'main_house_7', 'main_house_2']:
        service = SERVICES[service_id]
        prices_text += f"• {service['name']}: {service['price']}{service['currency']}/{service['unit']}\n"
    
    prices_text += "\n🔥 Дополнительные услуги:\n"
    for service_id in ['fireplace_hall', 'sauna', 'hot_tub']:
        service = SERVICES[service_id]
        prices_text += f"• {service['name']}: {service['price']}{service['currency']}/{service['unit']}\n"
    
    prices_text += "\n⚠️ Цены могут изменяться. Уточняйте актуальную стоимость перед бронированием.\n"
    prices_text += "\nВыберите услугу для подробной информации:"
    
    await update.message.reply_text(
        prices_text,
        reply_markup=get_services_keyboard()
    )


async def service_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора услуги"""
    query = update.callback_query
    await query.answer()
    
    service_id = query.data.replace('service_', '')
    service = SERVICES.get(service_id)
    
    if not service:
        await query.edit_message_text("Услуга не найдена.")
        return
    
    service_text = f"""
📌 {service['name']}

Цена: {service['price']}{service['currency']}/{service['unit']}

Услуга включает полный комплект удобств для комфортного отдыха.

Для бронирования нажмите кнопку ниже:
"""
    
    from keyboards import get_confirmation_keyboard
    context.user_data['selected_service'] = service_id
    
    await query.edit_message_text(
        service_text,
        reply_markup=get_confirmation_keyboard()
    )
