from src.build_bot import build_trainer_bot


if __name__ == "__main__":
    bot = build_trainer_bot()
    bot.polling()
