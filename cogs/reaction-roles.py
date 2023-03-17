import logging
import discord
from discord.ext import commands
from discord import app_commands

logger = logging.getLogger('bot.cogs.reaction-roles')
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

class ReactionRolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        message = await self.bot.get_channel(1065672913388326922).fetch_message(1068367226471727104)
        for reaction in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]:
            await message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == 1068367226471727104:
            guild = self.bot.get_guild(payload.guild_id)
            
            member = guild.get_member(payload.user_id)
            if member.bot:
                return
            
            if 987370945016639558 not in member.roles:
                await member.add_roles(guild.get_role(987370945016639558), reason="Reaction Role")

            if payload.emoji.name == "1️⃣":
                await member.add_roles(guild.get_role(989307961568538674), reason="Reaction Role")

            elif payload.emoji.name == "2️⃣":
                await member.add_roles(guild.get_role(989308071455096852), reason="Reaction Role")

            elif payload.emoji.name == "3️⃣":
                await member.add_roles(guild.get_role(1068365691054465076), reason="Reaction Role")
            
            elif payload.emoji.name == "4️⃣":
                await member.add_roles(guild.get_role(1068365759635521637), reason="Reaction Role")
            
            elif payload.emoji.name == "5️⃣":
                await member.add_roles(guild.get_role(1068365932566683680), reason="Reaction Role")
            
            logger.info('Reaction Roles: ' + member.name + ' added ' + payload.emoji.name + ' to ' + member.name + ' in ' + guild.name + '')
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == 1068367226471727104:
            guild = self.bot.get_guild(payload.guild_id)

            member = guild.get_member(payload.user_id)
            if member.bot:
                return
            
            if payload.emoji.name == "1️⃣":
                await member.remove_roles(guild.get_role(989307961568538674), reason="Reaction Role")

            elif payload.emoji.name == "2️⃣":
                await member.remove_roles(guild.get_role(989308071455096852), reason="Reaction Role")

            elif payload.emoji.name == "3️⃣":
                await member.remove_roles(guild.get_role(1068365691054465076), reason="Reaction Role")
            
            elif payload.emoji.name == "4️⃣":
                await member.remove_roles(guild.get_role(1068365759635521637), reason="Reaction Role")
            
            elif payload.emoji.name == "5️⃣":
                await member.remove_roles(guild.get_role(1068365932566683680), reason="Reaction Role")
            
            logger.info('Reaction Roles: ' + member.name + ' removed ' + payload.emoji.name + ' from ' + member.name + ' in ' + guild.name + '')

            if (989307961568538674 not in member.roles 
                and 989308071455096852 not in member.roles 
                and 1068365691054465076 not in member.roles 
                and 1068365759635521637 not in member.roles 
                and 1068365932566683680 not in member.roles):
                await member.remove_roles(guild.get_role(987370945016639558), reason="Reaction Role")


async def setup(bot):
    await bot.add_cog(ReactionRolesCog(bot))