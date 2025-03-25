from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📥 Мои источники"), KeyboardButton(text="➕ Добавить источники")],
            [KeyboardButton(text="🗑 Удалить источники")],
            [KeyboardButton(text="🔎 Помощь")]
        ],
        resize_keyboard=True
    )

    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )

    return kb