from src.build_bot import build_user_bot


if __name__ == "__main__":
    bot = build_user_bot()
    bot.polling()
