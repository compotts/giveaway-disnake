import disnake
from disnake.ext import commands
from loguru import logger

from cogs import setup
from config import TOKEN, TEST_GUILD


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
        logger.success(
            f"-> < DISCORD API  CONNECTED > {self.user.name} запущен")

    async def on_resumed(self):
        logger.warning(f"-> < DISCORD API RESUMED > {self.user}")

    async def on_disconnect(self):
        logger.critical(f"-> < DISCORD API DISCONNECTED > {self.user}")


bot = Bot()

setup(bot)

if __name__ == "__main__":
    logger.info("Trying to start a bot")

    if TOKEN == "":
        raise ValueError("Check the environment TOKEN variable, it is None")

    bot.run(TOKEN)
