from textwrap import dedent

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.fsm import SourcesFSM
from src.bot.keyboards.common_keyboards import get_main_kb, get_cancel_kb
from src.utils.validators import UrlValidator
from src.database.requests import set_sources, select_user_sources

router = Router(name=__name__)

@router.message(F.text == "📥 Мои источники")
async def show_sources(message: types.Message):
    sources = await select_user_sources(message.chat.id)

    if not sources:
        return await message.answer("У вас пока нет добавленных источников 📭")

    response = [f"Ваши источники: ({len(sources)})", *[f"🔗 {source.url}" for source in sources]]


    return await message.answer(
        text="\n".join(response),
        reply_markup=get_main_kb(),
        disable_web_page_preview=True,
    )

@router.message(F.text == "➕ Добавить источники")
@router.message(Command("add"))
async def cmd_add(message: types.Message, state: FSMContext):
    await state.set_state(SourcesFSM.WAITING_FOR_URL)

    add_text = dedent("""
    📥 Отправьте ссылки на источники через запятую. Например:
    t.me/канал1, https://t.me/канал2, @канал3 ...
    """).strip()

    return await message.answer(
        text=add_text,
        reply_markup=get_cancel_kb(),
        disable_web_page_preview=True
    )

@router.message(F.text == "🗑 Удалить источники")
async def delete_sources(message: types.Message, state: FSMContext):
    ...

@router.message(F.text == "❌ Отмена")
@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return None

    await state.clear()

    return await message.answer(
        text="Операция отменена",
        reply_markup=get_main_kb()
    )

@router.message(SourcesFSM.WAITING_FOR_URL)
async def on_source_add(message: types.Message, state: FSMContext):
    raw_urls = [url.strip() for url in message.text.split(",")]

    valid_urls = set()
    # unknown_urls = []
    invalid_urls = []
    existing_urls = [source.url for source in await select_user_sources(message.from_user.id)]
    not_added_urls = set()

    for url in raw_urls:
        is_valid, normalized = UrlValidator.validate_telegram_channel(url)
        if is_valid and normalized not in existing_urls:
            valid_urls.add(normalized)
        elif is_valid:
            not_added_urls.add(normalized)
        else:
            invalid_urls.append(url)

    if valid_urls:
        await set_sources(message.from_user.id, valid_urls)


    response = []
    if valid_urls:
        response.append("✅ Успешно добавлено:\n" + "\n".join(valid_urls))
    elif not not_added_urls:
        response.append("⚠️ Нет валидных ссылок")

    if valid_urls and invalid_urls:
        response.append("❌ Неккоректные ссылки:\n" + "\n".join(invalid_urls))

    if not_added_urls:
        response.append("📝 Уже сохранены:\n" + "\n".join(not_added_urls))

    await message.answer(
        text="\n\n".join(response),
        reply_markup=get_main_kb(),
        disable_web_page_preview=True
    )

    await state.clear()