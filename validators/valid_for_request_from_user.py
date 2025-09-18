from aiogram.filters import state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def valid_min_price(message,state):
    try:
        if int(message.text) >= 0:
            await state.update_data(min_price=int(message.text))
            return True
        else:
            await message.answer("Значение долно быть больше или равно нулю")
            return False
    except:
        await message.answer('Цена должна быть числом,введите значение снова')
        return False



async def valid_max_price(message,state):
        data = await state.get_data()
        try:
            if int(message.text) > 0:
                if data['min_price'] >= int(message.text):
                    await message.answer('Значение максимальной цены должно быть больше минимальной')
                    await message.delete()
                    return False

                else:
                    await state.update_data(max_price = int(message.text))
                    return True
            else:
                await message.answer('Введенное значение должно быть больше нуля')
                return False
        except:
            await message.answer('Значение должно быть числом, попробуйте снова')
            return False


async def valid_count_page(message,state):
    try:
        await state.update_data(count_page=int(message.text))
        if int(message.text) <= 0:
            await message.answer('Значение должно быть больше нуля')
            return False
        else:
            return True
    except:
        await message.answer('Количество страниц должно быть числом,введите значение снова')
        return False