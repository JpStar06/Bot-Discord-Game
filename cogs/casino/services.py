from database import get_connection
import random

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

def spin_slots(aposta: int):
    EMOJIS = ["🍒", "🍋", "🍉", "⭐", "💎", "💶", "🪙"]
    r1 = random.choice(EMOJIS)
    r2 = random.choice(EMOJIS)
    r3 = random.choice(EMOJIS)

    if r1 == r2 == r3:
        return (r1, r2, r3), aposta * 6, "jackpot"
    elif r1 == r2 or r2 == r3 or r1 == r3:
        return (r1, r2, r3), aposta * 3, "win"
    else:
        return (r1, r2, r3), -aposta, "lose"