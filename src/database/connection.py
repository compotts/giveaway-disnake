import aiomysql
from loguru import logger as log

from tools.converters import Url
from configs.config import Config
from schemas.database.database_models import ConvertedUrl


class DatabasePool:
    """
    Класс, представляющий пул базы данных.

    Атрибуты:
    - converted_url (ConvertedUrl): объект, содержащий преобразованный URL базы данных
    - pool (aiomysql.Pool): пул подключений к базе данных

    Методы:
    - create_pool: создает пул подключений к базе данных
    - close_pool: закрывает пул подключений к базе данных
    - is_closed: проверяет, закрыт ли пул подключений к базе данных
    - execute_query: выполняет SQL-запрос и возвращает результат в виде списка кортежей
    - execute_query_fetchRow: выполняет SQL-запрос и возвращает результат в виде одного кортежа
    """
    def __init__(self, converted_url: ConvertedUrl):
        self.converted_url = converted_url
        self.pool = None

    async def create_pool(self):
        """
        Создает пул подключений к базе данных.

        Если пул уже существует, выводится предупреждение.
        Если пул успешно создан, выводится сообщение об успехе.
        """
        if self.pool is not None:
            log.warning("Пул уже существует")
            return
        self.pool = await aiomysql.create_pool(
            host=self.converted_url.hostname,
            port=self.converted_url.port,
            user=self.converted_url.user,
            password=self.converted_url.password,
            db=self.converted_url.db
        )
        if self.pool is None:
            log.critical("Ошибка создания пула")
        else:
            log.success(f"Успешно, пул создан: {self.pool}")

    async def close_pool(self):
        """
        Закрывает пул подключений к базе данных.

        Если пул не существует, выводится предупреждение.
        Если пул успешно закрыт, выводится сообщение об успехе.
        """
        if self.pool is None:
            log.critical("Пул не существует")
            return
        log.warning(f"Закрытие пула: {self.pool}")
        self.pool.close()
        await self.pool.wait_closed()
        log.success("Успешно, пул закрыт")

    async def is_closed(self):
        """
        Проверяет, закрыт ли пул подключений к базе данных.

        Возвращает True, если пул закрыт, и False в противном случае.
        """
        log.warning("Проверка закрыт ли пул...")
        return self.pool is None
    
    async def execute_query(self, query, params=None):
        """
        Выполняет SQL-запрос и возвращает результат в виде списка кортежей.

        Если пул не существует, выводится предупреждение.
        Если произошла ошибка выполнения запроса, выводится сообщение об ошибке.
        """
        if self.pool is None:
            log.critical("Пул не существует")
            return
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)
                    await conn.commit()
                    return await cur.fetchall()
        except Exception as e:
            log.error(f"Ошибка выполнения запроса {query}: {e}")
            return None
        
    async def execute_query_fetchRow(self, query, params=None):
        """
        Выполняет SQL-запрос и возвращает результат в виде одного кортежа.

        Если пул не существует, выводится предупреждение.
        Если произошла ошибка выполнения запроса, выводится сообщение об ошибке.
        """
        if self.pool is None:
            log.critical("Пул не существует")
            return
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, params)
                    await conn.commit()
                    return (await cur.fetchone())
        except Exception as e:
            log.error(f"Ошибка выполнения запроса {query}: {e}")
            return None

db_pool = DatabasePool(Url.convert(str(Config.get_bot().database_url)))