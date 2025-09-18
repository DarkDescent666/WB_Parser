from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, FSInputFile


async def send(message: Message,path):
    document = FSInputFile(path, filename=path)
    await message.answer_document(document=document, caption="Работает!!")