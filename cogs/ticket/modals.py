import discord
from cogs.ticket.embeds import TicketEmbed
from cogs.ticket.view import EditPanelView
from cogs.ticket.view import EditTopicView
import re


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

        staff_id = None

        if self.staff.value:
            import re

            match = re.search(r"\d+", self.staff.value)

            if match:
                staff_id = int(match.group())

        self.data.update({
            "titulo": self.titulo.value,
            "descricao": self.descricao.value,
            "cor": int(self.cor.value),
            "imagem": self.imagem.value or None,
            "staff_id": staff_id
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

class EditTopicModal(discord.ui.Modal, title="Editar Tópico do Ticket"):

    def __init__(self, data, ticket_id, guild_id):
        super().__init__()

        self.data = dict(data)
        self.ticket_id = ticket_id
        self.guild_id = guild_id
        
        self.staff = discord.ui.TextInput(
            label="Cargo Staff",
            placeholder="@Staff",
            required=False,
            default=str(data.get("staff_id") or "")
        )

        self.titulo = discord.ui.TextInput(
            label="Título",
            default=data["titulo_cliente"]
        )

        self.descricao = discord.ui.TextInput(
            label="Descrição",
            style=discord.TextStyle.paragraph,
            default=data["descricao_cliente"]
        )

        self.cor = discord.ui.TextInput(
            label="Cor (int ou hex)",
            default=str(data["cor_cliente"])
        )

        self.imagem = discord.ui.TextInput(
            label="URL da imagem",
            required=False,
            default=data.get("imagem_cliente")
        )

        self.add_item(self.titulo)
        self.add_item(self.descricao)
        self.add_item(self.cor)
        self.add_item(self.imagem)
        self.add_item(self.staff)

    async def on_submit(self, interaction: discord.Interaction):
        staff_id = None
        if self.staff.value:
            match = re.search(r"\d+", self.staff.value)
            if match:
                staff_id = int(match.group())

        self.data.update({
            "titulo": self.titulo.value,
            "descricao": self.descricao.value,
            "cor": int(self.cor.value),
            "imagem": self.imagem.value or None,
            "staff_id": staff_id
        })

        embed = TicketEmbed.topico({
            "titulo_cliente": self.data["titulo"],
            "descricao_cliente": self.data["descricao"],
            "cor_cliente": self.data["cor"],
            "imagem_cliente": self.data["imagem"]
        })

        view = EditTopicView(
            self.data,
            self.ticket_id,
            self.guild_id
        )

        await interaction.response.send_message(
            content="👀 Pré-visualização do tópico:",
            embed=embed,
            view=view,
            ephemeral=True
        )