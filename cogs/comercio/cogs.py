import discord
from discord import app_commands
from discord.ext import commands
from . import services
from . import embeds

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    economia = app_commands.Group(name="eco", description="Sistema de economia.")

    @economia.command(name="carteira", description="Mostra sua carteira")
    async def coins(self, interaction: discord.Interaction):
        user = await services.get_user(interaction.user.id)

        await interaction.response.send_message(
            embed=embeds.carteira(
                f"💰 Coins: **{user['coins']:,}**\n"
                f"📦 Boxes: **{user['boxes']:,}**\n"
                f"🔥 Daily: **{user['daily_streak']:,}**"
            )
        )
    
    @economia.command(name="diario", description="pegue coins diárias")
    async def daily(self, interaction: discord.Interaction):
        user = await services.daily(interaction.user.id)

        if user["already_claimed"]:
            await interaction.response.send_message(
                embed=embeds.erro("⏳ Você já pegou o daily hoje.")
            )
            return

        await interaction.response.send_message(
            embed=embeds.daily(
                f"🎁 Daily coletado!\n+{user['reward']} coins\n🔥 Streak: {user['streak']}"
            )
        )
    
    @economia.command(name="work", description="Trabalhe para ganhar coins.")
    @app_commands.checks.cooldown(1, 10)
    async def work(self, interaction: discord.Interaction):
        user = await services.work(interaction.user.id)
        await interaction.response.send_message(embed=embeds.work(f"Você trabalhou como **{user['job']}** por 1 hora\n💰 Recebeu **{user['reward']} coins**"))

    @work.error
    async def work_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            if interaction.response.is_done():
                await interaction.followup.send(
                    embed=embeds.erro(f"⏳ Espere {round(error.retry_after)} segundos para usar novamente."),
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=embeds.erro(f"⏳ Espere {round(error.retry_after)} segundos para usar novamente."),
                    ephemeral=True
                )


async def setup(bot):
    await bot.add_cog(Economia(bot))