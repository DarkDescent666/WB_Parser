import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.config import bot


dp = Dispatcher()
# sbsfbsf bdb fgdbdfb
#vfvfffff
from user.handlers.start import rt as rt_start
from user.handlers.request_from_user import rt as rt_request_from_user
from user.handlers.seller import rt as rt_sales


def initial_routers(dispatcher: Dispatcher):
    dispatcher.include_routers(rt_start,
                               rt_request_from_user,
                               rt_sales)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    initial_routers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")