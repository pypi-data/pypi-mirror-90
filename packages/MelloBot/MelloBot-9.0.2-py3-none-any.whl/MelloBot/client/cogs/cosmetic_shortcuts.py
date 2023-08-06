import json, random, asyncio, aiofiles, fortnitepy
from MelloBot.client import Client
from fortnitepy.ext import commands
from MelloBot.utils import Character

class CosmeticShortcuts(commands.Cog):

    def __init__(self, client: Client):
        self.client = client

    def extract_variants(self, cosmetic: dict) -> list:
        variants = []
        if cosmetic['variants']:
            for variant in cosmetic['variants']:
                for option in variant['options']:
                    variants.append({'path':f"{cosmetic['path']}.{cosmetic['id']}",  'name':cosmetic['names']['en'],  'variants':[{'channel':variant['channel'],  'c':variant['channel'],  'variant':option['tag'],  'dE':0,  'item':cosmetic['backendType'],  'v':option['tag'],  'dE':0,  'item':cosmetic['backendType']}]})

        variants.append({'path':f"{cosmetic['path']}.{cosmetic['id']}",  'name':cosmetic['names']['en'],  'variants':[]})
        return variants

    def get_random_chapter1_default_cid(self) -> str:
        return random.choice(list(fortnitepy.DefaultCharactersChapter1)).name

    @commands.command()
    async def purpleskull(self, ctx: commands.Context):
        await self.client.party.me.set_outfit('CID_030_Athena_Commando_M_Halloween', variants=[{'dE':0,  'item':'AthenaCharacter',  'channel':'ClothingColor',  'c':'ClothingColor',  'variant':'Mat1',  'v':'Mat1'}])
        await ctx.send('Skin set to Skull Trooper with Purple Glow variant.')

    @commands.command()
    async def pinkghoul(self, ctx: commands.Context):
        await self.client.party.me.set_outfit('CID_029_Athena_Commando_F_Halloween', variants=[{'dE':0,  'item':'AthenaCharacter',  'channel':'Material',  'c':'Material',  'variant':'Mat3',  'v':'Mat3'}])
        await ctx.send('Skin set to Ghoul Trooper with Pink variant.')

    @commands.command()
    async def mintyelf(self, ctx: commands.Context):
        await self.client.party.me.set_outfit('CID_051_Athena_Commando_M_HolidayElf', variants=[{'dE':0,  'item':'AthenaCharacter',  'channel':'Material',  'c':'Material',  'variant':'Mat2',  'v':'Mat2'}])
        await ctx.send('Skin set to Elf with Minty variant.')

    @commands.command(aliases=['renegade'])
    async def checkeredrenegade(self, ctx: commands.Context):
        await self.client.party.me.set_outfit('CID_028_Athena_Commando_F', variants=[{'dE':0,  'item':'AthenaCharacter',  'channel':'Material',  'c':'Material',  'variant':'Mat2',  'v':'Mat2'}])
        await ctx.send('Skin set to Renegade Raider with Checkered variant.')

    @commands.command()
    async def hologram(self, ctx: commands.Context):
        await self.client.party.me.set_outfit('CID_VIP_Athena_Commando_M_GalileoGondola_SG')
        await ctx.send('Skin set to Hologram (Star Wars).')

    @commands.command()
    async def ninja(self, ctx: commands.Context):
        await self.client.party.me.set_outfit('CID_605_Athena_Commando_M_TourBus')
        await ctx.send('Skin set to Ninja.')

    @commands.command(aliases=['nohatrecon', 'reconexpert', 'reconnohat'])
    async def hatlessrecon(self, ctx: commands.Context):
        await self.client.party.me.set_outfit('CID_022_Athena_Commando_F', variants=[{'dE':0,  'item':'AthenaCharacter',  'channel':'Parts',  'c':'Parts',  'variant':'Stage2',  'v':'Stage2'}])
        await ctx.send('Skin set to Recon Expert with No Hat variant.')

    @commands.command(aliases=['noskin', 'recruit'])
    async def olddefault(self, ctx: commands.Context):
        cid = self.get_random_chapter1_default_cid()
        await self.client.party.me.set_outfit(cid)
        await ctx.send(f"Skin set to old default recruit ({cid})")

    @commands.command(aliases=['iron_man'])
    async def ironman(self, ctx: commands.Context):
        await self.client.party.me.set_outfit('CID_843_Athena_Commando_M_HightowerTomato_Casual', variants=[{'dE':0,  'item':'AthenaCharacter',  'channel':'Progressive',  'c':'Progressive',  'variant':'Stage2',  'v':'Stage2'}])
        await ctx.send('Skin set to Iron Man.')

    @commands.command()
    async def purpleportal(self, ctx: commands.Context) -> None:
        await self.client.party.me.set_backpack('BID_105_GhostPortal', variants=[{'dE':0,  'item':'AthenaCharacter',  'channel':'Parts',  'c':'Parts',  'variant':'Stage2',  'v':'Stage2'}, {'dE':0,  'item':'AthenaBackpack',  'channel':'Particle',  'c':'Particle',  'variant':'Particle1',  'v':'Particle1'}])
        await ctx.send('Backpack set to Ghost Portal with Purple variant.')

    @commands.group()
    async def random(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('TIP: You can also add emote/skin/backpack to only randomize this cosmetic.')
            cosmetics = json.loads(await (await aiofiles.open('assets/cosmetics.json', mode='r')).read())
            all_skins = []
            all_backpacks = []
            all_emotes = []
            for cosmetic in cosmetics:
                if cosmetic['backendType'].lower() == 'athenacharacter':
                    all_skins.extend(self.extract_variants(cosmetic))
                elif cosmetic['backendType'].lower() == 'athenabackpack':
                    all_backpacks.extend(self.extract_variants(cosmetic))
                else:
                    if cosmetic['backendType'].lower() == 'athenadance':
                        all_emotes.append({'path':f"{cosmetic['path']}.{cosmetic['id']}",  'name':cosmetic['names']['en']})
                    skin = random.choice(all_skins)
                    await self.client.party.me.set_outfit(asset=(skin['path']), variants=(skin['variants']))
                    backpack = random.choice(all_backpacks)
                    await self.client.party.me.set_backpack(asset=(backpack['path']), variants=(backpack['variants']))
                    emote = random.choice(all_emotes)

            await self.client.party.me.clear_emote()
            await self.client.party.me.set_emote(asset=(emote['path']))
            await ctx.send(f"Randomized all Cosmetics, (Outfit: {skin['name']}, Backpack: {backpack['name']}, Emote: {emote['name']}).")

    @random.command(name='skin', aliases=['outfit', 'character'])
    async def random_skin(self, ctx: commands.Context):
        cosmetics = json.loads(await (await aiofiles.open('assets/cosmetics.json', mode='r')).read())
        all_skins = [self.extract_variants(cosmetic) for cosmetic in cosmetics if cosmetic['backendType'].lower() == 'athenacharacter']
        skin = random.choice(all_skins)
        await self.client.party.me.set_outfit(asset=(skin['path']), variants=(skin['variants']))
        await ctx.send(f"Skin randomly set to {skin['name']}.")

    @random.command(aliases=['emote', 'dance'])
    async def random_emote(self, ctx: commands.Context):
        cosmetics = json.loads(await (await aiofiles.open('assets/cosmetics.json', mode='r')).read())
        all_emotes = [{'path':f"{cosmetic['path']}.{cosmetic['id']}",  'name':cosmetic['names']['en']} for cosmetic in cosmetics if cosmetic['backendType'].lower() == 'athenadance']
        emote = random.choice(all_emotes)
        await self.client.party.me.clear_emote()
        await self.client.party.me.set_emote(asset=(emote['path']))
        await ctx.send(f"Emote randomly set to {emote['name']}.")

    @random.command(aliases=['backbling', 'backpack'])
    async def random_backpack(self, ctx: commands.Context):
        cosmetics = json.loads(await (await aiofiles.open('assets/cosmetics.json', mode='r')).read())
        all_backpacks = [self.extract_variants(cosmetic) for cosmetic in cosmetics if cosmetic['backendType'].lower() == 'athenabackpack']
        backpack = random.choice(all_backpacks)
        await self.client.party.me.set_backpack(asset=(backpack['path']), variants=(backpack['variants']))
        await ctx.send(f"Backpack randomly set to {backpack['name']}.")

    @random.command(name='og')
    async def random_og(self, ctx: commands.Context):
        party = self.client.party
        characters = [
         party.me.set_outfit('cid_017_athena_commando_m'),
         party.me.set_outfit('cid_028_athena_commando_f', variants=party.me.create_variants(material=2)),
         party.me.set_outfit('cid_029_athena_commando_f_halloween', variants=party.me.create_variants(material=3)),
         party.me.set_outfit('cid_030_athena_commando_m_halloween', variants=party.me.create_variants(clothing_color=1)),
         party.me.set_outfit('cid_028_athena_commando_f', variants=party.me.create_variants(material=2)),
         party.me.set_outfit('cid_029_athena_commando_f_halloween', variants=party.me.create_variants(material=3)),
         party.me.set_outfit('cid_030_athena_commando_m_halloween', variants=party.me.create_variants(clothing_color=1))]
        await random.choice(characters)

    @commands.group()
    async def new(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('Please add skin, backpack or emote.')

    @new.command(aliases=['outfit', 'character', 'skin'])
    async def new_skin(self, ctx: commands.Context):
        new_cosmetics = await self.client.session.get('https://benbotfn.tk/api/v1/newCosmetics')
        if new_cosmetics.status == 200:
            new_cosmetics = await new_cosmetics.json()
            new_skins = [cosmetic for cosmetic in new_cosmetics['items'] if cosmetic['backendType'].lower() == 'athenacharacter']
            if len(new_skins) == 0:
                return await ctx.send('There are no new skins!')
            skin = random.choice(new_skins)
            await self.client.party.me.set_outfit(asset=f"{skin['path'].replace('FortniteGame/Content/', '/Game/')}.{skin['id']}")
            check_variants = f", check the variants with !variants skin {skin['name']}."
            await ctx.send(f"'Skin set to the leaked Outfit {skin['name']}{check_variants if skin['variants'] else ''}.'")

    @new.command(aliases=['emote', 'dance'])
    async def new_emote(self, ctx: commands.Context):
        new_cosmetics = await self.client.session.get('https://benbotfn.tk/api/v1/newCosmetics')
        if new_cosmetics.status == 200:
            new_cosmetics = await new_cosmetics.json()
            new_emotes = [cosmetic for cosmetic in new_cosmetics['items'] if cosmetic['backendType'].lower() == 'athenadance']
            if len(new_emotes) == 0:
                await ctx.send('There are no new emotes!')
                return
            emotes = random.choice(new_emotes)
            await self.client.party.me.clear_emote()
            await self.client.party.me.set_emote(asset=f"{emotes['path'].replace('FortniteGame/Content/', '/Game/')}.{emotes['id']}")
            await ctx.send(self.client.languages.get_string('cosmetic_shortcuts', 'new_emote', 'en').format(emotes['name']))

    @new.command(aliases=['backpack', 'backbling'])
    async def new_backpack(self, ctx: commands.Context):
        new_cosmetics = await self.client.session.get('https://benbotfn.tk/api/v1/newCosmetics')
        if new_cosmetics.status == 200:
            new_cosmetics = await new_cosmetics.json()
            new_backpack = [cosmetic for cosmetic in new_cosmetics['items'] if cosmetic['backendType'].lower() == 'athenabackpack']
            if len(new_backpack) == 0:
                return await ctx.send('There are no new backpacks!')
            backpack = random.choice(new_backpack)
            await self.client.party.me.set_backpack(asset=f"{backpack['path'].replace('FortniteGame/Content/', '/Game/')}.{backpack['id']}")
            check_variants = f", check the variants with !variants skin {backpack['name']}."
            await ctx.send(f"Backpack set to the leaked Backpack {backpack['name']}{check_variants if backpack['variants'] else ''}.")

    @new.command(aliases=['outfits', 'characters', 'skins'])
    @commands.max_concurrency(1)
    @commands.cooldown(1, 60)
    async def new_skins(self, ctx: commands.Context):
        new_cosmetics = await self.client.session.get('https://benbotfn.tk/api/v1/newCosmetics')
        if new_cosmetics.status == 200:
            new_cosmetics = await new_cosmetics.json()
            new_skins = [cosmetic for cosmetic in new_cosmetics['items'] if cosmetic['backendType'].lower() == 'athenacharacter']
            if len(new_skins) == 0:
                return await ctx.send('There are no new skins!')
            i = 0
            for skin in new_skins:
                await self.client.party.me.set_outfit(asset=f"{skin['path'].replace('FortniteGame/Content/', '/Game/')}.{skin['id']}")
                check_variants = f", check the variants with !variants skin {skin['name']}."
                await ctx.send(f"Skin set to the leaked Outfit {skin['name']}{check_variants if skin['variants'] else ''}.")
                i += 1
                if i == len(new_skins):
                    break
                await asyncio.sleep(3)

            await ctx.send('Done showing you the new Outfits!')

    @new.command(aliases=['emotes', 'dances'])
    @commands.max_concurrency(1)
    @commands.cooldown(1, 60)
    async def new_emotes(self, ctx: commands.Context):
        new_cosmetics = await self.client.session.get('https://benbotfn.tk/api/v1/newCosmetics')
        if new_cosmetics.status == 200:
            new_cosmetics = await new_cosmetics.json()
            new_emotes = [cosmetic for cosmetic in new_cosmetics['items'] if cosmetic['backendType'].lower() == 'athenadance']
            if len(new_emotes) == 0:
                await ctx.send('There are no new emotes!')
                return
            i = 0
            for emote in new_emotes:
                await self.client.party.me.clear_emote()
                await self.client.party.me.set_emote(asset=f"{emote['path'].replace('FortniteGame/Content/', '/Game/')}.{emote['id']}")
                await ctx.send(f"Emote set to the leaked Emote {emote['name']}.")
                i += 1
                if i == len(new_emotes):
                    break
                await asyncio.sleep(5)

            await ctx.send('Done showing you the new Emotes!')

    @new.command(aliases=['backpacks', 'backblings'])
    @commands.max_concurrency(1)
    @commands.cooldown(1, 60)
    async def new_backpacks(self, ctx: commands.Context):
        new_cosmetics = await self.client.session.get('https://benbotfn.tk/api/v1/newCosmetics')
        if new_cosmetics.status == 200:
            new_cosmetics = await new_cosmetics.json()
            new_backpack = [cosmetic for cosmetic in new_cosmetics['items'] if cosmetic['backendType'].lower() == 'athenabackpack']
            if len(new_backpack) == 0:
                await ctx.send('There are no new backpacks!')
                return
            i = 0
            for backpack in new_backpack:
                backpack = random.choice(new_backpack)
                await self.client.party.me.set_backpack(asset=f"{backpack['path'].replace('FortniteGame/Content/', '/Game/')}.{backpack['id']}")
                check_variants = f", check the variants with !variants backpack {backpack['name']}."
                await ctx.send(f"Backpack set to the leaked Backpack {backpack['name']}{check_variants if backpack['variants'] else ''}.")
                i += 1
                if i == len(new_backpack):
                    break
                await asyncio.sleep(3)

            await ctx.send('Done showing you the new Backpacks!')


def extension_setup(client: Client):
    client.add_cog(CosmeticShortcuts(client))