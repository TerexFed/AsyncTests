import asyncio
import pytest
import aiohttp
import aiosqlite
import sqlite3

async def async_function_to_test1():
    return 42

@pytest.mark.asyncio
async def test_successful_promise_resolution(event_loop):
    result = await async_function_to_test1()
    assert result == 42

async def async_function_to_test2():
    raise ValueError("Expected error")

@pytest.mark.asyncio
async def test_promise_rejection_with_expected_exception(event_loop):
    with pytest.raises(ValueError) as exc_info:
        await async_function_to_test2()
    assert str(exc_info.value) == "Expected error"

async def fetch_data_from_api(breed_name):
    async with aiohttp.ClientSession() as session:
        url = f'https://dog.ceo/api/breed/{breed_name}/images/random'
        async with session.get(url) as response:
            data = await response.json()
            if response.status == 200 and data.get("status") == "success":
                return data.get("message")
            else:
                return None

@pytest.mark.asyncio
async def test_fetch_data_from_api(event_loop):
    breed_name = "african"
    image_url = await fetch_data_from_api(breed_name)
    assert image_url is not None
    assert "https://images.dog.ceo/breeds/african/" in image_url

@pytest.fixture(scope='session')
def database_connection():
    connection = sqlite3.connect('dogs.db')
    yield connection
    connection.close()


# Функция для вставки данных
async def insert_data():
    # Создаем подключение к базе данных
    async with aiosqlite.connect("dogs.db") as db:
        # Выполняем SQL-запрос для вставки данных
        await db.execute(
            """
            INSERT INTO Dogs (Name, Breed) VALUES (?, ?)
            """,
            ("Teo", "Valdayan dalmatan"),
        )
        # Подтверждаем изменения в базе данных
        await db.commit()

async def select_data():
    # Создаем подключение к базе данных
    async with aiosqlite.connect("dogs.db") as db:
        # Выполняем SQL-запрос для выборки данных
        async with db.execute("SELECT * FROM Dogs") as cursor:
            # Итерируемся по результатам запроса
            async for row in cursor:
                # Выводим данные из строки результата
                print(row[0], row[1], row[2])

# Функция для обновления данных
async def update_data():
    # Создаем подключение к базе данных
    async with aiosqlite.connect("dogs.db") as db:
        # Выполняем SQL-запрос для обновления данных
        await db.execute(
            """
            UPDATE Dogs SET Name = ? WHERE Breed = ?
            """,
            ("Charik", "Valdayan dalmatan"),
        )
        # Подтверждаем изменения в базе данных
        await db.commit()

async def add_record_to_database():
    async with aiosqlite.connect('dogs.db') as db:
        await insert_data()
        await update_data()
        await select_data()
        await db.commit()

@pytest.mark.asyncio
async def test_add_record_to_database(database_connection):
    new_record_id = await add_record_to_database()
    assert new_record_id is not 0


async def async_function_to_run_in_thread():
    return 42

async def run_async_function_in_thread():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, async_function_to_run_in_thread)
    return result

@pytest.mark.asyncio
async def test_run_async_function_in_thread(event_loop):
    result = await run_async_function_in_thread()
    assert result == 42
