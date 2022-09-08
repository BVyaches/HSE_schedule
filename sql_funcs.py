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
    await cursor.execute('SELECT sheet_name, sheet_url FROM sheets')
    sql_data = {i[0]: i[1] for i in await cursor.fetchall()}
    new_data = await get_data()
    updates = []
    for new_sheet in new_data:
        await cursor.execute(
            f'SELECT * FROM sheets WHERE sheet_name = "{new_sheet}"')

        if not await cursor.fetchone():
            await download_sheet(new_sheet, new_data[new_sheet])

            updates.append(new_sheet)
            await cursor.execute(
                f'INSERT INTO sheets VALUES '
                f'("{new_sheet}", "{new_data[new_sheet]}")')
        else:
            if new_data[new_sheet] != sql_data[new_sheet]:
                await download_sheet(new_sheet, new_data[new_sheet])

                updates.append(new_sheet)
                await cursor.execute(
                    "f'UPDATE sheets SET sheet_url = " )
        await db.commit()

    for old_sheet_name in sql_data:

        if old_sheet_name not in new_data.keys():
            print(old_sheet_name)
            os.remove(f'sheets/{old_sheet_name}.xls')
            await cursor.execute(
                f'DELETE FROM sheets WHERE sheet_name = "{old_sheet_name}"')
            await db.commit()

    await cursor.close()
    await db.close()
    print('Result: ', updates)

    return updates


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(check_sheets())
    loop.close()
