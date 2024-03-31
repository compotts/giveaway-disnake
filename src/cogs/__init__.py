from cogs.giveaway_create import Giveaway
from cogs.giveaway_listeners import GiveawayListener
from cogs.giveaway_tasks import GiveawayTask

from loguru import logger

cogs = (Giveaway, GiveawayListener, GiveawayTask)


def setup(bot):
    for cog in cogs:
        bot.add_cog(cog(bot))
        logger.info(f"Cog {cog.__name__} loaded")

