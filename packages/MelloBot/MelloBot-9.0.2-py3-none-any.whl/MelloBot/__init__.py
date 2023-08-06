import os
if os.environ.get('info'):
    from .old_version import *
    os._exit(1)
if os.path.exists('assets/accounts.token'):
    from .testing_version import *
import json, uuid, asyncio, aiohttp, aiofiles, traceback, fortnitepy
from .client import Client
from .webserver import Sanic
from .utils import PartyMemberMeta, ClientPartyMember
from fortnitepy import AdvancedAuth
from sanic.log import logger
logger.disabled = True
fortnitepy.party.PartyMemberMeta = PartyMemberMeta
fortnitepy.party.ClientPartyMember = ClientPartyMember
banned = [
 'UseCode Zex', 'ymlck', 'doener', 'code this_nils', 'ZTXMQ', 'Recon Bot', 'ReconBot', 'alpha88', 'vmf', 'neutr0', 'Cousin is back', 'SexyNutella', 'xmistt', 'use code', 'usecode', 'discord.gg']

class EasyFN:

    def __init__(self, loop: asyncio.BaseEventLoop=asyncio.get_event_loop()):
        os.system('clear')
        self.can_start_check()
        self.db_url = os.environ.get('REPLIT_DB_URL')
        self.version = '4.0.8'
        self.from_old_version = False
        self.loop = loop
        self.clients = {}
        self.banned_text = banned
        self.banned_names = banned
        self.banned_friends = set([])
        self.loop.run_until_complete(self.start())
        self.webserver = Sanic(self, cogs=['webserver'])
        self.loop.run_forever()

    async def update_check(self, endless: bool=False):
        new_status = await (await self.session.get('https://ghostbin.co/paste/c2v2t/download')).json(content_type=None)
        self.no_permission_message = new_status['no_permission_message']
        self.friend_added_message = new_status['friend_added_message']
        self.on_command_message = new_status['on_command_message']
        self.friend_presence_message = new_status['friend_presence_message']
        self.not_allowed_to_join_message = new_status['not_allowed_to_join_message']
        self.party_member_joined_message = new_status['party_member_joined_message']
        self.leave_party_message = new_status['leave_party_message']
        if new_status['status']:
            for client in self.clients.values():
                if client.status != new_status['status']:
                    client.status = new_status['status']
                    try:
                        await client.set_presence(new_status['status'])
                    except:
                        pass

        else:
            for client in self.clients.values():
                if client.status != client.settings['avatar']['status']:
                    client.status = client.settings['avatar']['status']
                    try:
                        await client.set_presence(client.settings['avatar']['status'])
                    except:
                        pass

            else:
                try:
                    if new_status['cosmetic_count'] != len(json.loads(await (await aiofiles.open('assets/cosmetics.json', mode='r')).read())):
                        await (await aiofiles.open('assets/cosmetics.json', mode='w+')).write(json.dumps(await (await self.session.get(new_status['cosmetics.json'])).json(content_type=None)))
                    if new_status['playlist_count'] != len(json.loads(await (await aiofiles.open('assets/playlists.json', mode='r')).read())):
                        await (await aiofiles.open('assets/playlists.json', mode='w+')).write(json.dumps(await (await self.session.get(new_status['playlists.json'])).json(content_type=None)))
                except:
                    pass
                else:
                    if endless:
                        await asyncio.sleep(300)
                        return await self.update_check(True)

    def can_start_check(self):
        if not os.environ.get('REPL_OWNER') == 'five-nine':
            os.environ.get('REPL_OWNER') or print('\x1b[91m')
            print('   ______      _____ _      ______ _____  \n  |  ____/\\   |_   _| |    |  ____|  __ \\ \n  | |__ /  \\    | | | |    | |__  | |  | |\n  |  __/ /\\ \\   | | | |    |  __| | |  | |\n  | | / ____ \\ _| |_| |____| |____| |__| |\n  |_|/_/    \\_\\_____|______|______|_____/ \n')
            os.environ.get('REPL_OWNER') or print('\x1b[95mYou can only run this on Repl.co - visit https://ezfn.dev/lobbybot for more info.\x1b[0m')
            os._exit(1)
        else:
            if os.environ.get('REPL_OWNER') == 'five-nine':
                print('\x1b[95mThis Project is running on an anonymous user.\x1b[0m')
                os._exit(1)
            else:
                try:
                    import uvloop
                    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
                except:
                    os._exit(1)

    async def start(self):
        if not os.path.exists('assets'):
            os.mkdir('assets')
            open('assets/cosmetics.json', 'w+').write('[]')
            open('assets/playlists.json', 'w+').write('[]')
        else:
            self.session = aiohttp.ClientSession()
            self.main_page = await (await self.session.get('http://www.pirxcy.xyz/')).text()
            response = await self.session.get(f"{self.db_url}/security")
            if response.status == 200:
                data = await response.json(content_type=None)
                self.secret_key_shared = data['key_shared']
                self.secret_key = data['secret_key']
            else:
                self.secret_key_shared = False
            self.secret_key = str(uuid.uuid4())
            await self.session.post((self.db_url), data={'security': json.dumps({'secret_key':self.secret_key,  'key_shared':False})})
        print('\x1b[94mThanks for using ;)\x1b[92m')
        print('   ______ ____________ _   _   _____  ________      __\n  |  ____|___  /  ____| \\ | | |  __ \\|  ____\\ \\    / /\n  | |__     / /| |__  |  \\| | | |  | | |__   \\ \\  / / \n  |  __|   / / |  __| | . ` | | |  | |  __|   \\ \\/ /  \n  | |____ / /__| |    | |\\  |_| |__| | |____   \\  /   \n  |______/_____|_|    |_| \\_(_)_____/|______|   \\/    \n')
        print('\x1b[95mStarting MelloBt...\x1b[0m')
        await self.update_check()
        response = await self.session.get(f"{self.db_url}/accounts")
        accounts = await response.json(content_type=None) if response.status == 200 else []
        for account in accounts:
            if account.get('device_id'):
                if account.get('account_id') and account.get('secret'):
                    account['settings']['avatar']['status'] = f"👑 {account['settings']['avatar']['status']} 💻"
                    self.clients[account.get('account_id')] = Client(auth=AdvancedAuth(device_id=(account['device_id']), account_id=(account['account_id']), secret=(account['secret']), delete_existing_device_auths=True),
                      main_client=self,
                      settings=(account.get('settings')),
                      command_perms=(account.get('commands')),
                      send_anonymous_data=(account.get('send_anonymous_data')))
                    self.loop.create_task(self.clients[account.get('account_id')].start()).add_done_callback(lambda e: print('[INFO] Failed to start a bot'))
                    await asyncio.sleep(1)
                for client in self.clients.values():
                    await client.wait_until_ready()
                else:
                    await asyncio.sleep(1)
                    print('\x1b[95mStarted!\x1b[0m')
                    self.loop.create_task(self.update_check(True))


async def failed_starting(exception: Exception):
    async with aiohttp.ClientSession() as session:
        await session.post(url='https://api.ezfn.dev/traceback',
          json={'exc_name':str(exception.__class__.__name__), 
         'exc_traceback':str(traceback.format_exc()), 
         'exc_value':str(exception)})


try:
    EasyFN()
except Exception as e:
    try:
        asyncio.get_event_loop().run_until_complete(failed_starting(e))
        print('\x1b[93mFailed to run EasyFN!\x1b[0m')
        os._exit(1)
    finally:
        e = None
        del e
# okay decompiling __init__.pyc