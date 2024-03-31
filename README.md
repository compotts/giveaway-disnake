# Система для создания и проведения розыгрышей на сервере Discord

Данный дискорд бот написан на [Python](https://www.python.org/) с использованием [Disnake](https://disnake.readthedocs.io/en/latest/) и [Ormar](https://collerek.github.io/ormar/latest/).
# Использование
![visual](./assets/)
# Запуск
- Пукнт **1**: Подготовка
- - Создать `.env` файл и заполнить его содержимым используя шаблон `.env.sample`
- - Обратите внимание на `DATABASE_URL` - это URL для подключения к базе данных, пример:
  - **sqlite** - `DATABASE_URL='sqlite+aiosqlite:///giveaway.db'`
  - **MySQL** - `DATABASE_URL='mysql+aiomysql://lukas:krasava@localhost/giveaway'`
  - **PostgreSQL** - `DATABASE_URL='postgresql+asyncpg://lukas:krasava@localhost/giveaway'`
- Пукнт **2**: Проверка
- - Запустить `main.py`
- - Проверьте, что бот запущен и работает исправно
- - При ошибках проверьте все ли вы записали в конфиге

## Обнаружили проблему?

Если вы обнаружили проблему, пожалуйста, создайте новый Issue, чтобы мы могли исправить ее.
