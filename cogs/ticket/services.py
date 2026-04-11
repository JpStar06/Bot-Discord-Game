import asyncpg
import os
from dotenv import load_dotenv
import discord

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


class TicketService:

    @staticmethod
    async def get_connection():
        return await asyncpg.connect(DATABASE_URL)

    # ---------- CREATE ----------
    @staticmethod
    async def create_ticket(guild_id: int, channel_id: int):
        conn = await TicketService.get_connection()

        ticket_id = await conn.fetchval(
            """
            INSERT INTO tickets (
                guild_id, titulo, descricao, cor, emoji, canal_id,
                titulo_cliente, descricao_cliente, cor_cliente
            )
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
            RETURNING id
            """,
            guild_id,
            "Suporte",
            "Clique no botão abaixo para abrir um ticket.",
            0x3498db,
            "🎫",
            channel_id,
            "ESPERE SER ATENDIDO",
            "Nossa equipe pode estar ocupada.",
            0xFF0000
        )

        await conn.close()
        return ticket_id

    # ---------- GET ----------
    @staticmethod
    async def get_ticket(guild_id: int, ticket_id: int):
        conn = await TicketService.get_connection()

        data = await conn.fetchrow(
            "SELECT * FROM tickets WHERE id=$1 AND guild_id=$2",
            ticket_id,
            guild_id
        )

        await conn.close()
        return data

    # ---------- UPDATE ----------
    @staticmethod
    async def update_panel(guild_id, ticket_id, data: dict):
        conn = await TicketService.get_connection()

        await conn.execute(
            """
            UPDATE tickets SET titulo=$1, descricao=$2, cor=$3, imagem=$4
            WHERE id=$5 AND guild_id=$6
            """,
            data["titulo"],
            data["descricao"],
            data["cor"],
            data["imagem"],
            ticket_id,
            guild_id
        )

        await conn.close()

    @staticmethod
    async def update_topic(guild_id, ticket_id, data: dict):
        conn = await TicketService.get_connection()

        await conn.execute(
            """
            UPDATE tickets SET 
            titulo_cliente=$1,
            descricao_cliente=$2,
            cor_cliente=$3,
            imagem_cliente=$4,
            staff_id=$5
            WHERE id=$6 AND guild_id=$7
            """,
            data["titulo"],
            data["descricao"],
            data["cor"],
            data["imagem"],
            data.get("staff_id"),  # 🔥 NOVO
            ticket_id,
            guild_id
        )

        await conn.close()
    
    @staticmethod
    async def create_thread(interaction, ticket_id, user):
        conn = await TicketService.get_connection()

        data = await conn.fetchrow(
            """
            SELECT 
                titulo_cliente, descricao_cliente, cor_cliente, imagem_cliente, staff_id
            FROM tickets 
            WHERE id=$1 AND guild_id=$2
            """,
            ticket_id,
            interaction.guild.id
        )

        await conn.close()

        if not data:
            return None, "Configuração não encontrada."

        try:
            thread = await interaction.channel.create_thread(
                name=f"ticket-{user.name}",
                type=discord.ChannelType.private_thread
            )

            await thread.add_user(user)

            # 👮 adiciona staff (se tiver)
            if data["staff_id"]:
                role = interaction.guild.get_role(data["staff_id"])

                if role:
                    for member in role.members:
                        await thread.add_user(member)


        except Exception as e:
            return None, str(e)

        return thread, data