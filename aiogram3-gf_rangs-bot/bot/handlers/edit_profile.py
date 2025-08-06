from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.templates.kb_templates import edit_profile_text
from bot.db.users.dao import UserDAO
from bot.kb.users_kb import edit_profile_keyboard
from bot.templates.message_templates import (
    you_need_to_register_message,
    edit_profile_message_template,
    ask_fullname_message,
    fullname_updated_message,
    ask_course_message,
    invalid_course_message,
    course_updated_message,
    ask_group_message,
    group_updated_message,
    profile_updated_message,
    no_changes_message,
)

router = Router()


class EditProfile(StatesGroup):
    fullname = State()
    course_number = State()
    group_number = State()


@router.message(F.text == edit_profile_text)
async def start_editing(message: Message):
    user = await UserDAO.find_one_or_none(tg_id=message.from_user.id)
    if not user or not user.is_approved:
        return await message.answer(you_need_to_register_message)

    await message.answer(
        edit_profile_message_template.format(
            fullname=user.fullname,
            course=user.course_number,
            group=user.group_number
        ),
        reply_markup=edit_profile_keyboard()
    )


@router.callback_query(F.data == "edit_fullname")
async def ask_fullname(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(ask_fullname_message)
    await state.set_state(EditProfile.fullname)
    await callback.answer()


@router.message(EditProfile.fullname)
async def set_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer(
        fullname_updated_message,
        reply_markup=edit_profile_keyboard()
    )


@router.callback_query(F.data == "edit_course")
async def ask_course(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(ask_course_message)
    await state.set_state(EditProfile.course_number)
    await callback.answer()


@router.message(EditProfile.course_number)
async def set_course(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer(invalid_course_message)
    await state.update_data(course_number=int(message.text))
    await message.answer(
        course_updated_message,
        reply_markup=edit_profile_keyboard()
    )


@router.callback_query(F.data == "edit_group")
async def ask_group(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(ask_group_message)
    await state.set_state(EditProfile.group_number)
    await callback.answer()


@router.message(EditProfile.group_number)
async def set_group(message: Message, state: FSMContext):
    await state.update_data(group_number=message.text)
    await message.answer(
        group_updated_message,
        reply_markup=edit_profile_keyboard()
    )


@router.callback_query(F.data == "save_changes")
async def save_changes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = await UserDAO.find_one_or_none(tg_id=callback.from_user.id)
    if not user or not user.is_approved:
        return await callback.message.answer(you_need_to_register_message)

    updated_fields = {}
    if "fullname" in data:
        updated_fields["fullname"] = data["fullname"]
    if "course_number" in data:
        updated_fields["course_number"] = data["course_number"]
    if "group_number" in data:
        updated_fields["group_number"] = data["group_number"]

    if updated_fields:
        await UserDAO.update(model_id=user.id, **updated_fields)
        await callback.message.answer(profile_updated_message)
        await state.clear()
    else:
        await callback.message.answer(no_changes_message)

    await callback.answer()
