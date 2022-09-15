import asyncio
import os

import aiosqlite

from main import get_data, download_sheet


async def create_table():
    db = await aiosqlite.connect('server.db')
    cursor = await db.cursor()
    await cursor.execute('CREATE TABLE IF NOT EXISTS sheets('
                         'sheet_name TEXT,'
                         'sheet_url TEXT'
                         ')')
    await db.commit()
    await cursor.execute('CREATE TABLE IF NOT EXISTS users('
                         'id INT,'
                         'status INT'
                         ')')
    await cursor.close()
    await db.close()


async def check_sheets():
    db = await aiosqlite.connect('server.db')
    cursor = await db.cursor()
    await cursor.execute('SELECT sheet_name, sheet_url FROM sheets')

    sql_data = {i[0]: i[1] for i in await cursor.fetchall()}
    new_data = await get_data()
    updates = []
    for new_sheet in new_data:
        await cursor.execute(
            f'SELECT * FROM sheets WHERE sheet_name = "{new_sheet}"')

        if not await cursor.fetchone():
            await download_sheet(new_sheet, new_data[new_sheet])
            #await create_picture(new_sheet)
            updates.append(new_sheet)
            await cursor.execute(
                'INSERT INTO sheets VALUES '
                f'("{new_sheet}", "{new_data[new_sheet]}")')

        else:
            if new_data[new_sheet] != sql_data[new_sheet]:
                await download_sheet(new_sheet, new_data[new_sheet])
                #await create_picture(new_sheet)
                updates.append(new_sheet)
                await cursor.execute(
                    f'UPDATE sheets SET sheet_url = "{new_data[new_sheet]}"'
                    f' WHERE sheet_name = "{new_sheet}"')
        await db.commit()

    for old_sheet_name in sql_data:
        if old_sheet_name not in new_data.keys():

            os.remove(f'sheets/{old_sheet_name}.xls')
            #os.remove(f'sheets_pics/{old_sheet_name}.png')
            await cursor.execute(f'DELETE FROM sheets WHERE sheet_name = "{old_sheet_name}"')
            await db.commit()

    await cursor.close()
    await db.close()
    print('Result: ', updates)

    return updates


async def get_all_sheets():
    db = await aiosqlite.connect('server.db')
    cursor = await db.cursor()

    await cursor.execute('SELECT sheet_name FROM sheets')
    all_sheets = [i[0] for i in await cursor.fetchall()]
    await cursor.close()
    await db.close()


    return all_sheets


async def add_user(user_id):
    db = await aiosqlite.connect('server.db')
    cursor = await db.cursor()
    await cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')
    if not await cursor.fetchone():
        await cursor.execute(f'INSERT INTO users VALUES ({user_id}, 1)')
    else:
        await cursor.execute(f'UPDATE users SET status = 1 WHERE id = {user_id}')

    await db.commit()
    await cursor.close()
    await db.close()


async def stop_status(user_id):
    db = await aiosqlite.connect('server.db')
    cursor = await db.cursor()
    await cursor.execute(f'UPDATE users SET status = 0 WHERE id = {user_id}')
    await db.commit()
    await cursor.close()
    await db.close()


async def get_active_users():
    db = await aiosqlite.connect('server.db')
    cursor = await db.cursor()
    await cursor.execute('SELECT id FROM users WHERE status = 1')
    active_users = [i[0] for i in await cursor.fetchall()]
    await db.commit()
    await cursor.close()
    await db.close()
    return active_users



if __name__ == '__main__':
    asyncio.run(get_all_sheets())
