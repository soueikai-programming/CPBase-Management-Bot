import discord
from discord import app_commands
from discord.ext import commands

import logging
import glob

logger = logging.getLogger('bot.cog.manage-commands')
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

class CommandManager(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='ping', description='Pingを返します。')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms', ephemeral=True)
        logger.info(f'🏓Pingを返しました！ {round(self.bot.latency * 1000)}ms')
    
    @app_commands.command(name='reload', description='コマンドをリロードします。')
    async def reload(self, interaction: discord.Interaction):
        if interaction.user.id == 722072905604923393:
            logger.info('🔧コマンドをリロード中...')
            await interaction.response.send_message('リロードを開始します...', ephemeral=True)
            for a in logger.handlers:
                if(a.get_name() != 'bot.main'):
                    logger.removeHandler(a)
            for cog in cogs:
                logger.debug(f'🔧{cog}を有効化中...')
                await self.bot.reload_extension(cog)
                logger.debug(f'🔧{cog}が有効になりました！')
            await interaction.followup.send('リロードが完了しました！', ephemeral=True)
        else:
            await interaction.response.send_message('あなたにはこのコマンドを実行する権限がありません。', ephemeral=True)
    
    @app_commands.command(name='shutdown', description='Botをシャットダウンします。')
    async def shutdown(self, interaction: discord.Interaction):
        if interaction.user.id == 722072905604923393:
            logger.info('😪Botをシャットダウンします...')
            await interaction.response.send_message('Botをシャットダウンします...', ephemeral=True)
            await self.bot.close()
        else:
            await interaction.response.send_message('あなたにはこのコマンドを実行する権限がありません。', ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(CommandManager(bot))