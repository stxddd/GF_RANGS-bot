from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.decorators.admin_required import admin_required
from bot.templates.kb_templates import get_points_text
from bot.db.users.dao import UserDAO
from bot.db.events.dao import UserEventRoleDAO, EventDAO 
from bot.kb.events_kb import get_events_kb, role_kb

router = Router()

class RegistrationFSM(StatesGroup):
    category = State()
    event = State()
    role = State()
    media = State()

    
@router.message(F.text == get_points_text)
@admin_required
async def start_add_role(message: Message):
    user = await UserDAO.find_one_or_none(tg_id = message.from_user.id)
    if not user:
        return await message.answer('Вы не зарегистрированы!')
    events = await EventDAO.find_all(visibility = True)
    await message.answer("Выберите мероприятие:", reply_markup=await get_events_kb(events=events, tg_id = message.from_user.id))
    

@router.callback_query(F.data.startswith("edit_event_page_"))
async def change_events_page(callback: CallbackQuery, state: FSMContext):
    page = int(callback.data.split("_")[-1])
    events = await EventDAO.find_all(visibility = True)
    kb = await get_events_kb(events, callback.from_user.id, page=page)
    await callback.message.edit_reply_markup(reply_markup=kb)

@router.callback_query(F.data.startswith("get_event:"))
async def choose_event(callback: CallbackQuery, state: FSMContext):
    event_id = int(callback.data.split(":")[1])
    await state.update_data(event_id=event_id)
    await state.set_state(RegistrationFSM.role)
    await callback.message.edit_text("Выберите роль:", reply_markup=await role_kb(event_id))

@router.callback_query(F.data.startswith("role:"))
async def choose_role(callback: CallbackQuery, state: FSMContext):
    role_id = callback.data.split(":")[1]
    await state.update_data(role_id=role_id)
    await state.set_state(RegistrationFSM.media)
    await callback.message.edit_text("Отправьте ссылку или медиафайл для регистрации:")

@router.message(RegistrationFSM.media)
async def get_media_or_link(message: Message, state: FSMContext):
    data = await state.get_data()

    if message.text:  
        media_data = message.text
    elif message.photo:
        media_data = message.photo[-1].file_id
    elif message.document:
        media_data = message.document.file_id
    else:
        await message.answer("Пожалуйста, отправьте ссылку или медиафайл.")
        return

    await state.update_data(media=media_data)

    user = await UserDAO.find_one_or_none(tg_id = message.from_user.id)

    new_record = await UserEventRoleDAO.add(
        event_id = int(data['event_id']),
        user_id = user.id,
        role_id = int(data['role_id'])
    )

    await message.answer(
        f"✅ Регистрация завершена!\n\n"
        f"Мероприятие: {data['event_id']}\n"
        f"Роль: {data['role_id']}\n"
        f"Медиа: {media_data}"
    )

    await state.clear()