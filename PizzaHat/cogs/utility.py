import datetime
import time
import unicodedata
from typing import Optional, Union

import discord
import psutil
from core.bot import PizzaHat
from core.cog import Cog
from discord.ext import commands
from discord.ext.commands import Context

start_time = time.time()


def format_date(dt: datetime.datetime):
    if dt is None:
        return "N/A"
    return f"<t:{int(dt.timestamp())}>"


class Utility(Cog, emoji="🛠️"):
    """Utility commands that makes your Discord experience better!"""

    def __init__(self, bot: PizzaHat):
        self.bot: PizzaHat = bot
        self.process = psutil.Process()

    @commands.command(aliases=["latency"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx: Context):
        """Shows latency of bot."""

        time1 = time.perf_counter()
        msg = await ctx.send("Pinging...")
        time2 = time.perf_counter()

        await msg.edit(
            content="🏓 Pong!"
            f"\nAPI: `{round(self.bot.latency*1000)}ms`"
            f"\nBot: `{round(time2-time1)*1000}ms`"
        )

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def badges(self, ctx: Context, member: discord.Member = None):  # type: ignore
        """
        Shows different badges of a user.
        If no user is given, returns your badges.

        This command can be only used in the support server.
        """

        # thanks to .ddominik (Dominik#3040) for helping me out with this command.
        if ctx.guild.id != 764049436275114004 if ctx.guild else None:
            return await ctx.send(
                "This command can be only used in the support server.\nhttps://discord.gg/WhNVDTF"
            )

        badges = []
        member = member or ctx.author

        if ctx.guild is not None:
            staff_role = ctx.guild.get_role(849669358316683284)
            partner_role = ctx.guild.get_role(972071921791410188)
            booster_role = ctx.guild.get_role(782258520791449600)
            contrib_role = ctx.guild.get_role(950785470286163988)

            if self.bot.is_owner(member):
                badges.append("<:developer:833297795761831956> Developer of PizzaHat")

            for roles in member.roles:
                if roles == staff_role:
                    badges.append(
                        "<:staff:916988537264570368> Staff Member in the support server"
                    )

                elif roles == booster_role:
                    badges.append(
                        "<:booster:983684380134371339> Booster in the support server"
                    )

                elif roles == contrib_role:
                    badges.append(
                        "<:github:983685053752176691> Contributor of PizzaHat"
                    )

                elif roles == partner_role:
                    badges.append("<:partner:916988537033875468> PizzaHat's Partner")

            if member.avatar is not None:
                em = discord.Embed(title=f"{member} Badges", color=self.bot.color)
                em.set_thumbnail(url=member.avatar.url)
                em.description = (
                    "\n".join(badges)
                    if len(badges) != 0
                    else "This user has no special badges."
                )

                await ctx.send(embed=em)

            else:
                em = discord.Embed(title=f"{member} Badges", color=self.bot.color)
                em.set_thumbnail(url=ctx.guild.icon.url)  # type: ignore
                em.description = (
                    "\n".join(badges)
                    if len(badges) != 0
                    else "This user has no special badges."
                )

                await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def userinfo(self, ctx: Context, member: discord.Member = None):  # type: ignore
        """
        Shows info about a user.
        If no user is given, returns info about yourself.
        """

        member = member or ctx.author
        uroles = [role.mention for role in member.roles if not role.is_default()]
        uroles.reverse()

        user_badges_flags = {
            "hypesquad_bravery": "<:bravery:876078067548835850>",
            "hypesquad_balance": "<:balance:876078067297173534>",
            "hypesquad_brilliance": "<:brilliance:876078066848366662>",
            "hypesquad": "<:hypesquad:876081552826728459>",
            "partner": "<:partner:916988537033875468>",
            "verified_bot_developer": "<:developer:833297795761831956>",
            "active_developer": "<:activedev:1211600070819192922>",
            "bug_hunter_lvl_1": "<:bug_hunter_lvl1:876079074693480508> ",
            "bug_hunter_lvl_2": "<:bug_hunter_lvl2:876079074647371796>",
            "early_supporter": "<:supporter:843936375941103646>",
            "staff": "<:staff:916988537264570368>",
            "discord_certified_moderator": "<:certified_mod_badge:1211597953433862144>",
        }
        misc_flags_descriptions = {
            "team_user": "Application Team User",
            "system": "System User",
            "spammer": "Spammer",
            "verified_bot": "Verified Bot",
            "bot_http_interactions": "HTTP Interactions Bot",
        }

        set_flags = {flag for flag, value in member.public_flags if value}
        subset_flags = set_flags & user_badges_flags.keys()
        badges = [user_badges_flags[flag] for flag in subset_flags]

        if len(uroles) > 15:
            uroles = [f"{', '.join(uroles[:10])} (+{len(member.roles) - 11})"]

        user_roles = (
            (" **({} Total)**").format(len(member.roles) - 1)
            if uroles != []
            else ("No roles")
        )

        em = discord.Embed(
            title="User Information",
            color=member.color,
            timestamp=ctx.message.created_at,
        )
        em.description = f"""
    > **Username:** {member}
    > **Display Name:** {member.display_name}
    > **Created:** {format_date(member.created_at)}
    > **ID:** {member.id}
    {f"> **[User Icon]({member.avatar.url})**" if member.avatar else ""}
    """

        em.add_field(
            name="Joined",
            value=format_date(member.joined_at),  # type: ignore
            inline=False,
        )
        em.set_thumbnail(
            url=(
                member.avatar.url
                if member.avatar
                else "https://logos-world.net/wp-content/uploads/2020/12/Discord-Logo.png"
            )
        )

        em.add_field(name="Roles", value=", ".join(uroles) + user_roles, inline=False)
        em.add_field(
            name="Member Bot",
            value=f"{self.bot.yes} Yes" if member.bot else f"{self.bot.no} No",
            inline=False,
        )

        if ctx.guild is not None:
            if ctx.guild.owner_id == member.id:
                badges.append("<:owner:1211601449885110303>")

            elif (
                isinstance(member, discord.Member) and member.premium_since is not None
            ):
                em.add_field(
                    name="Boosted",
                    value=format_date(member.premium_since),
                    inline=False,
                )
                badges.append("<:booster:983684380134371339>")

        if badges:
            em.add_field(name="Badges", value=" ".join(badges), inline=False)

        em.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def serverinfo(self, ctx: Context):
        """Shows various info about the server."""

        def formatted_date(date):
            if date is None:
                return "N/A"
            return f"{date:%m-%d-%Y | %H:%M} UTC"

        if ctx.guild is not None:
            features = [f.lower().title().replace("_", " ") for f in ctx.guild.features]
            all_features = f"{self.bot.yes} " + f"\n{self.bot.yes} ".join(features)

            boost_level = (
                f"{ctx.guild.premium_tier} Level"
                if {ctx.guild.premium_tier} == 2
                else "No Level"
            )
            boosts = f"<:booster:983684380134371339> {ctx.guild.premium_subscription_count} Boosts ({boost_level})"

            em = discord.Embed(title=ctx.guild.name, color=self.bot.color)
            em.set_thumbnail(
                url=(
                    ctx.guild.icon.url
                    if ctx.guild.icon
                    else "https://logos-world.net/wp-content/uploads/2020/12/Discord-Logo.png"
                )
            )
            em.set_footer(text=f"Created at: {formatted_date(ctx.guild.created_at)}")

            if ctx.guild.owner is not None:
                em.description = f"""
    > **Owner:** {ctx.guild.owner.mention} `[{ctx.guild.owner}]`
    > **Description:** {ctx.guild.description if ctx.guild.description else "N/A"}
    > **ID:** {ctx.guild.id}
    {f"> **[Guild Icon]({ctx.guild.icon.url})**" if ctx.guild.icon else ""}
    """

            em.add_field(
                name=f"👥 {ctx.guild.member_count} Members",
                value=(
                    f"<:memberlist:811747305543434260> Humans: {len([m for m in ctx.guild.members if not m.bot])}\n"
                    f"<:botlist:811747723434786859> Bots: {sum(member.bot for member in ctx.guild.members)}"
                ),
                inline=False,
            )

            em.add_field(
                name="Channels",
                value=(
                    f"<:textchannel:811747767763992586> Text: {len(ctx.guild.text_channels)}\n"
                    f"<:voicechannel:811748732906635295> Voice: {len(ctx.guild.voice_channels)}\n"
                    f"📁 Categories: {len(ctx.guild.categories)}"
                ),
                inline=False,
            )

            em.add_field(
                name="<:role:985140259702583326> Role Count",
                value=len(ctx.guild.roles),
                inline=False,
            )
            em.add_field(
                name="🙂 Emoji Count", value=len(ctx.guild.emojis), inline=False
            )

            em.add_field(
                name="<:verified:985139472813412362> Verification level",
                value=str(ctx.guild.verification_level).capitalize(),
                inline=False,
            )

            em.add_field(
                name="✨ Server Features",
                value=(
                    f"{boosts}\n" + all_features
                    if boosts and features
                    else f"{self.bot.no} None"
                ),
                inline=False,
            )

            await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def channelinfo(self, ctx: Context, *, channel: discord.TextChannel = None):  # type: ignore
        """
        Shows info about a channel.
        If no channel is given, returns info for the current channel.
        """

        if channel is None:
            channel = ctx.channel  # type: ignore

        e = discord.Embed(title="Channel information", color=self.bot.color)

        e.add_field(name="Channel name", value=channel.name, inline=False)
        e.add_field(name="Channel ID", value=channel.id, inline=False)
        e.add_field(name="Mention", value=channel.mention, inline=False)

        if channel.category is not None:
            e.add_field(name="Category name", value=channel.category.name, inline=False)

        e.add_field(
            name="Channel Created", value=format_date(channel.created_at), inline=False
        )
        e.add_field(
            name="NSFW",
            value=f"{self.bot.yes} Yes" if channel.nsfw else f"{self.bot.no} No",
            inline=False,
        )

        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def vcinfo(self, ctx: Context, vc: discord.VoiceChannel):
        """Shows info about a voice channel."""

        e = discord.Embed(title="VC Information", color=self.bot.color)
        e.add_field(name="VC name", value=vc.name, inline=False)
        e.add_field(name="VC ID", value=vc.id, inline=False)
        e.add_field(name="VC bitrate", value=vc.bitrate, inline=False)
        e.add_field(name="Mention", value=vc.mention, inline=False)

        if vc.category is not None:
            e.add_field(name="Category name", value=vc.category.name, inline=False)

        e.add_field(name="VC Created", value=format_date(vc.created_at), inline=False)

        await ctx.send(embed=e)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.guild_only()
    async def roleinfo(self, ctx: Context, role: discord.Role):
        """
        Gives some info about the specified role.
        You can mention the role or give the name of it.
        """

        e = discord.Embed(title="Role Information", color=self.bot.color)
        e.add_field(name="Role name", value=role.name, inline=False)
        e.add_field(name="Role ID", value=role.id, inline=False)
        e.add_field(name="Mention", value=role.mention, inline=False)
        e.add_field(
            name="Role Created", value=format_date(role.created_at), inline=False
        )
        e.add_field(name="Role Color", value=role.color, inline=False)

        if role.mentionable:
            e.add_field(name="Mentionable", value=f"{self.bot.yes} Yes", inline=False)

        else:
            e.add_field(name="Mentionable", value=f"{self.bot.no} No", inline=False)

        await ctx.send(embed=e)

    def get_bot_uptime(self, *, brief=False):
        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = "{d} days, {h} hours, {m} minutes, and {s} seconds"

            else:
                fmt = "{h} hours, {m} minutes, and {s} seconds"

        else:
            fmt = "{h}h {m}m {s}s"
            if days:
                fmt = "{d}d " + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    @commands.command(aliases=["stats"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def about(self, ctx: Context):
        """Tells you information about the bot itself."""

        total_members = 0
        total_unique = len(self.bot.users)
        my_commands = [command for command in self.bot.walk_commands()]

        text = 0
        voice = 0
        guilds = 0

        for guild in self.bot.guilds:
            guilds += 1
            if guild.unavailable:
                continue

            total_members += guild.member_count or 0
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    text += 1

                elif isinstance(channel, discord.VoiceChannel):
                    voice += 1

        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

        dpy_version = discord.__version__
        dev = self.bot.get_user(710247495334232164)

        em = discord.Embed(color=self.bot.color)
        if dev and dev.avatar is not None:
            em.set_author(name=dev, icon_url=dev.avatar.url)

        em.title = "About"
        em.description = self.bot.description

        em.add_field(
            name="Users", value=f"{total_members} total\n{total_unique} unique"
        )

        em.add_field(
            name="Channels", value=f"{text + voice} total\n{text} text\n{voice} voice"
        )

        em.add_field(
            name="Process", value=f"{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU"
        )

        em.add_field(name="Guilds", value=guilds)

        em.add_field(name="Commands", value=len(my_commands))

        em.add_field(name="Uptime", value=self.get_bot_uptime(brief=True))

        if self.bot.user and self.bot.user.avatar is not None:
            em.set_thumbnail(url=self.bot.user.avatar.url)
        em.set_footer(
            text=f"Made with 💖 with discord.py v{dpy_version}",
            icon_url="http://i.imgur.com/5BFecvA.png",
        )

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def suggest(self, ctx: Context, *, suggestion):
        """
        Suggest some commands that should be included in bot.
        This command need not be used if you are in the support server.
        """

        await ctx.send(
            f"{self.bot.yes} {ctx.author.mention}, your suggestion has been recorded!"
        )
        channel = self.bot.get_channel(798259756803817545)

        em = discord.Embed(
            title="New Suggestion",
            description=f"> {suggestion}",
            color=discord.Color.green(),
            timestamp=ctx.message.created_at,
        )

        if ctx.author.avatar is not None:
            em.set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
            )

        msg = await channel.send(embed=em)  # type: ignore
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    # show perms
    async def say_permissions(self, ctx: Context, member, channel):
        permissions = channel.permissions_for(member)
        e = discord.Embed()
        allowed, denied = [], []
        for name, value in permissions:
            name = name.replace("_", " ").title()
            if value:
                allowed.append(name)

            else:
                denied.append(name)

        e.add_field(name="Allowed", value="\n".join(allowed))
        e.add_field(name="Denied", value="\n".join(denied))
        await ctx.send(embed=e)

    @commands.command(aliases=["perms"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def permissions(self, ctx: Context, *, member: discord.Member = None):  # type: ignore
        """Shows a member's permissions.
        If used in DM's, shows your permissions in a DM channel."""

        member = member or ctx.author
        channel = ctx.message.channel

        await self.say_permissions(ctx, member, channel)

    @commands.command(aliases=["botperms"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def botpermissions(self, ctx: Context):
        """Shows the bot's permissions."""

        channel = ctx.channel
        if ctx.message.guild is not None:
            member = ctx.message.guild.me

            await self.say_permissions(ctx, member, channel)

    @commands.command(aliases=["av"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def avatar(self, ctx: Context, member: Optional[Union[discord.Member, discord.User]]):  # type: ignore
        """
        Displays a user's avatar
        If no member is provided, returns your avatar.
        """

        if not member:
            member = ctx.author  # type: ignore

        em = discord.Embed(title=f"Avatar of {member.name}", color=self.bot.color)

        if member.avatar is not None:
            em.set_image(url=member.avatar.url)

        em.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def charinfo(self, ctx: Context, *, characters: str):
        """Shows you information about a number of characters.
        Only up to 15 characters at a time.
        """

        if len(characters) > 15:
            await ctx.send("Too many characters ({}/15)".format(len(characters)))
            return

        fmt = "`\\U{0:>08}`: {1} - {2} \N{EM DASH}"

        def to_string(c):
            digit = format(ord(c), "x")
            name = unicodedata.name(c, "Name not found.")
            return fmt.format(digit, name, c)

        await ctx.send("\n".join(map(to_string, characters)))


async def setup(bot):
    await bot.add_cog(Utility(bot))
