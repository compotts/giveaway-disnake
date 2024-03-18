import disnake

from loguru import logger
from disnake.ext import commands

from cogs import setup
from configs.config import Config


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix="!",
                         intents=disnake.Intents.all(),
                         test_guilds=[Config.get_bot().test_guild],
                         help_command=None,
                         reload=True,
                         **kwargs)

    async def on_ready(self):
        logger.success(f"-> < DISCORD API  CONNECTED > {self.user.name} запущен")

    async def on_resumed(self):
        logger.warning(f"-> < DISCORD API RESUMED > {self.user}")

    async def on_disconnect(self):
        logger.critical(f"-> < DISCORD API DISCONNECTED > {self.user}")


bot = Bot()

setup(bot)

if __name__ == "__main__":
    print("Starting bot...")
    bot.run(Config.get_bot().token)
