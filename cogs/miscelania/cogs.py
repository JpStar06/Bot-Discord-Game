import discord
import random
from discord import app_commands
from discord.ext import commands
from database import get_connection
from . import services
from . import embeds

class Mis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="8ball", description="Faça uma pergunta para a bola mágica")
    async def eightball(self, interaction: discord.Interaction, pergunta: str):
        escolha = await services.ball(interaction.user.id)
        await interaction.response.send_message(embed=embeds.ball(f"Pergunta: {pergunta}\nResposta: {escolha['resposta']}"))

async def setup(bot):
    await bot.add_cog(Mis(bot))