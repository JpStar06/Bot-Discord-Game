import discord
from . import services

class BlackjackView(discord.ui.View):
    def __init__(self, player, dealer, user_id, aposta):
        super().__init__(timeout=60)
        self.player = player
        self.dealer = dealer
        self.user_id = user_id
        self.aposta = aposta
        self.get_coins = services.get_coins
        self.add_coins = services.add_coins

    def build_embed(self, hidden=True):
        dealer_hand = "?, " + ", ".join(map(str, self.dealer[1:])) if hidden else ", ".join(map(str, self.dealer))

        return discord.Embed(
            title="🃏 Blackjack",
            description=(
                f"**Sua mão:** {', '.join(map(str, self.player))} ({services.calculate_hand(self.player)})\n"
                f"**Dealer:** {dealer_hand}"
            ),
            color=discord.Color.green()
        )

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Não é seu jogo.", ephemeral=True)

        self.player.append(services.draw_card())

        if services.calculate_hand(self.player) > 21:
            await self.add_coins(self.user.id, -self.aposta)
            embed = self.build_embed(hidden=False)
            embed.description += "\n💀 Você estourou!"
            self.stop()
            return await interaction.response.edit_message(embed=embed, view=None)

        await interaction.response.edit_message(embed=self.build_embed(), view=self)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Não é seu jogo.", ephemeral=True)

        # dealer joga
        while services.calculate_hand(self.dealer) < 17:
            self.dealer.append(services.draw_card())

        player_total = services.calculate_hand(self.player)
        dealer_total = services.calculate_hand(self.dealer)

        embed = self.build_embed(hidden=False)

        if dealer_total > 21 or player_total > dealer_total:
            embed.description += f"\n🎉 Você venceu!\n +{self.aposta} coins"
            await self.add_coins(self.user_id, self.aposta)
        elif player_total < dealer_total:
            embed.description += f"\n💀 Você perdeu!\n -{self.aposta} coins"
            await self.add_coins(self.user_id, -self.aposta)
        else:
            embed.description += "\n🤝 Empate!"

        self.stop()
        await interaction.response.edit_message(embed=embed, view=None)