from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.templates.kb_templates import (
    my_point_text,
    get_points_text,
    get_conditions_text,
    add_event_text,
    add_role_text,
    view_all_events_text,
    view_all_users_text

)
from utils.check_admin_tg_id import check_admin_tg_id


def main_menu_kb(tg_id):
    
    keyboard = [
        [KeyboardButton(text=my_point_text)],
        [KeyboardButton(text=get_points_text)],
        [KeyboardButton(text=get_conditions_text)],
    ]
    
    if check_admin_tg_id(tg_id):
        keyboard.append([KeyboardButton(text=add_event_text)])
        keyboard.append([KeyboardButton(text=add_role_text)])
        keyboard.append([KeyboardButton(text=view_all_events_text)])
        keyboard.append([KeyboardButton(text=view_all_users_text)])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    




