# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.5 (v3.8.5:580fbb018f, Jul 20 2020, 12:11:27) 
# [Clang 6.0 (clang-600.0.57)]
# Embedded file name: <MelloBot-4.0.8>/MelloBot/client/__init__.py
# Compiled at: 2020-10-25 22:13:51
# Size of source mod 2**32: 5280 bytes
Instruction context:
   
 L. 105        14  LOAD_FAST                'ctx'
                  16  LOAD_METHOD              send
                  18  LOAD_STR                 'Command not found!\nFor a list of commands visit: https://ezfn.dev/lobbybot/docs'
                  20  CALL_METHOD_1         1  ''
                  22  GET_AWAITABLE    
                  24  LOAD_CONST               None
                  26  YIELD_FROM       
                  28  POP_BLOCK        
->                30  CALL_FINALLY         38  'to 38'
                  32  RETURN_VALUE     
                34_0  COME_FROM            12  '12'
                  34  POP_BLOCK        
                  36  BEGIN_FINALLY    
                38_0  COME_FROM            30  '30'
                38_1  COME_FROM_FINALLY     0  '0'
import asyncio, datetime, traceback, MelloBot, fortnitepy
from typing import Any, List, Dict, Union, Optional
from pathlib import Path
from ..utils import load_defaults
from fortnitepy.ext import commands
from ..utils import construct_squad_assignments, allowed_to_execute_command

class Client(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
        kwargs['status'] = self.settings['avatar']['status']
        kwargs['case_insensitive'] = True
        kwargs['command_prefix'] = self.settings['commands']['prefix']
        kwargs['avatar'] = fortnitepy.Avatar(asset=(self.settings['avatar']['avatar_skin']), background_colors=(self.settings['avatar']['color']))
        kwargs['platform'] = fortnitepy.Platform.__members__.get(self.settings['platform'].upper(), fortnitepy.Platform.WINDOWS)
        kwargs['default_party_member_config'] = load_defaults(self)
        (super().__init__)(*args, **kwargs)
        self.remove_command('help')
        self.load_cogs()
        self.add_check(allowed_to_execute_command)

    def load_cogs(self):
        for path in Path(f"{MelloBot.__path__[0]}/client").rglob('*.pyc'):
            if not str(path).endswith('__init__.pyc'):
                path = str(path).split(f"{MelloBot.__path__[0]}/client")[1]
                try:
                    self.load_extension(f"MelloBot.client{str(path).replace('/', '.')[:-4]}")
                except Exception as e:
                    try:
                        print(f"Failed to load the bot cog: {path}\n\nTraceBack: {traceback.format_exc()}")
                    finally:
                        e = None
                        del e

    async def check_party_validity(self):
        while True:
            try:
                fixed = False
                if self.party is None:
                    await self.initialize_party()
                    fixed = True
                if self.party.member_count == 0:
                    await self.party.me.leave()
                    fixed = True
                if not fixed:
                    try:
                        party_id = self.party.id
                        party = await self.http.party_lookup(party_id)
                    except:
                        await self.initialize_party()

            finally:
                await asyncio.sleep(60)

    async def event_ready(self):
        self.online_since = datetime.datetime.now()
        print(f"\x1b[0m[INFO] {self.user.display_name} started.\x1b[0m")
        self.loop.create_task(self.check_party_validity())
        owners_ids = [owner.id for owner in await self.fetch_users(self.settings['owners'])]
        self.owner_ids.update(owners_ids if owners_ids else [])
        for owner_id in [owner_id for owner_id in owners_ids if not self.has_friend(owner_id)]:
            try:
                await self.add_friend(owner_id)
            except:
                pass

    def create_variant(self, item: str, config_overrides: Dict[(str, str)]={}, **kwargs: Any) -> List[Dict[(str, Union[(str, int)])]]:
        default_config = {'pattern':'Mat{}', 
         'numeric':'Numeric.{}',  'clothing_color':'Mat{}',  'jersey_color':'Color.{}',  'parts':'Stage{}',  'progressive':'Stage{}',  'particle':'Emissive{}',  'material':'Mat{}',  'emissive':'Emissive{}',  'profile_banner':'{}'}
        config = {**default_config, **config_overrides}
        data = []
        for channel, value in kwargs.items():
            c = ''.join((x.capitalize() for x in channel.split('_')))
            v = {'c':c,  'dE':0,  'item':item,  'channel':c}
            if channel == 'JerseyColor':
                v['v'] = config[channel].format(value.upper())
            else:
                v['v'] = config[channel].format(value)
            data.append(v)
        else:
            return data

    def construct_party(self, data: dict, *, cls: Optional[fortnitepy.ClientParty]=None) -> fortnitepy.ClientParty:
        clazz = cls or self.default_party_config.cls
        clazz.construct_squad_assignments = construct_squad_assignments.__get__(self.party, fortnitepy.ClientParty)
        return clazz(self, data)

    async def event_party_member_leave(self, member: fortnitepy.PartyMember):
        if self.party.member_count == 1:
            await self.party.me.leave()

    async def event_command_error--- This code section failed: ---

 L. 103         0  SETUP_FINALLY        38  'to 38'

 L. 104         2  LOAD_GLOBAL              isinstance
                4  LOAD_FAST                'error'
                6  LOAD_GLOBAL              commands
                8  LOAD_ATTR                CommandNotFound
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    34  'to 34'

 L. 105        14  LOAD_FAST                'ctx'
               16  LOAD_METHOD              send
               18  LOAD_STR                 'Command not found!\nFor a list of commands visit: https://ezfn.dev/lobbybot/docs'
               20  CALL_METHOD_1         1  ''
               22  GET_AWAITABLE    
               24  LOAD_CONST               None
               26  YIELD_FROM       
               28  POP_BLOCK        
               30  CALL_FINALLY         38  'to 38'
               32  RETURN_VALUE     
             34_0  COME_FROM            12  '12'
               34  POP_BLOCK        
               36  BEGIN_FINALLY    
             38_0  COME_FROM            30  '30'
             38_1  COME_FROM_FINALLY     0  '0'

 L. 108        38  LOAD_FAST                'self'
               40  LOAD_ATTR                send_anonymous_data
               42  POP_JUMP_IF_FALSE    96  'to 96'

 L. 109        44  LOAD_FAST                'self'
               46  LOAD_ATTR                main_client
               48  LOAD_ATTR                session
               50  LOAD_ATTR                post

 L. 110        52  LOAD_STR                 'https://api.ezfn.dev/traceback'

 L. 112        54  LOAD_GLOBAL              str
               56  LOAD_FAST                'error'
               58  LOAD_ATTR                __class__
               60  LOAD_ATTR                __name__
               62  CALL_FUNCTION_1       1  ''

 L. 113        64  LOAD_GLOBAL              str
               66  LOAD_GLOBAL              traceback
               68  LOAD_METHOD              format_exc
               70  CALL_METHOD_0         0  ''
               72  CALL_FUNCTION_1       1  ''

 L. 114        74  LOAD_GLOBAL              str
               76  LOAD_FAST                'error'
               78  CALL_FUNCTION_1       1  ''

 L. 111        80  LOAD_CONST               ('exc_name', 'exc_traceback', 'exc_value')
               82  BUILD_CONST_KEY_MAP_3     3 

 L. 109        84  LOAD_CONST               ('url', 'json')
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  GET_AWAITABLE    
               90  LOAD_CONST               None
               92  YIELD_FROM       
               94  POP_TOP          
             96_0  COME_FROM            42  '42'
               96  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 30

# file __init__.pyc
# Deparsing stopped due to parse error