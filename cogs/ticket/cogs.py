import discord
from discord import app_commands
from discord.ext import commands
from ticket.modals import EditPanelModal
from ticket.services import TicketService
from ticket.embeds import TicketEmbed
from ticket.view import EditPanelView


class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    tickets = app_commands.Group(name="tickets", description="Sistema de tickets")

    # ---------- CRIAR ----------
    @tickets.command(name="criar")
    async def criar(self, interaction: discord.Interaction):

        ticket_id = await TicketService.create_ticket(
            interaction.guild.id,
            interaction.channel.id
        )

        await interaction.response.send_message(f"✅ Ticket criado ID `{ticket_id}`")

    # ---------- EDITAR (AGORA COM MODAL) ----------
    @tickets.command(name="editar-painel")
    async def editar(self, interaction: discord.Interaction, id: int):

        data = await TicketService.get_ticket(interaction.guild.id, id)

        if not data:
            await interaction.response.send_message("Ticket não encontrado.", ephemeral=True)
            return

        view = EditPanelView(dict(data), id, interaction.guild.id)

        embed = TicketEmbed.painel(data)

        await interaction.response.send_message(
            content="✏️ Editor de painel:",
            embed=embed,
            view=view,
            ephemeral=True
        )

    # ---------- ENVIAR ----------
    @tickets.command(name="enviar")
    async def enviar(self, interaction: discord.Interaction, id: int):

        data = await TicketService.get_ticket(interaction.guild.id, id)

        if not data:
            await interaction.response.send_message("Ticket não encontrado.", ephemeral=True)
            return

        embed = TicketEmbed.painel(data)

        await interaction.response.send_message(
            embed=embed,
            view=None
        )


async def setup(bot):
    await bot.add_cog(Tickets(bot))