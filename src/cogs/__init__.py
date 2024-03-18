from cogs.listeners.giveaway_listeners import GiveawayListeners
from cogs.giveaway_tasks import GiveawayTasks
from cogs.giveaway_create import Giveaway
from database import TablesCreate
from database import PoolCreate

cogs = (
    Giveaway,
    PoolCreate,
    TablesCreate,
    GiveawayTasks,
    GiveawayListeners
)

def setup(bot):
    for cog in cogs:
        bot.add_cog(cog(bot))
    print("Cogs loaded")