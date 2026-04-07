from database import get_connection

def get_coins(self, user_id: int) -> int:
        pool = get_connection()
        with pool.acquire() as conn:
            row = conn.fetchrow("SELECT coins FROM economy WHERE user_id=$1", user_id)
            if not row:
                conn.execute("INSERT INTO economy (user_id, coins) VALUES ($1, $2)", user_id, 0)
                return 0
            return row["coins"]
        
def add_coins(self, user_id: int, amount: int):
        pool = get_connection()
        with pool.acquire() as conn:
            conn.execute("UPDATE economy SET coins = coins + $1 WHERE user_id=$2", amount, user_id)
