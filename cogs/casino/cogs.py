import discord
import random
from discord import app_commands
from discord.ext import commands
from database import get_connection
from .services import get_coins, add_coins
from .embeds import erro, ganhou, perdeu


class Casino(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_coins = get_coins
        self.add_coins = add_coins

    casino = app_commands.Group(name="casino", description="Jogos de aposta")

    # -------------------- COINFLIP --------------------
    @casino.command(name="coinflip", description="Cara ou coroa")
    @app_commands.checks.cooldown(30, 1200)
    async def coinflip(self, interaction: discord.Interaction, aposta: int, escolha: str):
        escolha = escolha.lower()
        if escolha not in ["cara", "coroa"]:
            await interaction.response.send_message("Escolha `cara` ou `coroa`", ephemeral=True)
            return

        coins = await self.get_coins(interaction.user.id)
        if aposta > coins:
            await interaction.response.send_message(embed=erro("Você não tem coins suficientes."))
            return
        
        resultado = random.choice(["cara", "coroa"])
        if escolha == resultado:
            await self.add_coins(interaction.user.id, aposta)
            embed=ganhou(f"🪙 **{resultado}**\nVocê ganhou `{aposta}` coins!")
        else:
            await self.add_coins(interaction.user.id, -aposta)
            embed=perdeu(f"🪙 **{resultado}**\nVocê perdeu `{aposta}` coins.")

        await interaction.response.send_message(embed=embed)

# -------------------- SETUP --------------------
async def setup(bot):
    await bot.add_cog(Casino(bot))