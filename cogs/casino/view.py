import discord
from discord.ext import commands
import services

#----------erro embed---------

embed_erro = discord.Embed(
title= "Erro",
description= f"{text_erro}",
color=discord.Color.red()
)