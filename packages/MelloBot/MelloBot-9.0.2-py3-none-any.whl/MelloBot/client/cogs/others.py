# Embedded file name: <EZFNSetup-4.0.8>/EZFNSetup/client/cogs/others.py
# Compiled at: 2020-10-25 22:13:51
# Size of source mod 2**32: 3088 bytes
import fortnitepy
from typing import Union
from MelloBot.client import Client
from fortnitepy.ext.commands import Cog, Context, command

class Others(Cog):

    def __init__(self, client: Client):
        self.client = client

    @command()
    async def level(self, ctx: Context, *, level: int):
        await self.client.party.me.set_banner(season_level=level)
        await ctx.send(f"Level set to {level}.")

    @command(aliases=['bp', 'battle_pass'])
    async def battlepass(self, ctx: Context, level: int=893, self_boost_xp: int=2679, friend_boost_xp: int=3895, has_purchased: bool=True):
        await self.client.party.me.set_battlepass_info(level=level, self_boost_xp=self_boost_xp, friend_boost_xp=friend_boost_xp, has_purchased=has_purchased)
        await ctx.send(f"Set battle pass (level: {level}, self_boost_xp: {self_boost_xp}, friend_boost_xp: {friend_boost_xp}, has_purchased: {has_purchased}).")

    @command(aliases=['description'])
    async def status(self, ctx: Context, *, status: str):
        await self.client.send_presence(status, to=(ctx.author.jid))
        await ctx.send(f"Status set to {status}.")

    @command(aliases=['friend_count'])
    async def friends(self, ctx: Context):
        await ctx.send(f"I have {len(self.client.friends)} friends and {sum((1 for friend in self.client.friends if friend.is_online()))} of them are online.")

    @command(aliases=['add'])
    async def friend(self, ctx: Context, *, display_name: Union[(str, None)]=None):
        if display_name is None:
            display_name = ctx.author.display_name
        else:
            user = await self.client.fetch_user(display_name)
            if user is None:
                await ctx.send(f"Can not find any user with the name {display_name}.")
            if self.client.has_friend(user.id):
                return await ctx.send(f"{user.display_name} is already my friend.")
            try:
                await self.client.add_friend(user.id)
                await ctx.send(f"Sent a friend request to {user.display_name}.")
            except fortnitepy.FriendshipRequestAlreadySent:
                await ctx.send(f"Friend request already sent to {user.display_name}.")
            except fortnitepy.MaxFriendshipsExceeded:
                await ctx.send('Sorry, I can not add more friends, check some other bots at https://ezfn.dev/bots')
            except fortnitepy.Forbidden:
                await ctx.send(f"Failed to send a friend request to {user.display_name} due to his settings.")
            except fortnitepy.InviteeMaxFriendshipsExceeded:
                await ctx.send(f"Failed to send a friend request to {user.display_name}, his incoming friendships limit is exceeded.")
            except Exception as e:
                try:
                    await ctx.send(f"Failed to parse error: {str(e)}")
                finally:
                    e = None
                    del e

    @command()
    async def help(self, ctx: Context):
        await ctx.send('For a list of commands check https://ezfn.dev/lobbybot/docs or join my discod https://ezfn.dev/discord to make your own bot.')


def extension_setup(client: Client):
    client.add_cog(Others(client))
# okay decompiling others.pyc