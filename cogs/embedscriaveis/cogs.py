import discord
from discord import app_commands
from discord.ext import commands
import datetime
from database import get_connection
from . import embeds
from . import services

class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = None
    
    async def cog_load(self):
        self.pool = await get_connection()  # Usa o pool asyncpg

    embed = app_commands.Group(name="embeds", description="Comandos de embeds")

    # -------------------- CRIAR EMBED --------------------
    @embed.command(name="criar", description="Cria um embed padrão.")
    @app_commands.checks.has_permissions(administrator=True)
    async def criarembed(self, interaction: discord.Interaction):

        embed_id = await services.criarembed(interaction.guild.id)

        await interaction.response.send_message(f"Embed criado com ID `{embed_id}`", embed=embeds.padrao())

async def setup(bot):
    await bot.add_cog(Comandos(bot))