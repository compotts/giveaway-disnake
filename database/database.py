from database.connection import db_pool


class Database:
    def __init__(self):
        pass

    async def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS `giveaways` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `message_id` BIGINT(50) NOT NULL,
            `guild_id` BIGINT(50) NOT NULL,
            `channel_id` BIGINT(50) NOT NULL,
            `host_id` BIGINT(50) NOT NULL,
            `prize` VARCHAR(255) NOT NULL,
            `winers` VARCHAR(255) NOT NULL,
            `start_time` DATETIME NOT NULL,
            `end_time` DATETIME NOT NULL,
            `voice` VARCHAR(255) NOT NULL DEFAULT 'No'
        );
        CREATE TABLE IF NOT EXISTS `giveaway_entries` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `message_id` BIGINT(50) NOT NULL,
            `user_id` BIGINT(50) NOT NULL,
            `date` DATETIME NOT NULL
        );
        """
        await db_pool.execute_query(query)
    
    async def add_giveaway(self, message_id, guild_id, channel_id, host_id, prize, winers, start_time, end_time, voice):
        query = """
        INSERT INTO `giveaways` (message_id, guild_id, channel_id, host_id, prize, winers, start_time, end_time, voice)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        await db_pool.execute_query(query, (message_id, guild_id, channel_id, host_id, prize, winers, start_time, end_time, voice))

    async def get_giveaway(self, message_id):
        query = """
        SELECT * FROM `giveaways` WHERE message_id = %s;
        """
        return await db_pool.execute_query(query, (message_id,))
    
    async def get_all_giveaways(self):
        query = """
        SELECT * FROM `giveaways`;
        """
        return await db_pool.execute_query(query)

    async def delete_giveaway(self, message_id):
        query = """
        DELETE FROM `giveaways` WHERE message_id = %s;
        """
        await db_pool.execute_query(query, (message_id,))

    async def add_giveaway_entry(self, message_id, user_id, date):
        query = """
        INSERT INTO `giveaway_entries` (message_id, user_id, date)
        VALUES (%s, %s, %s);
        """
        await db_pool.execute_query(query, (message_id, user_id, date))

    async def get_all_giveaway_entries(self):
        query = """
        SELECT * FROM `giveaway_entries`;
        """
        return await db_pool.execute_query(query)

    async def get_giveaway_entries(self, message_id):
        query = """
        SELECT * FROM `giveaway_entries` WHERE message_id = %s;
        """
        return await db_pool.execute_query(query, (message_id,))
    
    async def delete_giveaway_entries(self, message_id):
        query = """
        DELETE FROM `giveaway_entries` WHERE message_id = %s;
        """
        await db_pool.execute_query(query, (message_id,))
    
    async def delete_user_giveaway_entries(self, message_id, user_id):
        query = """
        DELETE FROM `giveaway_entries` WHERE message_id = %s AND user_id = %s;
        """
        await db_pool.execute_query(query, (message_id, user_id))

####
        
    async def get_user_giveaway_entry(self, message_id, user_id):
        query = """
        SELECT * FROM `giveaway_entries` WHERE message_id = %s AND user_id = %s;
        """
        return await db_pool.execute_query(query, (message_id, user_id))
    
    async def get_user_giveaway_entries(self, user_id):
        query = """
        SELECT * FROM `giveaway_entries` WHERE user_id = %s;
        """
        return await db_pool.execute_query(query, (user_id,))