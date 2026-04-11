import discord
from cogs.ticket.embeds import TicketEmbed
from cogs.ticket.view import EditPanelView

class EditPanelModal(discord.ui.Modal, title="Editar Painel"):

    def __init__(self, data, ticket_id, guild_id):
        super().__init__()

        self.ticket_id = ticket_id
        self.guild_id = guild_id
        self.data = dict(data)

        self.titulo = discord.ui.TextInput(
            label="Título",
            default=data["titulo"]
        )

        self.descricao = discord.ui.TextInput(
            label="Descrição",
            style=discord.TextStyle.paragraph,
            default=data["descricao"]
        )

        self.cor = discord.ui.TextInput(
            label="Cor (hex ou int)",
            default=str(data["cor"])
        )

        self.imagem = discord.ui.TextInput(
            label="URL da imagem",
            required=False,
            default=data.get("imagem")
        )

        self.add_item(self.titulo)
        self.add_item(self.descricao)
        self.add_item(self.cor)
        self.add_item(self.imagem)

    async def on_submit(self, interaction: discord.Interaction):

        self.data.update({
            "titulo": self.titulo.value,
            "descricao": self.descricao.value,
            "cor": int(self.cor.value),
            "imagem": self.imagem.value or None
        })

        embed = TicketEmbed.painel(self.data)

        view = EditPanelView(
            self.data,
            self.ticket_id,
            self.guild_id
        )

        await interaction.response.send_message(
            content="👀 Pré-visualização:",
            embed=embed,
            view=view,
            ephemeral=True
        )