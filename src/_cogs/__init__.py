from _cogs.test import Giveaway
from _cogs.testTwo import GiveawayTwo

from loguru import logger

cogs = (
    Giveaway, 
    GiveawayTwo
)


def setup(bot):
    for cog in cogs:
        bot.add_cog(cog(bot))
        logger.info(f"Cog {cog.__name__} loaded")

