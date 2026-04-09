import discord
from discord import app_commands
from discord.ext import commands
import random
import datetime
from database import get_connection
from . import services
from . import embeds

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = None

    get_user = services.get_user()
    add_coins = services.add_coins()

    economia = app_commands.Group(name="eco", description="Sistema de economia.")

    @economia.command(name="carteira", description="Mostra sua carteira")
    async def coins(self, interaction: discord.Interaction):
            user = await services.get_user(interaction.user.id)
            await interaction.response.send_message(embed=embeds.carteira(f"coins: **{user['coins']:,}**\nboxes: **{user['boxes']:,}**\ndaily: **{user['daily_streak']:,}**"))


async def setup(bot):
    await bot.add_cog(Economia(bot))
