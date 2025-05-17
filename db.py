import aiosqlite as sql

async def create_table():
    async with sql.connect("db.db") as con:
        await con.execute("""CREATE TABLE IF NOT EXISTS "users" (
	"id"	TEXT,
	"type"	TEXT,
	"genre"	TEXT,
	"year"	TEXT,
	"country"	TEXT,
	"length"	TEXT
);""")
        await con.commit()

async def add_user(id):
    async with sql.connect("db.db") as con:
        await con.execute(f"""INSERT INTO users (
                          id,
                          type,
                          genre,
                          year,
                          country,
                          length
                      )
                      VALUES (
                          '{id}',
                          '',
                          '',
                          '',
                          '',
                          ''
                      );
    """)
        await con.commit()

async def clear_settings(id, pt):
    async with sql.connect("db.db") as con:
        r = f"UPDATE users SET id = '{id}', {pt} = ''"
        r += f"WHERE id = {id}"
        await con.execute(r)
        await con.commit()

async def set_settings(id, type="", genre="", year="", country="", length=""):
    async with sql.connect("db.db") as con:
        r = f"UPDATE users SET id = '{id}'"
        if type:
            r += f", type = '{type}'"
        if genre:
            r += f", genre = '{genre}'"
        if year:
            r += f", year = '{year}'"
        if country:
            r += f", country = '{country}'"
        if length:
            r += f", length = '{length}'"
        r += f"WHERE id = {id}"
        await con.execute(r)
        await con.commit()

async def get_settings(id):
    async with sql.connect("db.db") as con:
        async with con.execute(f"""SELECT type,
       genre,
       year,
       country,
       length
  FROM users WHERE id = '{id}'""") as cursor:
            settings = await cursor.fetchall()
            if not settings:
                await add_user(id)
                return await get_settings(id)
            else:
                return settings