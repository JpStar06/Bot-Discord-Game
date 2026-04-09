import discord
from discord import app_commands
from discord.ext import commands
from . import services
from . import embeds

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    economia = app_commands.Group(name="eco", description="Sistema de economia.")
    box = app_commands.Group(name="box", description= "Sistema de boxes")
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
            await interaction.response.send_message(embed=embeds.erro("⏳ Você já pegou o daily hoje."))
            return

        await interaction.response.send_message(
            embed=embeds.daily(f"🎁 Daily coletado!\n+{user['reward']} coins\n🔥 Streak: {user['streak']}"))
    
    @economia.command(name="work", description="Trabalhe para ganhar coins.")
    @app_commands.checks.cooldown(1, 10)
    async def work(self, interaction: discord.Interaction):
        user = await services.work(interaction.user.id)

        await interaction.response.send_message(embed=embeds.work(f"Você trabalhou como **{user['job']}** por 1 hora\n💰 Recebeu **{user['reward']} coins**"))
    
    @work.error
    async def work_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            if interaction.response.is_done():
                await interaction.followup.send(embed=embeds.erro(f"⏳ Espere {round(error.retry_after)} segundos para usar novamente."), ephemeral=True)
            else:
                await interaction.response.send_message(embed=embeds.erro(f"⏳ Espere {round(error.retry_after)} segundos para usar novamente."), ephemeral=True)

    @economia.command(name="pay", description="Envie coins para outro usuário")
    async def pay(self, interaction: discord.Interaction, usuario: discord.Member, quantia: int):
        user = await services.transfer(interaction.user.id)
        if user["error"] == "invalid_amount":
            await interaction.response.send_message(embed=embeds.erro("o valor minimo de transação é de 100 coins."))
        elif user["error"] == "no_money":
            await interaction.response.send_message(embed=embeds.erro("Você não tem coins suficiente para essa transação."))
        else:
            await interaction.response.send_message(embed=embeds.pay(f"Você enviou {user['enviado']} coins para {user['target_id']}"))
        

    @box.command(name="comprar", description="Comprar lootbox")
    async def buy_box(self, interaction: discord.Interaction):
        user = await services.buy_box(interaction.user.id)
        if user['success'] == False:
            await interaction.response.send_message(embed=embeds.erro(f"Você não pode comprar essa box.\n ainda falta {user['faltante']} coins para finalizar a compra."))
        else:
            await interaction.response.send_message(embed=embeds.compra("📦 Você comprou uma lootbox!"))

    @box.command(name="abrir", description="Abrir lootbox")
    async def open_box(self, interaction: discord.Interaction):
        data = await services.open_box(interaction.user.id)

        if not data:
            await interaction.response.send_message(
                embed=embeds.erro("📦 Você não tem lootboxes."),
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            embed=embeds.ganhou(
                f"📦 Você abriu uma lootbox!\n"
                f"{data['rarity']}\n"
                f"💰 Você ganhou **{data['reward']} coins**"
            )
        )
    

async def setup(bot):
    await bot.add_cog(Economia(bot))