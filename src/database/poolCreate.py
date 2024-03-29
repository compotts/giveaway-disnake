from disnake.ext import commands

from database.connection import db_pool


class PoolCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if await db_pool.is_closed():
            await db_pool.create_pool()

    @commands.Cog.listener()
    async def on_disconnect(self):
        ...
        # if not await db_pool.is_closed():
        #     await db_pool.close_pool()
        #     print("Pool closed")

    @commands.Cog.listener()
    async def on_resumed(self):
        if await db_pool.is_closed():
            await db_pool.create_pool()
