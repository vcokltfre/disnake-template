from os import environ

from . import Bot


def main() -> None:
    bot = Bot()

    extensions: list[str] = []

    for ext in extensions:
        bot.load_extension(ext)

    bot.run(environ["TOKEN"])


main()
