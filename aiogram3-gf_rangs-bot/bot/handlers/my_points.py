from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from utils.decorators.admin_required import admin_required

from bot.templates.kb_templates import my_point_text
from bot.db.users.dao import UserDAO
from bot.db.events.dao import UserEventRoleDAO, EventDAO, RoleDAO
from bot.templates.message_templates import your_points_message


router = Router()

@router.message(F.text == my_point_text)
@admin_required
async def start_add_role(message: Message):
    user = await UserDAO.find_one_or_none(tg_id = message.from_user.id)
    if not user:
        return await message.answer('Вы не зарегистрированы!')
    
    user_role_event = await UserEventRoleDAO.find_all(user_id = user.id)
    
    if not user_role_event:
        return await message.answer('Вы не зарегистрированы ни на одном мероприятии!')
    
    points = await UserDAO.get_total_points_by_user_id(user.id)
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    events_info = []
    for user_role_event_item in user_role_event:
        event = await EventDAO.find_one_or_none(id = user_role_event_item.event_id)
        role = await RoleDAO.find_one_or_none(id = user_role_event_item.role_id)
        events_info.append(f"🔹 {event.name} | {role.name} -> {role.points}")
        
    await message.answer(your_points_message(date = timestamp, points = points, events_info = events_info))
    
    