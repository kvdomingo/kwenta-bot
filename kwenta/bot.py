import asyncio
import logging

import discord
from discord.ext.commands import Bot
from loguru import logger

from .cogs import COGS_TO_LOAD
from .config import BOT_PREFIX, DISCORD_TOKEN

logging.basicConfig(level=logging.INFO)


@logger.catch
async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = Bot(intents=intents, command_prefix=BOT_PREFIX)
    for Cog in COGS_TO_LOAD:
        await bot.add_cog(Cog(bot))

    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
