from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.users.dao import UserDAO
from bot.db.events.dao import UserEventRoleDAO, RoleDAO
from bot.templates.kb_templates import (
    yes_text,
    no_text,
    cancel_text,
    delete_text,
    left_text,
    right_text
)


async def get_users_to_edit(visibility: bool, event_id: int, page: int = 1, per_page: int = 15):
    user_event_role = await UserEventRoleDAO.find_all(event_id=event_id)
    
    total_users = len(user_event_role)
    total_pages = (total_users + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    user_page = user_event_role[start:end]
    
    keyboard = InlineKeyboardBuilder()

    for user_event_role_item in user_page:
        user = await UserDAO.find_by_id(user_event_role_item.user_id)
        role = await RoleDAO.find_by_id(user_event_role_item.role_id)
        if user:
            keyboard.row(
                InlineKeyboardButton(
                    text=f'{user.fullname} | {role.name}',
                    callback_data=f"get_user_to_edit_{user_event_role_item.id}",
                )
            )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text=left_text,
                callback_data=f"edit_user_page_{event_id}_{page - 1}",
            )
        )
    if total_pages != 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text=f'{page}/{total_pages}',
                callback_data="noop",
            )
        )
    
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(
                text=right_text,
                callback_data=f"edit_user_page_{event_id}_{page + 1}",
            )
        )

    if nav_buttons:
        keyboard.row(*nav_buttons)

    
    keyboard.row(
        InlineKeyboardButton(
            text=f"Сделать {'невидимым' if visibility else 'видимым'}",
            callback_data=f"toggle_visibility:{event_id}"
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Переименовать мероприятие",
            callback_data=f"rename_event:{event_id}"
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Изменить роли",
            callback_data=f"edit_roles:{event_id}"
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text=cancel_text,
            callback_data="delete_last_message",
        )
    )

    return keyboard.as_markup()


def delete_user_kb(user_role_event_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=delete_text,
                    callback_data=f"prepare_to_delete_user_role_event_{user_role_event_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=cancel_text, callback_data="delete_last_message"
                )
            ],
        ]
    )


def yes_or_not_delete_user_role_event_keyboard(user_role_event_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=yes_text, callback_data=f"delete_user_role_event_{user_role_event_id}"
                ),
                InlineKeyboardButton(
                    text=no_text, callback_data="delete_last_message"
                ),
            ],
        ]
    )

