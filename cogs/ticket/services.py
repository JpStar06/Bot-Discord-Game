import asyncpg
import os
from dotenv import load_dotenv

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
            titulo_cliente=$1, descricao_cliente=$2, cor_cliente=$3, imagem_cliente=$4
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