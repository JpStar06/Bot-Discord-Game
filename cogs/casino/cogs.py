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
        self.get_coins = services.get_coins
        self.add_coins = services.add_coins
        

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