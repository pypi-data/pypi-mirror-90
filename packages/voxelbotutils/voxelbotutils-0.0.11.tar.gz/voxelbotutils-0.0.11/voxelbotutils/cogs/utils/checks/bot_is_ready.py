from discord.ext import commands


class BotNotReady(commands.CheckFailure):
    """The generic error for the bot failing the bot_is_ready check"""


def bot_is_ready():
    """The check for whether the bot has cached all of its data yet"""

    async def predicate(ctx:commands.Context):
        if ctx.bot.is_ready() and (ctx.bot.startup_method is None or ctx.bot.startup_method.done()):
            return True
        raise BotNotReady("The bot isn't marked as ready to process commands yet - please wait a minute or so.")
    return commands.check(predicate)
