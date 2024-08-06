from aiogram.filters import Command
from aiogram.types import ContentType, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import F
from utils.database_utils import Data
from aiogram import Router
import os
import dotenv
dotenv.load_dotenv()
database = os.getenv('database')
user_db = os.getenv('user')
host = os.getenv('host')
port = os.getenv('port')
password = os.getenv('password')
table_name=os.getenv('table_name')
router = Router()
button_1 = KeyboardButton(text='Завести заявку')
button_2 = KeyboardButton(text='Узнать статус заявки')
ven_db = Data(database = database, user = user_db, host = host, port = port, password = password) 

users = {}

keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]], resize_keyboard=True)

contact_btn_auto = KeyboardButton(
    text='Да',
    request_contact=True
)
contact_btn_hand = KeyboardButton(text = 'Ввести вручную')
contact_kboard = ReplyKeyboardMarkup(keyboard=[[contact_btn_auto, contact_btn_hand]], resize_keyboard=True)


@router.message(F.text and F.text.lower() == 'завести заявку')
async def make_request(message: Message):
    users[message.from_user.id] = ['waiting_inn', {}]
    await message.answer('Введите ИНН юрлица', reply_markup=ReplyKeyboardRemove())


@router.message(F.text and F.text.lower() == 'узнать статус заявки')
async def know_status(message: Message):
    status = ven_db.get_status(table_name, message.from_user.id)
    await message.answer(f'{status}', reply_markup=ReplyKeyboardRemove())


@router.message(lambda x: x.text and x.text.isdigit() and users[x.from_user.id][0] == 'waiting_inn')
async def get_inn(message: Message):
    if len(message.text) == 9:
        users[message.from_user.id][1]['INN'] = message.text 
        await message.answer('Отправить номер телефона, привязанный к аккаунту?', reply_markup=contact_kboard)
        users[message.from_user.id][0] = 'waiting_phone'
    else:
        await message.answer('Неверный формат ИНН, попробуйте еще раз')


@router.message(lambda x: x.text and x.text.lower() == 'ввести вручную')
async def hand_phone(message: Message):
    await message.answer('Напишите номер телефона', reply_markup=ReplyKeyboardRemove())


@router.message(lambda x: users[x.from_user.id][0] == 'waiting_phone')
async def get_phone(message: Message):
    if message.content_type == ContentType.CONTACT:
        users[message.from_user.id][1]['phone_number'] = message.contact.phone_number
        await message.answer('Опишите предмет заявки', reply_markup=ReplyKeyboardRemove())
        users[message.from_user.id][0] = 'comment'
    else:
        msg = message.text
        if (((len(msg) == 13) and msg.startswith('+998') and msg[1:].isdigit()) or 
            (((len(msg) == 9) or ((len(msg) == 12) and msg.startswith('998'))) and msg.isdigit())):
            users[message.from_user.id][1]['phone_number'] = msg
            await message.answer('Опишите предмет заявки', reply_markup=ReplyKeyboardRemove())
            users[message.from_user.id][0] = 'comment'
        else:
            await message.answer('Неверный формат номера телефона, попробуйте еще раз')


@router.message(lambda x: users[x.from_user.id][0] == 'comment')
async def get_comment(message:Message):
    users[message.from_user.id][1]['firstname'] = message.from_user.first_name
    users[message.from_user.id][1]['lastname'] = message.from_user.last_name
    users[message.from_user.id][1]['username'] = message.from_user.username
    users[message.from_user.id][1]['request_number'] = str(message.from_user.id) + '_' + str(ven_db.get_last_req_number(table_name, message.from_user.id) + 1)
    users[message.from_user.id][1]['req_text'] = message.text
    users[message.from_user.id][1]['user_id'] = message.from_user.id
    ven_db.post_data(users[message.from_user.id], table_name)
    await message.answer(f'Номер вашей заявки: {users[message.from_user.id][1]["request_number"]}', reply_markup=ReplyKeyboardRemove())
    del users[message.from_user.id]


@router.message()
async def process_other_answers(message: Message):
    await message.answer('Чтобы начать, напишите /start')