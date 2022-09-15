"""import asyncpg
import asyncio


async def create_table():
    cursor = await asyncpg.connect(host='localhost', user='postgres', password='Slavatop')
    #cursor = await db.cursor()
    await cursor.execute('CREATE TABLE IF NOT EXISTS sheets('
                         'sheet_name TEXT,'
                         'sheet_url TEXT'
                         ')')
    #await cursor.commit()
    await cursor.execute('CREATE TABLE IF NOT EXISTS users('
                         'id INT,'
                         'status INT'
                         ')')
    await cursor.execute(
        'INSERT INTO sheets VALUES '
        f'("1", "2")')
    await cursor.close()
    #await db.close()
    print(111)


asyncio.get_event_loop().run_until_complete(create_table())"""
