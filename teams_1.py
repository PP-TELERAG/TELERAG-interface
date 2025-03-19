from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = ''

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = """
    Руководство пользования для бота:
    - /help - Получить руководство пользования.
    - /info - Получить информацию о проекте и обратную связь.
    - /license - Показать лицензию проекта.
    """
    await update.message.reply_text(help_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    info_text = """
    Информация о проекте:
    """
    await update.message.reply_text(info_text)


async def license_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    license_text = """
    Лицензия проекта:
    """
    await update.message.reply_text(license_text)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("license", license_command))

    application.run_polling()

if __name__ == '__main__':
    main()