from typing import Union
from MelloBot.client import Client
from MelloBot.utils import Character, Backpack, Pickaxe, Pet, Dance, Emoji
from fortnitepy.ext.commands import Cog, Context, command, group

class Cosmetics(Cog):

    def __init__(self, client: Client):
        self.client = client

    @command(aliases=['outfit', 'character'])
    async def skin(self, ctx: Context, *, skin: Character):
        await self.client.party.me.set_outfit(asset=(skin['path']), variants=(skin['parsed_variants']))
        await ctx.send(f"Skin set to {skin['names']['en']}.")

    @command(aliases=['backbling'])
    async def backpack(self, ctx: Context, *, backpack: Backpack):
        await self.client.party.me.set_backpack(asset=(backpack['path']), variants=(backpack['parsed_variants']))
        await ctx.send(f"Backpack set to {backpack['names']['en']}.")

    @command()
    async def pickaxe(self, ctx: Context, *, pickaxe: Pickaxe):
        await self.client.party.me.set_pickaxe(asset=(pickaxe['path']), variants=(pickaxe['parsed_variants']))
        await ctx.send(f"Pickaxe set to {pickaxe['names']['en']}.")

    @command()
    async def pet(self, ctx: Context, *, pet: Pet):
        await self.client.party.me.set_pet(asset=(pet['path']), variants=(pet['parsed_variants']))
        await ctx.send(f"Pet set to {pet['names']['en']}.")

    @command(aliases=['dance'])
    async def emote(self, ctx: Context, *, emote: Dance):
        await self.client.party.me.clear_emote()
        await self.client.party.me.set_emote(asset=(emote['path']), run_for=(emote['run_for']))
        await ctx.send(f"Emote set to {emote['names']['en']} for {emote['run_for'] if emote['run_for'] else 'unlimited'} seconds.")

    @command()
    async def emoji(self, ctx: Context, *, emoji: Emoji):
        await self.client.party.me.clear_emote()
        await self.client.party.me.set_emoji(asset=(emoji['path']), run_for=(emoji['run_for']))
        await ctx.send(f"Emoji set to {emoji['names']['en']} for {emoji['run_for'] if emoji['run_for'] else 'unlimited'} seconds.")

    @command()
    async def point(self, ctx: Context, *, pickaxe: Union[(Pickaxe, None)]=None):
        await self.client.party.me.clear_emote()
        if pickaxe is None:
            await self.client.party.me.set_emote(asset='EID_IceKing')
            await ctx.send('Point it Out played.')
        else:
            await self.client.party.me.set_pickaxe(asset=(pickaxe['path']), variants=(pickaxe['parsed_variants']))
            await self.client.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f"Pickaxe set to {pickaxe['names']['en']} & Point it Out played.")

    @command()
    async def ghost(self, context: Context, *, content: str):
        skin = Character()
        skin = await skin.convert(context, f"{content} --STYLE=GHOST")
        if not skin['parsed_variants']:
            return await context.send(f"{skin['names']['en']} does not have a Ghost variant.")
        if 'progressive' not in [v['channel'].lower() for v in skin['parsed_variants']]:
            return await context.send(f"{skin['names']['en']} does not have a Ghost variant.")
        await self.client.party.me.set_outfit((skin['id']), variants=(skin['parsed_variants']))
        await context.send(f"Skin set to {skin['names']['en']} with Ghost variant.")

    @command()
    async def shadow(self, context: Context, *, content: str):
        skin = Character()
        skin = await skin.convert(context, f"{content} --STYLE=SHADOW")
        if not skin['parsed_variants']:
            return await context.send(f"{skin['names']['en']} does not have a Shadow variant.")
        if 'progressive' not in [v['channel'].lower() for v in skin['parsed_variants']]:
            return await context.send(f"{skin['names']['en']} does not have a Shadow variant.")
        await self.client.party.me.set_outfit((skin['id']), variants=(skin['parsed_variants']))
        await context.send(f"Skin set to {skin['names']['en']} with Shadow variant.")

    @command()
    async def golden(self, context: Context, *, content: str):
        skin = Character()
        skin = await skin.convert(context, f"{content} --STYLE=GOLDEN AGENT")
        if not skin['parsed_variants']:
            return await context.send(f"{skin['names']['en']} does not have a Golden Agent variant.")
        if 'progressive' not in [v['channel'].lower() for v in skin['parsed_variants']]:
            return await context.send(f"{skin['names']['en']} does not have a Golden Agent variant.")
        await self.client.party.me.set_outfit((skin['id']), variants=(skin['parsed_variants']), enlightenment=(int(skin['season']), 1000))
        await context.send(f"Skin set to {skin['names']['en']} with Golden Agent variant.")

    @group()
    async def clear(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('What do you want to clear?\nPlease add emote, backpack or match.')

    @clear.command(aliases=['emote', 'dance'])
    async def clear_emote(self, ctx: Context):
        await self.client.party.me.clear_emote()
        await ctx.send('Stopped dancing.')

    @clear.command(aliases=['backpack', 'backbling', 'pet'])
    async def clear_backpack(self, ctx: Context):
        await self.client.party.me.clear_backpack()
        await self.client.party.me.clear_pet()
        await ctx.send('Removed Backpack.')

    @clear.command(aliases=['match', 'game'])
    async def clear_match(self, ctx: Context):
        await self.client.party.me.clear_in_match()
        await ctx.send('Set state to lobby.')

    @group()
    async def variants(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('No cosmetic type found.\nPlease add skin, backpack, pet or pickaxe.')

    @variants.command(aliases=['outfit', 'skin', 'character'])
    async def variants_skin(self, ctx: Context, *, skin: Character):
        variants = ''
        for v in skin['variants']:
            variants += '\n' + f"{v['types']['en']}:"
            for option in v['options']:
                variants += '\n   -' + option['names']['en']

            await ctx.send(f"Variants: {variants}")

    @variants.command(aliases=['pickaxe'])
    async def variants_pickaxe(self, ctx: Context, *, pickaxe: Pickaxe):
        variants = ''
        for v in pickaxe['variants']:
            variants += '\n' + f"{v['types']['en']}:"
            for option in v['options']:
                variants += '\n   -' + option['names']['en']

            await ctx.send(f"Variants: {variants}")

    @variants.command(aliases=['backpack', 'backbling'])
    async def variants_backpack(self, ctx: Context, *, backpack: Backpack):
        variants = ''
        for v in backpack['variants']:
            variants += '\n' + f"{v['types']['en']}:"
            for option in v['options']:
                variants += '\n   -' + option['names']['en']

            await ctx.send(f"Variants: {variants}")

    @variants.command(aliases=['pet'])
    async def variants_pet(self, ctx: Context, *, pet: Pet):
        variants = ''
        for v in pet['variants']:
            variants += '\n' + f"{v['types']['en']}:"
            for option in v['options']:
                variants += '\n   -' + option['names']['en']

            await ctx.send(f"Variants: {variants}")


def extension_setup(client: Client):
    client.add_cog(Cosmetics(client))
# okay decompiling cosmetics.pyc