import discord

def carteira(msg: str):
    return discord.Embed(
        title="CARTEIRA",
        description=msg,
        color=discord.Color.yellow()
    )