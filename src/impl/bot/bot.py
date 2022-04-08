from os import getenv
from typing import Any

from aioredis import Redis, from_url
from disnake.ext.commands import Bot as _Bot
from disnake import Intents
from fakeredis.aioredis import FakeRedis
from loguru import logger

from src.impl.database import database

from .status import StatusHeartbeater


class Bot(_Bot):
    def __init__(
        self,
        intents: Intents,
        *args: Any,
        command_prefix: str | list[str] | None = None,
        description: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(
            *args,
            command_prefix=command_prefix,
            description=description,
            intents=intents,
            **kwargs,
        )

        self._status = StatusHeartbeater()

        if not (redis_uri := getenv("REDIS_URI")):
            self.redis = FakeRedis()
        else:
            self.redis: Redis = from_url(redis_uri)

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        logger.info("Connecting to the database...")

        await database.connect()

        logger.info("Connected to the database.")

        self._status.run()

        await super().start(token, reconnect=reconnect)

    async def on_connect(self) -> None:
        logger.info("Connected to the Discord Gateway.")

    async def on_ready(self) -> None:
        logger.info(f"READY event received, connected as {self.user} with {len(self.guilds)} guilds.")

    def load_extension(self, name: str, *, package: str | None = None) -> None:
        super().load_extension(name, package=package)

        logger.info(f"Loaded extension {name}.")
