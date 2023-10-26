from src.build_bot import build_bot


if __name__ == "__main__":
    bot = build_bot()
    bot.polling()
