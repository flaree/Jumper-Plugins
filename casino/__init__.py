from .casino import Casino
from dislash.slash_commands import SlashClient

__red_end_user_data_statement__ = "This cog stores discord IDs as needed for operation."



async def setup(bot):
    cog = Casino(bot)
    bot.add_cog(cog)
    if not hasattr(bot, "slash"):
        bot.slash = SlashClient(bot)
    await cog.initialise()
