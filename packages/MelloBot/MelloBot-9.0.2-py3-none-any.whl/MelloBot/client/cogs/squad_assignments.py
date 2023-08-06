import asyncio, fortnitepy
from typing import Union
from MelloBot.client import Client
from fortnitepy.ext.commands import Cog, Context, command

class Squad_Assignments(Cog):

    def __init__(self, client: Client):
        self.client = client
        self.loop = client.loop
        self.client.visible = set([])
        self.client.invisible = set([])

    def get_party_member(self, display_name: str) -> fortnitepy.PartyMember:
        for member in self.client.party.members:
            if member.display_name == display_name or member.id == display_name:
                return member

    @command(aliases=['invisible'])
    async def hide(self, ctx: Context, *, party_member: str=None):
        if not self.client.party.me.leader:
            return await ctx.send('Party leader permission needed.')
            if party_member == 'all':
                self.client.settings['party']['hide_all_members'] = True
                self.client.visible.clear()
                self.client.invisible.clear()
                await self.client.party.refresh_squad_assignments()
                await ctx.send('All members are now visible.')
            if party_member:
                party_member = self.get_party_member(party_member)
                if not party_member:
                    return await ctx.send(f"{party_member.display_name} not found!")
        else:
            party_member = ctx.author
        if party_member.id in self.client.visible:
            self.client.visible.remove(party_member.id)
        if party_member.id not in self.client.invisible:
            self.client.invisible.add(party_member.id)
        await self.client.party.refresh_squad_assignments()
        await ctx.send(f"Hid {party_member.display_name}.")

    @command(aliases=['unhide', 'visible'])
    async def show(self, ctx: Context, *, party_member: str=None):
        if not self.client.party.me.leader:
            return await ctx.send('Party leader permission needed.')
            if party_member == 'all':
                self.client.settings['party']['hide_all_members'] = False
                self.client.visible.clear()
                self.client.invisible.clear()
                await self.client.party.refresh_squad_assignments()
                return await ctx.send('All members are not invisible.')
            if party_member:
                party_member = self.get_party_member(party_member)
                if not party_member:
                    return await ctx.send(f"{party_member.display_name} not found!")
        else:
            party_member = ctx.author
        if party_member.id in self.client.invisible:
            self.client.invisible.remove(party_member.id)
        if party_member.id not in self.client.visible:
            self.client.visible.add(party_member.id)
        await self.client.party.refresh_squad_assignments()
        await ctx.send(f"{party_member.display_name} is now visible again.")

    @command(aliases=['spots', 'member_positions'])
    async def positions(self, ctx: Context):
        await ctx.send('\n '.join([f"{idx}.{member.display_name}" for idx, member in enumerate(self.client.party.members.values())]))


def extension_setup(client: Client):
    client.add_cog(Squad_Assignments(client))
# okay decompiling squad_assignments.pyc