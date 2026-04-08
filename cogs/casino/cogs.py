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
        
    async def get_coins(self, user_id: int) -> int:
        pool = await get_connection()
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT coins FROM economy WHERE user_id=$1", user_id)
            if not row:
                await conn.execute("INSERT INTO economy (user_id, coins) VALUES ($1, $2)", user_id, 0)
                return 0
            return row["coins"]

    async def add_coins(self, user_id: int, amount: int):
        pool = await get_connection()
        async with pool.acquire() as conn:
            await conn.execute("UPDATE economy SET coins = coins + $1 WHERE user_id=$2", amount, user_id)


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

    #-----------dices-----------------------
    @casino.command(name="dice", description="Jogue dados")
    @app_commands.checks.cooldown(30, 1200)
    async def dice(self, interaction: discord.Interaction, aposta: int):
        coins = await self.get_coins(interaction.user.id)
        if aposta > coins:
            await interaction.response.send_message(embed=embeds.erro("Você não tem coins suficientes."))
            return

        player = random.randint(1, 6)
        bot_roll = random.randint(1, 6)

        if player > bot_roll:
            await self.add_coins(interaction.user.id, aposta)
            embedresult = embeds.ganhou(f"🎲 Você: {player}\n🎲 Bot: {bot_roll}\nVocê ganhou `{aposta}` coins!")
        elif player < bot_roll:
            await self.add_coins(interaction.user.id, -aposta)
            embedresult = embeds.perdeu(f"🎲 Você: {player}\n🎲 Bot: {bot_roll}\nVocê perdeu `{aposta}` coins.")
        else:
            await self.add_coins(interaction.user.id, aposta)
            embedresult = embeds.ganhou(f"🎲 Você: {player}\n🎲 Bot: {bot_roll}\nEmpate!")

        await interaction.response.send_message(embed=embedresult)
# -------------------- SETUP --------------------
async def setup(bot):
    await bot.add_cog(Casino(bot))
