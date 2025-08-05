from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from bot.db.users.dao import UserDAO

from bot.templates.message_templates import (
    welcome_message,
    registation_message,
    enter_fullname_message,
    enter_course_number_message,
    enter_group_name_message,
    already_register_message,
    success_registration_message,
    register_error
)


from bot.kb.main_menu_kb import main_menu_kb

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
    await message.answer(registation_message)
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
async def process_group_name(message: Message, state: FSMContext):
    data = await state.get_data()
    group_name = message.text 
    tg_id = message.from_user.id
    user = await UserDAO.add( 
        tg_id=tg_id,
        fullname=data["fullname"],
        course_number=data["course_number"],
        group_number=group_name
    )
    
    if not user:
        return await message.answer(register_error)
    await message.answer(success_registration_message, reply_markup=main_menu_kb(tg_id))
    
    await state.clear()
