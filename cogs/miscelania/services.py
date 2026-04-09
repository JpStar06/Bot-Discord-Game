import random
import discord

async def ball(pergunta: str):
    respostas = [
            "Sim.",
            "Não.",
            "Talvez.",
            "Com certeza.",
            "Pergunte novamente depois.",
            "Muito improvável.",
            "Definitivamente."
        ]
    resposta = random.choice(respostas)
    return resposta