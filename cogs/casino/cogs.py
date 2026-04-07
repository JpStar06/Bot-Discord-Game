import discord
import random
from discord import app_commands
from discord.ext import commands
from database import get_connection
from . import services
from . import embeds


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
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


    casino = app_commands.Group(name="casino", description="Jogos de aposta")

    # -------------------- COINFLIP --------------------
    @casino.command(name="coinflip", description="Cara ou coroa")
    @app_commands.checks.cooldown(1, 2)
    async def coinflip(self, interaction: discord.Interaction, aposta: int, escolha: str):
        print("coinflip chamado")
        escolha = escolha.lower()
        if escolha not in ["cara", "coroa"]:
            await interaction.response.send_message("Escolha `cara` ou `coroa`", ephemeral=True)
            return

        coins = await self.get_coins(interaction.user.id)

        if aposta > coins:
            await interaction.response.send_message(embed=embeds.erro("Você não tem coins suficientes."))
            return

        resultado = random.choice(["cara", "coroa"])

        if escolha == resultado:
            await self.add_coins(interaction.user.id, aposta)
            embedresult = embeds.ganhou("teste 2")
        else:
            await self.add_coins(interaction.user.id, -aposta)
            embedresult = embeds.perdeu("teste 1")

        await interaction.response.send_message(embed=embedresult)

    @coinflip.error
    async def coinflip_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(
                f"⏳ Espere {round(error.retry_after)} segundos para usar novamente.",
                ephemeral=True
            )

# -------------------- SETUP --------------------
async def setup(bot):
    await bot.add_cog(Casino(bot))