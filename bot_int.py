



# Пример точки входа (нужна будет замена на свой Config)
if __name__ == '__main__':
    class TempConfig:
        BOT_TOKEN = "Токен"  # Нужен реальный токен !!!!!!

    bot = BotCore(TempConfig())
    import asyncio

    asyncio.run(bot.start())