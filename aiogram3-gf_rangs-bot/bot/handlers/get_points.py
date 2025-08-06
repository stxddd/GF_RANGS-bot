import os
import random
import aiofiles
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.templates.kb_templates import get_points_text
from bot.templates.message_templates import (
    enter_event_message,
    enter_role_message,
    you_need_to_register_message,
    enter_media_message,
    participation_added_message
)
from bot.db.users.dao import UserDAO
from bot.db.events.dao import RoleDAO, UserEventRoleDAO, EventDAO
from bot.kb.events_kb import get_events_kb, role_kb
from config import settings
from bot.kb.main_menu_kb import main_menu_kb

media_dir = settings.MEDIA_DIR
router = Router()


class RegistrationFSM(StatesGroup):
    category = State()
    event = State()
    role = State()
    media = State()

processed_media_groups = set()

@router.message(F.text == get_points_text)
async def start_add_role(message: Message):
    user = await UserDAO.find_one_or_none(tg_id=message.from_user.id)
    if not user or not(user.is_approved):
        return await message.answer(you_need_to_register_message)
    events = await EventDAO.find_all(visibility=True)
    kb = await get_events_kb(events=events, tg_id=message.from_user.id) if len(events) > 0 else None
    return await message.answer(
        enter_event_message(len(events)),
        reply_markup=kb
    )


@router.callback_query(F.data.startswith("edit_event_page_"))
async def change_events_page(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[-1])
    events = await EventDAO.find_all(visibility=True)
    kb = await get_events_kb(events, callback.from_user.id, page=page)
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data.startswith("get_event:"))
async def choose_event(callback: CallbackQuery, state: FSMContext):
    event_id = int(callback.data.split(":")[1])
    roles = await RoleDAO.find_all(event_id=event_id)
        
    kb = await role_kb(roles) if len(roles) > 0 else None
    await state.update_data(event_id=event_id)
    await state.set_state(RegistrationFSM.role)
    await callback.message.edit_text(enter_role_message(len(roles)), reply_markup=kb)


@router.callback_query(F.data.startswith("role:"))
async def choose_role(callback: CallbackQuery, state: FSMContext):
    role_id = callback.data.split(":")[1]
    await state.update_data(role_id=role_id)
    await state.set_state(RegistrationFSM.media)
    await callback.message.edit_text(enter_media_message)

@router.message(RegistrationFSM.media)
async def get_media_or_link(message: Message, state: FSMContext):
    data = await state.get_data()
    user = await UserDAO.find_one_or_none(tg_id=message.from_user.id)

    if not user:
        await message.answer(you_need_to_register_message)
        return

    if message.media_group_id and message.media_group_id in processed_media_groups:
        return

    if data.get("registration_in_progress"):
        return

    await state.update_data(registration_in_progress=True)

    try:
        if message.media_group_id:
            processed_media_groups.add(message.media_group_id)

        media_path = ""

        # Проверка текста или файла
        if message.text:
            media_path = message.text
        else:
            file_id = (
                message.photo[-1].file_id if message.photo else
                message.video.file_id if message.video else None
            )

            if not file_id:
                await message.answer("Пожалуйста, отправь ссылку или медиафайл.")
                await state.update_data(registration_in_progress=False)
                return

            file = await message.bot.get_file(file_id)

            if file.file_size > settings.MAX_FILE_SIZE:
                await message.answer("❌ Файл слишком большой. Максимальный размер: 20 МБ.")
                await state.update_data(registration_in_progress=False)
                return

            ext = (
                "jpg" if message.photo else
                "mp4" if message.video else
                (message.document.file_name.split(".")[-1] if message.document else "bin")
            )

            file_path = os.path.join(media_dir, f"{user.id}_{data['event_id']}_{random.randint(1000,9999)}_media.{ext}")
            os.makedirs(media_dir, exist_ok=True)

            file_bytes = await message.bot.download_file(file.file_path)
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(file_bytes.read())

            media_path = file_path

        # Создаём запись только после проверки медиа
        new_record = await UserEventRoleDAO.add(
            event_id=int(data["event_id"]),
            user_id=user.id,
            role_id=int(data["role_id"]),
            media_path=media_path
        )

        await message.answer(participation_added_message, reply_markup=main_menu_kb(message.from_user.id))
        await state.clear()

    finally:
        if message.media_group_id:
            processed_media_groups.discard(message.media_group_id)
