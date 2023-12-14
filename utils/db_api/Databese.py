from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(user=config.DB_USER, password=config.DB_PASS, host=config.DB_HOST,
                                              database=config.DB_NAME, )

    async def execute(self, command, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False,
                      execute: bool = False, ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict, start=1):
        sql += " AND ".join([f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=start)])
        return sql, tuple(parameters.values())

# users table start------------------------------
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        user_id numeric NOT NULL,
        status text,
        join_date text NOT NULL,
        lang text,
        CONSTRAINT user_id UNIQUE (user_id)
        INCLUDE(user_id)
        );
        """
        await self.execute(sql, execute=True)

    async def add_user(self, user_id, join_date, status='active', lang='uz'):
        sql = "INSERT INTO users (user_id, status, join_date, lang) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, user_id, status, join_date, lang, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users;"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM users"
        return await self.execute(sql, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def update_status(self, status, user_id):
        sql = "UPDATE users SET status=$1 WHERE user_id=$2"
        return await self.execute(sql, status, user_id, execute=True)

    async def update_language(self, language, user_id):
        sql = "UPDATE users SET language=$1 WHERE user_id=$2"
        return await self.execute(sql, language, user_id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users", execute=True)

# users table end------------------------------

# Channels start-----------------------------------
    async def create_table_channels(self):
        sql = """
        CREATE TABLE IF NOT EXISTS channels (
        channel_id TEXT UNIQUE NOT NULL,
        link TEXT
        );
        """
        await self.execute(sql, execute=True)

    async def add_channel(self, channel_id: str, link: str = None):
        sql = """
        INSERT INTO channels(channel_id, link)  VALUES($1, $2) returning *
        """
        return await self.execute(sql, channel_id, link, fetchrow=True)

    async def select_all_channels(self):
        sql = """
        SELECT * FROM channels;
        """
        return await self.execute(sql, fetch=True)

    async def select_channel(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM channels WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_channel(self, **kwargs):
        # SQL_EXAMPLE = "DELETE FROM Users where id=1 AND Name='John'"
        sql = "DELETE FROM channels WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_channels(self):
        sql = "SELECT COUNT(*) FROM channels;"
        return await self.execute(sql, fetchval=True)

    async def delete_channels(self):
        await self.execute("DELETE FROM channels WHERE TRUE", execute=True)

    async def drop_channels(self):
        await self.execute("DROP TABLE channels", execute=True)

# Channels end-------------------------------------

# Admins start--------------------------------
    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
        admin_id TEXT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def add_admin(self, admin_id):
        sql = """INSERT INTO admins(admin_id) VALUES($1) returning *"""
        return await self.execute(sql, admin_id, fetchrow=True)

    async def remove_admin(self, **kwargs):
        sql = """DELETE FROM admins WHERE """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_admin(self, **kwargs):
        sql = "SELECT * FROM admins WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_admins(self):
        sql = """
        SELECT * FROM admins;
        """
        sql = await self.execute(sql, fetch=True)
        return sql

    async def count_admins(self):
        sql = "SELECT COUNT(*) FROM admins;"
        return await self.execute(sql, fetchval=True)

    async def delete_admins(self):
        await self.execute("DELETE FROM admins WHERE TRUE", execute=True)

# Admins end--------------------------------