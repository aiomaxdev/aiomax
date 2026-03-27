"""
Пример бота с FSM (Finite State Machine).

Демонстрирует использование состояний для многошаговых диалогов.
"""
import asyncio
import os
from dotenv import load_dotenv

from aiomax import Bot
from aiomax.filters import F
from aiomax.fsm import StatesGroup, MemoryStorage, FSMManager

load_dotenv()
token = os.getenv("MaxToken")

bot = Bot(token=token)
fsm_manager = FSMManager(MemoryStorage())


class FormState(StatesGroup):
    """Группа состояний для формы регистрации"""
    waiting_for_name = "waiting_for_name"
    waiting_for_age = "waiting_for_age"
    waiting_for_email = "waiting_for_email"


@bot.on_message(F.command("register"))
async def start_registration(update):
    """Начало регистрации"""
    await fsm_manager.set_state(update, FormState.waiting_for_name)

    if update.message and update.message.recipient.chat_id:
        await bot.send_message(
            chat_id=update.message.recipient.chat_id,
            text="Введите ваше имя:"
        )


@bot.on_message(F.text.contains("@"))
async def handle_email(update):
    """Обработка email (только если не в состоянии регистрации)"""
    state = await fsm_manager.get_state(update)
    if state == FormState.waiting_for_email:
        # Сохраняем email
        data = await fsm_manager.get_data(update)
        data["email"] = update.message.body.text
        await fsm_manager.set_data(update, data)

        # Завершение регистрации
        await fsm_manager.clear(update)

        if update.message and update.message.recipient.chat_id:
            await bot.send_message(
                chat_id=update.message.recipient.chat_id,
                text=f"Регистрация завершена!\nИмя: {data.get('name')}\nВозраст: {data.get('age')}\nEmail: {data['email']}"
            )


@bot.on_message()
async def handle_form_input(update):
    """Обработка ввода данных формы"""
    state = await fsm_manager.get_state(update)

    if not state:
        return  # Не в состоянии формы

    if update.message and update.message.body.text and update.message.recipient.chat_id:
        chat_id = update.message.recipient.chat_id
        text = update.message.body.text

        if state == FormState.waiting_for_name:
            # Сохраняем имя
            await fsm_manager.update_data(update, {"name": text})
            await fsm_manager.set_state(update, FormState.waiting_for_age)
            await bot.send_message(chat_id=chat_id, text="Введите ваш возраст:")

        elif state == FormState.waiting_for_age:
            # Сохраняем возраст
            await fsm_manager.update_data(update, {"age": text})
            await fsm_manager.set_state(update, FormState.waiting_for_email)
            await bot.send_message(chat_id=chat_id, text="Введите ваш email:")


async def main():
    await bot.start()
    print("Запуск FSM бота...")
    await bot.start_polling()
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())