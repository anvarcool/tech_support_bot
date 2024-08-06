import asyncio
from aiogram import Bot, Dispatcher
import dotenv
import os
from handlers import user_handlers
print('imports successful')
async def main() -> None:

    # Инициализируем бот и диспетчер
    dotenv.load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())