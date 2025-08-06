from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message

from bot.templates.kb_templates import my_point_text, get_points_text
from bot.db.users.dao import UserDAO
from bot.db.events.dao import UserEventRoleDAO, EventDAO, RoleDAO
from bot.templates.message_templates import (
    your_points_message,
    you_need_to_register_message,
    no_user_role_events_text,
)
from utils.calculate_rank import get_rank_and_remaining
from bot.kb.main_menu_kb import main_menu_kb

router = Router()

@router.message(F.text == my_point_text)
async def start_add_role(message: Message):
    user = await UserDAO.find_one_or_none(tg_id = message.from_user.id)
    if not user or not(user.is_approved):
        return await message.answer(you_need_to_register_message)
    
    user_role_event = await UserEventRoleDAO.find_all(user_id = user.id)
    
    if not user_role_event:
        return await message.answer(no_user_role_events_text)
    
    points = await UserDAO.get_total_points_by_user_id(user.id)
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    events_info = []
    for user_role_event_item in user_role_event:
        event = await EventDAO.find_one_or_none(id = user_role_event_item.event_id)
        role = await RoleDAO.find_one_or_none(id = user_role_event_item.role_id)
        events_info.append(f"🔹 {event.name} | {role.name} -> {role.points}")
    
    rank_info = await get_rank_and_remaining(user.id)   
    
    await message.answer(your_points_message(date = timestamp, points = points, events_info = events_info, rank_info= rank_info), reply_markup=main_menu_kb(message.from_user.id))
    