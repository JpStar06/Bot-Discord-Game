import discord
from cogs.ticket.services import TicketService

class EditPanelView(discord.ui.View):

    def __init__(self, data, ticket_id, guild_id):
        super().__init__(timeout=300)
        self.data = data
        self.ticket_id = ticket_id
        self.guild_id = guild_id

    @discord.ui.button(label="Salvar", style=discord.ButtonStyle.success)
    async def salvar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await TicketService.update_panel(
            self.guild_id,
            self.ticket_id,
            self.data
        )

        await interaction.response.send_message(
            "✅ Alterações salvas!",
            ephemeral=True
        )

class EditTopicView(discord.ui.View):

    def __init__(self, data, ticket_id, guild_id):
        super().__init__(timeout=300)
        self.data = data
        self.ticket_id = ticket_id
        self.guild_id = guild_id

    @discord.ui.button(label="Salvar", style=discord.ButtonStyle.success)
    async def salvar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await TicketService.update_topic(
            self.guild_id,
            self.ticket_id,
            {
                "titulo": self.data["titulo"],
                "descricao": self.data["descricao"],
                "cor": self.data["cor"],
                "imagem": self.data["imagem"]
            }
        )

        await interaction.response.send_message(
            "✅ Tópico atualizado com sucesso!",
            ephemeral=True
        )