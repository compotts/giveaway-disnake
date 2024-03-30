import disnake
from disnake.ext import commands
from loguru import logger

from config import TOKEN, TEST_GUILD


from db import db_setup, metadata, database


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
        await database.connect()

        db_setup(metadata)

        logger.info("Database connected properly")

        logger.success(f"-> < DISCORD API  CONNECTED > {self.user.name} запущен")

    async def on_resumed(self):
        logger.warning(f"-> < DISCORD API RESUMED > {self.user}")

    async def on_disconnect(self):
        await database.disconnect()

        logger.critical(f"-> < DISCORD API DISCONNECTED > {self.user}")


bot = Bot()


if __name__ == "__main__":
    logger.info("Trying to start a bot")

    if TOKEN == "":
        raise ValueError("Check the environment TOKEN variable, it is None")

    bot.run(TOKEN)

