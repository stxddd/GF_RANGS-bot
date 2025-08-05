import asyncio
import os
import aiofiles
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from utils.decorators.admin_required import admin_required
from bot.templates.kb_templates import get_points_text
from bot.db.users.dao import UserDAO
from bot.db.events.dao import UserEventRoleDAO, EventDAO
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
    if not user:
        return await message.answer("Вы не зарегистрированы!")
    events = await EventDAO.find_all(visibility=True)
    await message.answer(
        "🔹 Выберите мероприятие",
        reply_markup=await get_events_kb(events=events, tg_id=message.from_user.id)
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
    await state.update_data(event_id=event_id)
    await state.set_state(RegistrationFSM.role)
    await callback.message.edit_text("🔹 Выберите роль", reply_markup=await role_kb(event_id))


@router.callback_query(F.data.startswith("role:"))
async def choose_role(callback: CallbackQuery, state: FSMContext):
    role_id = callback.data.split(":")[1]
    await state.update_data(role_id=role_id)
    await state.set_state(RegistrationFSM.media)
    await callback.message.edit_text(
        "🔹 Пришли своё фото с мероприятия. 1 фото (до 20 МБ)\n\nЕсли ты 'медиа' - отправь ссылку на свою работу!"
    )


@router.message(RegistrationFSM.media)
async def get_media_or_link(message: Message, state: FSMContext):
    data = await state.get_data()
    user = await UserDAO.find_one_or_none(tg_id=message.from_user.id)

    if not user:
        await message.answer("❌ Пользователь не найден.")
        return

    if message.media_group_id and message.media_group_id in processed_media_groups:
        return

    if data.get("registration_in_progress"):
        return

    await state.update_data(registration_in_progress=True)

    try:
        if message.media_group_id:
            processed_media_groups.add(message.media_group_id)

        new_record = await UserEventRoleDAO.add(
            event_id=int(data["event_id"]),
            user_id=user.id,
            role_id=int(data["role_id"]),
            media_path=""
        )

        media_path = ""

        if message.text:
            media_path = message.text
        else:
            file_id = (
                message.photo[-1].file_id if message.photo else
                message.video.file_id if message.video else None
            )

            if not file_id:
                await message.answer("Пожалуйста, отправьте ссылку или медиафайл (фото или видео).")
                await UserEventRoleDAO.delete(new_record.id)
                return

            file = await message.bot.get_file(file_id)

            if file.file_size > settings.MAX_FILE_SIZE:
                await message.answer("❌ Файл слишком большой. Максимальный размер: 20 МБ.")
                await UserEventRoleDAO.delete(new_record.id)
                return

            ext = (
                "jpg" if message.photo else
                "mp4" if message.video else
                (message.document.file_name.split(".")[-1] if message.document else "bin")
            )

            file_path = os.path.join(media_dir, f"{new_record.id}_media.{ext}")
            os.makedirs(media_dir, exist_ok=True)

            file_bytes = await message.bot.download_file(file.file_path)
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(file_bytes.read())

            media_path = file_path

        await UserEventRoleDAO.update(new_record.id, media_path=media_path)
        await message.answer("✅ Регистрация завершена!", reply_markup=main_menu_kb(message.from_user.id))

    finally:
        await state.clear()
        if message.media_group_id:
            processed_media_groups.discard(message.media_group_id)
