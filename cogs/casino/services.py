from database import get_connection

async def get_coins(user_id: int) -> int:
    pool = get_connection()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT coins FROM economy WHERE user_id=$1", user_id
        )

        if not row:
            await conn.execute(
                "INSERT INTO economy (user_id, coins) VALUES ($1, $2)",
                user_id, 0
            )
            return 0

        return row["coins"]


async def add_coins(user_id: int, amount: int):
    pool = get_connection()

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO economy (user_id, coins)
            VALUES ($1, $2)
            ON CONFLICT (user_id)
            DO UPDATE SET coins = economy.coins + $2
            """,
            user_id, amount
        )

