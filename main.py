import discord
from discord.ext import commands

import datetime
import logging
import logging.handlers
import glob
import os
import asyncio

logger = logging.getLogger('bot.main')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='log/discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

cogs = glob.glob('cogs/*.py')
if len(cogs) > 0:
    cogs = [cog.replace('\\', '.').replace('.py', '') for cog in cogs]
print(cogs)

class CPBaseManager(commands.Bot):
    def __init__(self, *, prefix, intents: discord.Intents) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or(prefix), intents=intents)
        logger.info('🚽根幹システムを有効化中...')

    async def on_ready(self):
        await self.change_presence(activity=discord.Game('起動日時: ' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        logger.info('✨Botがオンラインになりました！')

async def main():
    bot = CPBaseManager(prefix='!', intents=discord.Intents.all())
    if len(cogs) > 0:
        logger.info('🚽分散機能を有効化中...')
        for cog in cogs:
            logger.debug(f'🔧{cog}を有効化中...')
            await bot.load_extension(cog)
            logger.debug(f'🔧{cog}が有効になりました！')
    
    await bot.start(token=os.environ.get('CPBaseManagementBot_TOKEN', ''))

if __name__ == '__main__':
    asyncio.run(main())