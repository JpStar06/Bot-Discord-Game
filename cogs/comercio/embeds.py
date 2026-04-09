import discord

def carteira(msg: str):
    return discord.Embed(
        title="CARTEIRA",
        description=msg,
        color=discord.Color.yellow()
    )

def daily(msg: str):
    return discord.Embed(
        title="COINS DIÁRIA",
        description=msg,
        color=discord.Color.green()
    )

def erro(msg: str):
    return discord.Embed(
        title="Erro",
        description=msg,
        color=discord.Color.red()
    )