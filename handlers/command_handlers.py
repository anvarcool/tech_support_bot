from aiogram import Router
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from handlers import user_handlers

router_commands = Router()
router_commands.include_router(user_handlers.router)

button_1 = KeyboardButton(text='Завести заявку')
button_2 = KeyboardButton(text='Узнать статус заявки')
keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]], resize_keyboard=True)

@router_commands.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Здравствуйте! Что вы хотите сделать?',  reply_markup=keyboard)

@router_commands.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Тут будет список команд наверное'
    )

