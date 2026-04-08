from database import get_connection

async def criarembed(guild_id: int):
    pool = get_connection()

    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO embeds (guild_id, title, description, color, image)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """, guild_id, "Título do Embed", "Descrição padrão", 0x3498db, None)

        return row["id"]