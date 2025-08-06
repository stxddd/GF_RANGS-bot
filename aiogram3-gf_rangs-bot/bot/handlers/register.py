from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.db.users.dao import UserDAO
from bot.templates.message_templates import (
    welcome_message,
    registration_message,
    enter_fullname_message,
    enter_course_number_message,
    enter_group_name_message,
    register_error,
    too_many_attempts_message,
    success_registration_message,
    accec_deny_message,
    wait_message
)
from bot.kb.main_menu_kb import main_menu_kb
from datetime import date
from config import settings
from utils.check_admin_tg_id import check_admin_tg_id

router = Router()


class RegisterState(StatesGroup):
    fullname = State()
    course_number = State()
    group_name = State()


@router.message(F.text.lower() == "/start")
async def cmd_start(message: Message, state: FSMContext):
    user = await UserDAO.find_one_or_none(tg_id=message.from_user.id)
    
    if user:
        return await message.answer(welcome_message, reply_markup= main_menu_kb(user.tg_id), parse_mode='Markdown')
    
    await message.answer(welcome_message)
    await message.answer(registration_message)
    await message.answer(enter_fullname_message)
    await state.set_state(RegisterState.fullname)


@router.message(RegisterState.fullname)
async def process_fullname(message: Message, state: FSMContext):
    fullname = message.text.lower()
    await state.update_data(fullname=fullname)
    await message.answer(enter_course_number_message)
    await state.set_state(RegisterState.course_number)


@router.message(RegisterState.course_number)
async def process_course_number(message: Message, state: FSMContext):
    course_number = message.text
    if not course_number.isdigit():
        return await message.answer(enter_course_number_message)
    await state.update_data(course_number=int(course_number))
    await message.answer(enter_group_name_message)
    await state.set_state(RegisterState.group_name)


@router.message(RegisterState.group_name)
async def process_group_name(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    group_name = message.text
    tg_id = message.from_user.id
    today = date.today()

    existing_user = await UserDAO.find_one_or_none(tg_id=tg_id)
    if existing_user:
        if existing_user.last_attempt_date == today and existing_user.attempt_count >= 2:
            await message.answer(too_many_attempts_message)
            await state.clear()
            return
        attempt_count = existing_user.attempt_count + 1 if existing_user.last_attempt_date == today else 1
        await UserDAO.update(
            model_id=existing_user.id,
            attempt_count=attempt_count,
            last_attempt_date=today
        )
        await UserDAO.delete(tg_id=tg_id)

    user = await UserDAO.add(
        tg_id=tg_id,
        fullname=data["fullname"],
        course_number=data["course_number"],
        group_number=group_name,
        is_approved=False,  
        attempt_count=1 if not existing_user else attempt_count,
        last_attempt_date=today
    )
    
    if not user:
        await message.answer(register_error)
        await state.clear()
        return

    admin_message = (
        f"Новый пользователь:\n"
        f"ФИО: {data['fullname']}\n"
        f"КУРС: {data['course_number']}\n"
        f"ГРУППА: {group_name}\n"
        f"ID: {tg_id}"
    )
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Принять", callback_data=f"accept_{user['id']}"),
            InlineKeyboardButton(text="Отклонить", callback_data=f"reject_{tg_id}")
        ]
    ])
    try:
        await bot.send_message(
            chat_id=str(settings.ADMIN_TG_IDS).split(',')[-1],
            text=admin_message,
            reply_markup=inline_kb
        )
    except Exception as e:
        await state.clear()
        return
    
    await message.answer(wait_message)
    await state.clear()

@router.callback_query(F.data.startswith("accept_"))
async def process_accept(callback: CallbackQuery, bot: Bot):
    if not check_admin_tg_id(callback.from_user.id):
        return
    
    user_id = int(callback.data.split("_")[1])
    user = await UserDAO.update(model_id=user_id, is_approved=True)
    
    if user:
        await callback.message.edit_text(
            text=callback.message.text + "\n\n✅ Вход разрешен!",
        )
        try:
            await bot.send_message(
                chat_id=user.tg_id,
                text=success_registration_message,
                reply_markup=main_menu_kb(user.tg_id)
            )
        except Exception as e:
            print(f"Failed to notify user {user.tg_id}: {e}")
    else:
        await callback.message.edit_text(
            text=callback.message.text + "\n\n❌ Пользователя нет!",
            reply_markup=None
        )
    
    await callback.answer()

@router.callback_query(F.data.startswith("reject_"))
async def process_reject(callback: CallbackQuery, bot: Bot):
    if not check_admin_tg_id(callback.from_user.id):
        return
    
    tg_id = int(callback.data.split("_")[1])
    user = await UserDAO.delete(tg_id=tg_id)
    
    if user:
        await callback.message.edit_text(
            text=callback.message.text + "\n\n❌ Отказано",
            reply_markup=None
        )
        try:
            await bot.send_message(
                chat_id=tg_id,
                text=accec_deny_message
            )
        except Exception as e:
            print(f"Failed to notify user {tg_id}: {e}")
    else:
        await callback.message.edit_text(
            text=callback.message.text + "\n\n❌ Пользователя нет",
            reply_markup=None
        )
    
    await callback.answer()