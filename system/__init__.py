from system.giveaway_create import Giveaway
from database.poolCreate import PoolCreate
from system.giveaway_listeners import GiveawayListeners
from database.tablesCreate import TablesCreate


cogs = (
    Giveaway,
    PoolCreate,
    TablesCreate,
    GiveawayListeners
)

def setup(bot):
    for cog in cogs:
        bot.add_cog(cog(bot)) 
        for command in cog.get_application_commands(self=cog):
            print(f"загружена команда /{command.name}")