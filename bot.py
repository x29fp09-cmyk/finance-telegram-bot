from aiogram import Bot, Dispatcher, executor, types
from database import *
import re

TOKEN = "8335084252:AAEA7PbbZvaCSI06ozG0gOPFlZir-ClqT0I"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

CATEGORIES = {
    "еда": "необходимая",
    "аптека": "необходимая",
    "транспорт": "необходимая",
    "учеба": "необходимая",
    "игры": "необязательная",
    "развлечения": "необязательная",
    "кафе": "необязательная"
}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋\n"
        "Введи расход: `еда 500`\n"
        "Или пополнение: `пополнение 10000`\n"
        "Посмотреть статистику: /stats",
        parse_mode="Markdown"
    )

@dp.message_handler(commands=["stats"])
async def stats(message: types.Message):
    incomes, expenses, balance = get_totals()

    if incomes > 0:
        percent = int((expenses / incomes) * 100)
    else:
        percent = 0

    advice = "Финансовая ситуация стабильная ✅"

    if percent > 80:
        advice = "⚠️ Вы тратите почти все доходы. Стоит сократить расходы."
    elif percent > 50:
        advice = "Расходы выше среднего, будьте внимательнее."

    await message.answer(
        f"📊 Статистика:\n\n"
        f"💰 Доходы: {incomes} ₽\n"
        f"💸 Расходы: {expenses} ₽\n"
        f"⚖️ Баланс: {balance} ₽\n\n"
        f"Расходы составляют {percent}% от доходов.\n"
        f"{advice}"
    )

@dp.message_handler()
async def handle_message(message: types.Message):
    text = message.text.lower()

    numbers = re.findall(r"\d+", text)
    if not numbers:
        await message.answer("❌ Не нашёл сумму. Пример: `еда 500`")
        return

    amount = int(numbers[0])

    if "пополнение" in text or "income" in text:
        add_income(amount)
        await message.answer(f"💰 Пополнение на {amount} ₽ добавлено.")
        return

    words = text.split()
    category = words[0]

    if category not in CATEGORIES:
        category = "другое"

    add_expense(amount, category)

    await message.answer(
        f"💸 Трата {amount} ₽ добавлена.\n"
        f"Категория: {category}"
    )

if __name__ == "__main__":
    init_db()
    executor.start_polling(dp)