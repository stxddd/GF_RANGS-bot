import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.decorators.admin_required import admin_required
from bot.db.events.dao import EventDAO, RoleDAO
from bot.templates.kb_templates import add_role_text
from bot.templates.message_templates import (
    NO_EVENTS_FOR_ROLE_MESSAGE,
    EVENTS_LIST_MESSAGE,
    ENTER_EVENT_ID_MESSAGE,
    INVALID_EVENT_ID_MESSAGE,
    EVENT_NOT_FOUND_MESSAGE,
    ENTER_ROLE_NAME_MESSAGE,
    EMPTY_ROLE_NAME_MESSAGE,
    ENTER_ROLE_POINTS_MESSAGE,
    INVALID_ROLE_POINTS_MESSAGE,
    ROLE_ADDED_SUCCESS_MESSAGE,
    ROLE_ADD_ERROR_MESSAGE,
)

router = Router()


class AddRoleState(StatesGroup):
    waiting_for_event_id = State()
    waiting_for_name = State()
    waiting_for_points = State()
    
class EditRoleState(StatesGroup):
    waiting_for_name = State()
    waiting_for_points = State()

EDIT_ROLE_PATTERN = r"^edit_role:(\d+)$"

@router.message(F.text == add_role_text)
@admin_required
async def start_add_role(message: Message, state: FSMContext):
    events = await EventDAO.find_all()

    if not events:
        return await message.answer(NO_EVENTS_FOR_ROLE_MESSAGE)

    events_list = "\n".join([f"{event.id}: {event.name}" for event in events])
    await message.answer(EVENTS_LIST_MESSAGE.format(events=events_list))
    await state.set_state(AddRoleState.waiting_for_event_id)
    await message.answer(ENTER_EVENT_ID_MESSAGE)


@router.message(AddRoleState.waiting_for_event_id)
@admin_required
async def add_role_event_id(message: Message, state: FSMContext):
    try:
        event_id = int(message.text.strip())
    except ValueError:
        return await message.answer(INVALID_EVENT_ID_MESSAGE)

    event = await EventDAO.find_by_id(event_id)
    if not event:
        return await message.answer(EVENT_NOT_FOUND_MESSAGE)

    await state.update_data(event_id=event_id)
    await state.set_state(AddRoleState.waiting_for_name)
    await message.answer(ENTER_ROLE_NAME_MESSAGE)


@router.message(AddRoleState.waiting_for_name)
@admin_required
async def add_role_name(message: Message, state: FSMContext):
    name = message.text.strip()

    if not name:
        return await message.answer(EMPTY_ROLE_NAME_MESSAGE)

    await state.update_data(name=name)
    await state.set_state(AddRoleState.waiting_for_points)
    await message.answer(ENTER_ROLE_POINTS_MESSAGE)


@router.message(AddRoleState.waiting_for_points)
@admin_required
async def add_role_points(message: Message, state: FSMContext):
    try:
        points = int(message.text.strip())
    except ValueError:
        return await message.answer(INVALID_ROLE_POINTS_MESSAGE)

    data = await state.get_data()

    result = await RoleDAO.add(event_id=data["event_id"], name=data["name"], points=points)
    if result:
        await message.answer(
            ROLE_ADDED_SUCCESS_MESSAGE.format(
                name=data["name"],
                event_id=data["event_id"],
                points=points,
                role_id=result["id"]
            )
        )
    else:
        await message.answer(ROLE_ADD_ERROR_MESSAGE)

    await state.clear()


EDIT_ROLES_PATTERN = r"^edit_roles:(\d+)$"

@router.callback_query(F.data.regexp(EDIT_ROLES_PATTERN))
@admin_required
async def handle_edit_roles(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(EDIT_ROLES_PATTERN, callback.data)
    event_id = int(match.group(1))

    roles = await RoleDAO.find_all(event_id=event_id)
    if not roles:
        return await callback.message.answer("Роли для этого мероприятия не найдены.")

    keyboard = InlineKeyboardBuilder()
    for role in roles:
        keyboard.row(
            InlineKeyboardButton(
                text=f"{role.name} (Баллы: {role.points})",
                callback_data=f"edit_role:{role.id}"
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text="Отмена",
            callback_data="delete_last_message"
        )
    )
    await callback.message.answer("Выберите роль для редактирования:", reply_markup=keyboard.as_markup())


@router.callback_query(F.data.regexp(EDIT_ROLE_PATTERN))
@admin_required
async def handle_edit_role(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    match = re.match(EDIT_ROLE_PATTERN, callback.data)
    role_id = int(match.group(1))

    role = await RoleDAO.find_by_id(role_id)
    if not role:
        return await callback.message.answer("Роль не найдена.")

    await state.update_data(role_id=role_id)
    await state.set_state(EditRoleState.waiting_for_name)
    await callback.message.answer(f"Текущее название роли: {role.name}\nВведите новое название (или оставьте как есть):")


@router.message(EditRoleState.waiting_for_name)
@admin_required
async def process_role_name(message: Message, state: FSMContext):
    new_name = message.text.strip()
    data = await state.get_data()
    role_id = data.get("role_id")

    # Сохраняем новое имя, если оно не пустое, иначе оставляем старое
    if not new_name:
        return await message.answer("Название роли не может быть пустым. Введите заново:")

    await state.update_data(new_name=new_name)
    await state.set_state(EditRoleState.waiting_for_points)
    await message.answer("Введите новое количество баллов для роли:")

@router.message(EditRoleState.waiting_for_points)
@admin_required
async def process_role_points(message: Message, state: FSMContext):
    try:
        new_points = int(message.text.strip())
    except ValueError:
        return await message.answer("Баллы должны быть числом. Введите заново:")

    data = await state.get_data()
    role_id = data.get("role_id")
    new_name = data.get("new_name")

    updated = await RoleDAO.update(role_id, name=new_name, points=new_points)
    if updated:
        await message.answer(f"Роль успешно обновлена: {new_name} (Баллы: {new_points})")
    else:
        await message.answer("Ошибка при обновлении роли.")

    await state.clear()
