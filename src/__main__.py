from os import environ

from . import Bot


def main() -> None:
    bot = Bot()

    for ext in []:
        bot.load_extension(ext)

    bot.run(environ["TOKEN"])


main()
