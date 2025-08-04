from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()

DELETE_LAST_MESSAGE_PATTERN = "delete_last_message"


@router.callback_query(F.data == DELETE_LAST_MESSAGE_PATTERN)
async def handle_delete_last_message(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
