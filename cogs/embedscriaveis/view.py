import discord

class EmbedBuilderView(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=300)
        self.author = author

        self.title = "Título"
        self.description = "Descrição"
        self.color = discord.Color.blue()
        self.image = None

    def build_embed(self):
        embed = discord.Embed(
            title=self.title,
            description=self.description,
            color=self.color
        )
        if self.image:
            embed.set_image(url=self.image)
        return embed

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.author