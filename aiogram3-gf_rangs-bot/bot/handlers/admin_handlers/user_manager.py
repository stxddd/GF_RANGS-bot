import re
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.kb.users_kb import delete_user_kb, get_users_to_edit, yes_or_not_delete_user_role_event_keyboard
from bot.db.users.dao import UserDAO
from bot.db.events.dao import EventDAO, RoleDAO, UserEventRoleDAO
from bot.templates.message_templates import (
    user_info_message,
    are_you_sure_to_delete_user_message,
    USER_NOT_FOUND_MESSAGE,
    USER_DELETE_ERROR_MESSAGE,
    USER_DELETED_MESSAGE,
)
from utils.decorators.admin_required import admin_required

router = Router()

EDIT_USER_PAGE_PATTERN = r"^edit_user_page_(\d+)_(\d+)$"
GET_USER_TO_EDIT_PATTERN = r"^get_user_to_edit_(\d+)$"
PREPARE_TO_DELETE_USER_PATTERN = r"^prepare_to_delete_user_role_event_(\d+)$"
DELETE_USER_PATTERN = r"^delete_user_role_event_(\d+)$"


async def get_user_event_role_data(user_event_role):
    """Получение user, role, event по user_event_role"""
    user = await UserDAO.find_by_id(user_event_role.user_id)
    role = await RoleDAO.find_by_id(user_event_role.role_id)
    event = await EventDAO.find_by_id(user_event_role.event_id)
    return user, role, event


@router.callback_query(F.data.regexp(EDIT_USER_PAGE_PATTERN))
async def handle_pagination(callback: CallbackQuery):
    """Обработка пагинации"""
    await callback.answer()

    match = re.match(EDIT_USER_PAGE_PATTERN, callback.data)
    event_id = int(match.group(1))
    page = int(match.group(2))

    await callback.message.edit_reply_markup(
        reply_markup=await get_users_to_edit(event_id=event_id, page=page)
    )


@router.callback_query(F.data.regexp(GET_USER_TO_EDIT_PATTERN))
async def handle_get_connection_to_edit(callback: CallbackQuery):
    """Открытие информации о пользователе"""
    await callback.answer()

    match = re.match(GET_USER_TO_EDIT_PATTERN, callback.data)
    user_event_role_id = int(match.group(1))

    user_event_role = await UserEventRoleDAO.find_by_id(user_event_role_id)
    if not user_event_role:
        return await callback.message.answer(USER_NOT_FOUND_MESSAGE)

    user, role, event = await get_user_event_role_data(user_event_role)

    await callback.message.answer(
        user_info_message(user=user, role=role, event=event),
        reply_markup=delete_user_kb(user_event_role_id)
    )


@router.callback_query(F.data.regexp(PREPARE_TO_DELETE_USER_PATTERN))
@admin_required
async def handle_prepare_to_delete_client(callback: CallbackQuery, state: FSMContext):
    """Подтверждение удаления пользователя"""
    await callback.answer()

    match = re.match(PREPARE_TO_DELETE_USER_PATTERN, callback.data)
    user_event_role_id = int(match.group(1))

    user_event_role = await UserEventRoleDAO.find_by_id(user_event_role_id)
    if not user_event_role:
        return await callback.message.answer(USER_NOT_FOUND_MESSAGE)

    await state.update_data(user_event_role=user_event_role)

    user, role, event = await get_user_event_role_data(user_event_role)

    return await callback.message.answer(
        are_you_sure_to_delete_user_message(user, event, role),
        reply_markup=yes_or_not_delete_user_role_event_keyboard(user_role_event_id=user_event_role_id),
    )


@router.callback_query(F.data.regexp(DELETE_USER_PATTERN))
@admin_required
async def handle_delete_client(callback: CallbackQuery):
    """Удаление пользователя"""
    await callback.answer()

    match = re.match(DELETE_USER_PATTERN, callback.data)
    user_event_role_id = int(match.group(1))

    user_event_role = await UserEventRoleDAO.find_by_id(user_event_role_id)
    if not user_event_role:
        return await callback.message.answer(USER_NOT_FOUND_MESSAGE)

    if not await UserEventRoleDAO.delete(id=user_event_role_id):
        return await callback.message.answer(USER_DELETE_ERROR_MESSAGE)

    return await callback.message.answer(USER_DELETED_MESSAGE)
