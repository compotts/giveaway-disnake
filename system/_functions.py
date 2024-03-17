import random

from database.database import Database


async def choose_winners(self, giveaway_id):
    db = Database()
    entries = await self.db.get_giveaway_entries(giveaway_id)
    giveaway = await self.db.get_giveaway(giveaway_id)
    winners_count = giveaway[4]
    winners = random.sample(entries, min(winners_count, len(entries)))
    return winners
