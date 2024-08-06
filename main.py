import asyncio
from aiogram import Bot, Dispatcher
import dotenv
import os
from handlers import command_handlers
print('imports successful')
async def main() -> None:

    # bot and dispatcher init
    dotenv.load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(command_handlers.router_commands)

    # skipping old updates and starting polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())