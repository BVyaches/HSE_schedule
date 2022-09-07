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
    await cursor.close()
    await db.close()


async def check_sheets():
    db = await aiosqlite.connect('server.db')
    cursor = await db.cursor()
    sql_data = await cursor.execute('SELECT * FROM sheets')
    new_data = await get_data()

    updates = []
    for new_sheet in new_data:
        await cursor.execute(
            f'SELECT * FROM sheets WHERE sheet_name = "{new_sheet}"')
        if not await cursor.fetchall():
            await download_sheet(new_sheet, new_data[new_sheet])
            updates.append(new_sheet)
            await cursor.execute(
                f'INSERT INTO sheets VALUES '
                f'("{new_sheet}", "{new_data[new_sheet]}")')
        await db.commit()

    async for sheet in sql_data:
        old_sheet_name, old_sheet_link = sheet
        if old_sheet_name not in new_data:
            os.remove(f'sheets/{old_sheet_name}.xls')
            await cursor.execute(
                f'DELETE FROM sheets WHERE sheet_name = "{old_sheet_name}"')
            await db.commit()
        else:
            await download_sheet(old_sheet_name, new_data[old_sheet_name])
            updates.append(old_sheet_name)
            await cursor.execute(
                f'UPDATE sheets SET sheet_url = "{new_data[old_sheet_name]}"'
                f' WHERE sheet_name = "{old_sheet_name}"')

    await cursor.close()
    await db.close()
    return updates

asyncio.run(create_table())

asyncio.run(check_sheets())
