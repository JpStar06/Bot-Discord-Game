import discord
from discord import app_commands
from discord.ext import commands
import datetime
from database import get_connection
from . import embeds
from . import services
from .view import EmbedBuilderView

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

    #----------------EDITAR EMBED---------------------------
    @embed.command(name="editar", description="Edita um embed.")
    @app_commands.checks.has_permissions(administrator=True)
    async def editarembed(self, interaction: discord.Interaction, id: int, novo_titulo: str = None, novo_descricao: str = None, nova_cor: int = None, imagem_url: str = None):

        data = await services.editar_embed(interaction.guild.id, id, novo_titulo, novo_descricao, nova_cor, imagem_url)

        if not data:
            await interaction.response.send_message("Embed não encontrado.", ephemeral=True)
            return

        embed = discord.Embed(
            title=data["title"], description=data["description"], color=data["color"])

        if data["image"]:
            embed.set_image(url=data["image"])

        await interaction.response.send_message("Embed atualizado:", embed=embed)


    @embed.command(name="listar", description="Lista os embeds.")
    @app_commands.checks.has_permissions(administrator=True)
    async def listarembeds(self, interaction: discord.Interaction):
        embeds_list = await services.listarembeds(interaction.guild.id)

        if not embeds_list:
            await interaction.response.send_message("Nenhum embed criado.",ephemeral=True)
            return

        lista = "\n".join([f"ID `{e['id']}` - {e['title']}" for e in embeds_list])

        await interaction.response.send_message(lista)

    @embed.command(name="deletar", description="Deleta um embed.")
    @app_commands.checks.has_permissions(administrator=True)
    async def deletarembed(self, interaction: discord.Interaction, id: int):

        success = await services.deletar_embed(interaction.guild.id, id)

        if not success:
            await interaction.response.send_message(f"Embed `{id}` não encontrado.",ephemeral=True)
            return

        await interaction.response.send_message(f"Embed `{id}` deletado com sucesso.")
    
    @embed.command(name="builder", description="Criar embed interativo")
    async def builder(self, interaction: discord.Interaction):

        view = EmbedBuilderView(interaction.user)

        await interaction.response.send_message(
            embed=view.build_embed(),
            view=view
        )

async def setup(bot):
    await bot.add_cog(Comandos(bot))