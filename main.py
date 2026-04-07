import discord
from discord.ext import commands
import asyncio
import os
import dotenv
from database import init_db

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")
    await bot.tree.sync()


async def main():
    await init_db()

    async with bot:
        count = 0
        for folder in os.listdir("./cogs"):
            path = f"./cogs/{folder}"

            if os.path.isdir(path):
                try:
                    await bot.load_extension(f"cogs.{folder}.cogs")
                    print(f"✅ Cog '{folder}' carregada com sucesso!")
                    count += 1
                except Exception as e:
                    print(f"❌ Erro ao carregar '{folder}': {e}")
        print(f"\n🚀 Total de cogs carregadas: {count}")

        await bot.start(TOKEN)


asyncio.run(main())
