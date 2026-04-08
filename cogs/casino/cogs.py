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
            await interaction.response.send_message(embed=embeds.erro("Escolha `cara` ou `coroa`", ephemeral=True))
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
            await interaction.response.send_message(embed=embeds.erro(f"⏳ Espere {round(error.retry_after)} segundos para usar novamente.",
                ephemeral=True))

    #-----------dices-----------------------
    @casino.command(name="dice", description="Jogue dados")
    @app_commands.checks.cooldown(1, 6)
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

    @dice.error
    async def dice_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(embed=embeds.erro(f"⏳ Espere {round(error.retry_after)} segundos para usar novamente.",
                ephemeral=True))
#---------------------SLOTS----------------------
    @casino.command(name="slots", description="Caça-níquel")
    @app_commands.checks.cooldown(1, 6)
    async def slots(self, interaction: discord.Interaction, aposta: int):
        coins = await self.get_coins(interaction.user.id)
        if aposta > coins:
            await interaction.response.send_message(embed=embeds.erro("Você não tem coins suficientes."))
            return
        
        (r1, r2, r3), ganho, tipo = services.spin_slots(aposta)
        resultado = f"{r1} | {r2} | {r3}\n"

        if tipo == "jackpot":
            embed = embeds.ganhou(resultado + f"🎉 JACKPOT! Você ganhou `{ganho}` coins!")
        elif tipo == "lose":
            embed = embeds.perdeu(resultado + f"❌ LOSE! Você perdeu `{ganho}` coins!")
        else:
            embed = embeds.ganhou(resultado + f"✨ Você ganhou `{ganho}` coins!")

        await self.add_coins(interaction.user.id, ganho)
        await interaction.response.send_message(embed=embed)
    
    @slots.error
    async def slots_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(embed=embeds.erro(f"⏳ Espere {round(error.retry_after)} segundos para usar novamente.",
                ephemeral=True))
# -------------------- SETUP --------------------
async def setup(bot):
    await bot.add_cog(Casino(bot))
