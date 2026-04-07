import discord
import discord.ext

def erro(msg: str):
    return discord.Embed(
        title="Erro",
        description=msg,
        color=discord.Color.red()
    )