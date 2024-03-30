import disnake
import asyncio
from disnake.ext import commands
from loguru import logger

from config import TOKEN, TEST_GUILD

from _cogs import setup

import db


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix="!",
            intents=disnake.Intents.all(),
            test_guilds=[int(TEST_GUILD)],
            help_command=None,
            reload=True,
            **kwargs,
        )

    async def on_ready(self):
        await db.database.connect()
        await db.db_setup(db.metadata)

        logger.info("Database connected properly")

        logger.success(f"-> < DISCORD API  CONNECTED > {self.user.name} запущен")

    async def on_resumed(self):
        logger.warning(f"-> < DISCORD API RESUMED > {self.user}")

    async def on_disconnect(self):
        await db.database.disconnect()

        logger.critical(f"-> < DISCORD API DISCONNECTED > {self.user}")


bot = Bot()

setup(bot)


# async def main():
#     await db.db_setup(db.metadata)

if __name__ == "__main__":
    logger.info("Trying to start a bot")

    if TOKEN == "":
        raise ValueError("Check the environment TOKEN variable, it is None")

    # asyncio.run(main())
    bot.run(TOKEN)