from os import environ

from disnake import Intents

from . import Bot


def main() -> None:
    intents = Intents.none()

    intents.guilds = True
    intents.messages = True

    bot = Bot(intents=intents)

    extensions: list[str] = []

    for ext in extensions:
        bot.load_extension(ext)

    bot.run(environ["TOKEN"])


main()
