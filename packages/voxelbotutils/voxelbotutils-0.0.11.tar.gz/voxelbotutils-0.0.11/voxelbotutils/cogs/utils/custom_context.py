import random

import discord
from discord.ext import commands


class Context(commands.Context):

    DESIRED_PERMISSIONS = discord.Permissions(embed_links=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_author_id = self.author.id
        self.is_slash_command = False

    async def okay(self) -> None:
        """
        Adds the okay hand reaction to a message.
        """

        return await self.message.add_reaction("\N{OK HAND SIGN}")

    @property
    def clean_prefix(self):
        """
        Gives the prefix used to run the command but cleans up the bot mention.
        """

        return self.prefix.replace(f"<@{self.bot.user.id}>", f"@{self.bot.user.name}").replace(f"<@!{self.bot.user.id}>", f"@{self.bot.user.name}")

    def _set_footer(self, embed:discord.Embed) -> None:
        """
        Sets a footer on the embed from the config
        """

        pool = []
        for data in self.bot.config.get('embed', dict()).get('footer', list()):
            safe_data = data.copy()
            amount = safe_data.pop('amount')
            if amount <= 0:
                continue
            text = safe_data.pop('text')
            text = text.format(ctx=self)
            safe_data['text'] = text
            for _ in range(amount):
                pool.append(safe_data.copy())
        if not pool:
            return
        embed.set_footer(**random.choice(pool), icon_url=self.bot.user.avatar_url)

    async def send(
            self, content:str=None, *args, embed:discord.Embed=None, file:discord.File=None, ignore_error:bool=False, embeddify:bool=None,
            embeddify_file:bool=True, image_url:str=None, **kwargs) -> discord.Message:
        """
        The normal `discord.abc.Messageable.send` but with an optional arg to ignore errors, as well as automatically
        embedding the content based on the bot's config.

        Args:
            content (str, optional): The content to be sent.
            *args: The default args for `discord.abc.Messageable.send`.
            embed (discord.Embed, optional): The embed object to be sent with the message.
            file (discord.File, optional): The file object to be sent with the message.
            ignore_error (bool, optional): Whether or not to ignore `discord.HTTPException` errors on message send.
            embeddify (bool, optional): Whether or not to automatically embed the content of the message.
            embeddify_file (bool, optional): Whether or not ot automatically embed the file of the message.
            **kwargs: The default args for `discord.abc.Messageable.send`.

        Returns:
            discord.Message: The message that was returned to Discord.

        Raises:
            discord.HTTPException: If the message send should fail, this is the erorr that was raised.
        """

        # Set default embeddify
        if embeddify is None and image_url is not None:
            embeddify = True
        if embeddify is None:
            embeddify = self.bot.embeddify

        # See if we need to check channel permissions at all
        if embeddify is False or embed is not None:
            should_not_embed = True
        else:
            try:
                channel_permissions: discord.Permissions = self.channel.permissions_for(self.guild.me)
                missing_embed_permission = not self.DESIRED_PERMISSIONS.is_subset(channel_permissions)
            except AttributeError:
                missing_embed_permission = False
            should_not_embed = any([
                missing_embed_permission,
                embeddify is False,
                embed is not None,
            ])

        # Can't embed? Just send it normally
        if should_not_embed:
            try:
                return await super().send(content, *args, embed=embed, file=file, **kwargs)
            except Exception as e:
                if ignore_error:
                    return None
                raise e

        # No current embed, and we _want_ to embed it? Alright!
        embed = discord.Embed(description=content, colour=random.randint(1, 0xffffff) or self.bot.config.get('embed', dict()).get('colour', 0))
        self._set_footer(embed)

        # Set image
        if image_url is not None:
            embed.set_image(url=image_url)
        if file and file.filename and embeddify_file:
            file_is_image = any([
                file.filename.casefold().endswith('.png'),
                file.filename.casefold().endswith('.jpg'),
                file.filename.casefold().endswith('.jpeg'),
                file.filename.casefold().endswith('.gif'),
                file.filename.casefold().endswith('.webm')
            ])
            if file_is_image:
                embed.set_image(url=f'attachment://{file.filename}')

        # Reset content
        content = self.bot.config.get('embed', dict()).get('content', '').format(ctx=self) or None

        # Set author
        author_data = self.bot.config.get('embed', dict()).get('author')
        if author_data.get('enabled', False):
            name = author_data.get('name', '').format(ctx=self) or discord.Embed.Empty
            url = author_data.get('url', '').format(ctx=self) or discord.Embed.Empty
            author_data = {
                'name': name,
                'url': url,
                'icon_url': self.bot.user.avatar_url,
            }
            embed.set_author(**author_data)

        # Sick now let's send the data
        return await self.send(content, *args, embed=embed, file=file, ignore_error=ignore_error, **kwargs)
