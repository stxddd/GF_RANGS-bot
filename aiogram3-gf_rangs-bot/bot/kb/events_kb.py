from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.events.dao import RoleDAO, UserEventRoleDAO
from bot.templates.kb_templates import (
    cancel_text,
    delete_text,
    yes_text,
    no_text,
    left_text,
    right_text
)
from utils.check_admin_tg_id import check_admin_tg_id

async def get_events_for_edit(events, tg_id, page: int = 1, per_page: int = 10):
    total_events = len(events)
    total_pages = (total_events + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    events_page = events[start:end]

    keyboard = InlineKeyboardBuilder()

    for event in events_page:
        if event.visibility or check_admin_tg_id(tg_id):
            user_role_events = await UserEventRoleDAO.find_all(event_id = event.id)
            keyboard.row(
                InlineKeyboardButton(
                    text= str("🤐 " if not event.visibility else "") + f"{event.name} 👤 {len(user_role_events)}" ,
                    callback_data=f"get_event_to_edit_{event.id}",
                )
            )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text=left_text,
                callback_data=f"edit_page_{page - 1}",
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
                callback_data=f"edit_page_{page + 1}",
            )
        )

    if nav_buttons:
        keyboard.row(*nav_buttons)

    keyboard.row(
        InlineKeyboardButton(
            text=cancel_text,
            callback_data="delete_last_message",
        )
    )

    
    return keyboard.as_markup()


def delete_event_kb(event_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=delete_text,
                    callback_data=f"prepare_to_delete_event_{event_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=cancel_text, callback_data="delete_last_message"
                )
            ],
        ]
    )


def yes_or_not_delete_event_keyboard(event_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=yes_text, callback_data=f"delete_event_{event_id}"
                ),
                InlineKeyboardButton(
                    text=no_text, callback_data="delete_last_message"
                ),
            ],
        ]
    )

def category_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Культ-масс", callback_data="category:cult")],
        [InlineKeyboardButton(text="Медиа", callback_data="category:media")]
    ])
    

async def get_events_kb(events, tg_id, page: int = 1, per_page: int = 10):
    total_events = len(events)
    total_pages = (total_events + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    events_page = events[start:end]

    keyboard = InlineKeyboardBuilder()

    for event in events_page:
        if event.visibility or check_admin_tg_id(tg_id):
            keyboard.row(
                InlineKeyboardButton(
                    text= str("🤐 " if not event.visibility else "") + f"{event.name}" ,
                    callback_data=f"get_event:{event.id}",
                )
            )

    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text=left_text,
                callback_data=f"edit_event_page_{page - 1}",
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
                callback_data=f"edit_event_page_{page + 1}",
            )
        )

    if nav_buttons:
        keyboard.row(*nav_buttons)

    keyboard.row(
        InlineKeyboardButton(
            text=cancel_text,
            callback_data="delete_last_message",
        )
    )

    
    return keyboard.as_markup()

async def role_kb(event_id):
    roles = await RoleDAO.find_all(event_id=event_id)
    
    keyboard = InlineKeyboardBuilder()
    
    for role in roles:
        keyboard.row(
            InlineKeyboardButton(
                text = f'{role.name} | {role.points}',
                callback_data=f"role:{role.id}",
            )
        )

    return keyboard.as_markup()