from discord.ext import commands

from .cooldown import Cooldown


class CooldownWithChannelExemptions(Cooldown):
    """
    A custom cooldown which allows for channel white/blacklisting by name.

    Params:
        cooldown_in : typing.List[str]
            A list of channel names where the cooldown should apply. If left blank, it'll apply everywhere minus the blacklist given.
        no_cooldown_in : typing.List[str]
            A list of channel names where the cooldown shouldn't apply. If left blank, it won't apply anywhere apart from the whitelist.
    """

    _copy_kwargs = ('cooldown_in', 'no_cooldown_in')

    def __init__(self, *, cooldown_in:list=None, no_cooldown_in:list=None, **kwargs):
        """
        Args:
            cooldown_in (list, optional): A list of channel names where the cooldown should apply. If left blank, it'll apply everywhere minus the blacklist given.
            no_cooldown_in (list, optional): A list of channel names where the cooldown shouldn't apply. If left blank, it won't apply anywhere apart from the whitelist.
            **kwargs: The default kwargs to be passed to the original cooldown class.

        Raises:
            ValueError: There are no channels set to blacklist or whitelist.
        """

        super().__init__(**kwargs)
        if cooldown_in is None and no_cooldown_in is None:
            raise ValueError("You need to set at least one channel in your blacklist/whitelist")
        self.cooldown_in = cooldown_in or []
        self.no_cooldown_in = no_cooldown_in or []

    def __call__(self, rate, per, type=None):
        super().__call__(rate, per, commands.BucketType.channel)  # Override cooldown type
        return self

    def predicate(self, ctx) -> bool:
        """
        The check to see if this cooldown is applied.
        """

        # Check if invoked in a channel where there should be no cooldown
        if self.no_cooldown_in:
            if any([i for i in self.no_cooldown_in if i == ctx.channel.name]):
                return False

        # Check if invoked in a channel where there SHOULD be a cooldown
        if self.cooldown_in:
            if any([i for i in self.cooldown_in if i == ctx.channel.name]):
                return True
            return False  # Not invoked in a cooldown_in channel

        # Default answer - trigger cooldown
        return True
