from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from bot.templates.kb_templates import get_conditions_text
from bot.templates.message_templates import condition_message
from bot.kb.main_menu_kb import main_menu_kb

router = Router()


@router.message(F.text == get_conditions_text)
async def start_add_role(message: Message):   
    photo = FSInputFile("bot/handlers/condition.jpg") 
    await message.answer_photo(photo, caption=condition_message, reply_markup=main_menu_kb(message.from_user.id))

    