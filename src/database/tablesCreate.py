import asyncio
from disnake.ext import commands

from database.database import Database


class TablesCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(1)
        await self.db.create_tables()
        print("Tables created")