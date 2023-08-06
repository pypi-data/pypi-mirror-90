# Size of source mod 2**32: 4705 bytes
Instruction context:
   
 L.  45        86  LOAD_FAST                'self'
                  88  LOAD_METHOD              _Friends__invite_friend
                  90  LOAD_FAST                'friend'
                  92  CALL_METHOD_1         1  ''
                  94  GET_AWAITABLE    
                  96  LOAD_CONST               None
                  98  YIELD_FROM       
                 100  ROT_FOUR         
->               102  POP_BLOCK        
                 104  POP_EXCEPT       
                 106  CALL_FINALLY        114  'to 114'
                 108  RETURN_VALUE     
               110_0  COME_FROM            64  '64'
                 110  POP_BLOCK        
                 112  BEGIN_FINALLY    
               114_0  COME_FROM           106  '106'
               114_1  COME_FROM_FINALLY    54  '54'
                 114  LOAD_CONST               None
                 116  STORE_FAST               'e'
                 118  DELETE_FAST              'e'
                 120  END_FINALLY      
                 122  POP_EXCEPT       
                 124  JUMP_FORWARD        148  'to 148'
               126_0  COME_FROM            46  '46'
import asyncio, fortnitepy
from typing import Union
from MelloBot.client import Client
from fortnitepy.ext.commands import Cog

class Friends(Cog):

    def __init__(self, client: Client):
        self.client = client
        self.loop = client.loop
        self.settings = client.settings
        self.invite_throttled_for = 0

    @Cog.event()
    async def event_ready(self):
        self.loop.create_task(self.contains_banned_friend())
        if self.settings['friends']['accept_all_requests']:
            self.loop.create_task(self._inbound('accept'))
        else:
            if self.settings['friends']['decline_all_requests']:
                self.loop.create_task(self._inbound('decline'))

    def name_contains_banned(self, text: str) -> bool:
        return any((banned_word.lower() in text.lower() for banned_word in self.client.main_client.banned_names))

    async def contains_banned_friend(self):
        for friend in self.client.friends:
            try:
                if friend.display_name:
                    if self.name_contains_banned(friend.display_name):
                        self.client.main_client.banned_friends.add(friend.id)
                        await friend.remove()
            except:
                pass

    async def __invite_friend--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              asyncio
                2  LOAD_METHOD              sleep
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                invite_throttled_for
                8  CALL_METHOD_1         1  ''
               10  GET_AWAITABLE    
               12  LOAD_CONST               None
               14  YIELD_FROM       
               16  POP_TOP          

 L.  40        18  SETUP_FINALLY        38  'to 38'

 L.  41        20  LOAD_FAST                'friend'
               22  LOAD_METHOD              invite
               24  CALL_METHOD_0         0  ''
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  POP_TOP          
               34  POP_BLOCK        
               36  JUMP_FORWARD        148  'to 148'
             38_0  COME_FROM_FINALLY    18  '18'

 L.  42        38  DUP_TOP          
               40  LOAD_GLOBAL              fortnitepy
               42  LOAD_ATTR                HTTPException
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE   126  'to 126'
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY       114  'to 114'

 L.  43        56  LOAD_FAST                'e'
               58  LOAD_ATTR                message_code
               60  LOAD_STR                 'errors.com.epicgames.common.throttled'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE   110  'to 110'

 L.  44        66  LOAD_GLOBAL              int
               68  LOAD_FAST                'e'
               70  LOAD_ATTR                message_vars
               72  LOAD_CONST               0
               74  BINARY_SUBSCR    
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_CONST               30
               80  BINARY_ADD       
               82  LOAD_FAST                'self'
               84  STORE_ATTR               invite_throttled_for

 L.  45        86  LOAD_FAST                'self'
               88  LOAD_METHOD              _Friends__invite_friend
               90  LOAD_FAST                'friend'
               92  CALL_METHOD_1         1  ''
               94  GET_AWAITABLE    
               96  LOAD_CONST               None
               98  YIELD_FROM       
              100  ROT_FOUR         
              102  POP_BLOCK        
              104  POP_EXCEPT       
              106  CALL_FINALLY        114  'to 114'
              108  RETURN_VALUE     
            110_0  COME_FROM            64  '64'
              110  POP_BLOCK        
              112  BEGIN_FINALLY    
            114_0  COME_FROM           106  '106'
            114_1  COME_FROM_FINALLY    54  '54'
              114  LOAD_CONST               None
              116  STORE_FAST               'e'
              118  DELETE_FAST              'e'
              120  END_FINALLY      
              122  POP_EXCEPT       
              124  JUMP_FORWARD        148  'to 148'
            126_0  COME_FROM            46  '46'

 L.  46       126  DUP_TOP          
              128  LOAD_GLOBAL              fortnitepy
              130  LOAD_ATTR                PartyError
              132  COMPARE_OP               exception-match
              134  POP_JUMP_IF_FALSE   146  'to 146'
              136  POP_TOP          
              138  POP_TOP          
              140  POP_TOP          

 L.  47       142  POP_EXCEPT       
              144  JUMP_FORWARD        148  'to 148'
            146_0  COME_FROM           134  '134'
              146  END_FINALLY      
            148_0  COME_FROM           144  '144'
            148_1  COME_FROM           124  '124'
            148_2  COME_FROM            36  '36'

 L.  49       148  LOAD_CONST               0
              150  LOAD_FAST                'self'
              152  STORE_ATTR               invite_throttled_for

Parse error at or near `POP_BLOCK' instruction at offset 102

    async def _inbound(self, action: str):
        friends = [friend for friend in self.client.pending_friends if isinstance(friend, fortnitepy.IncomingPendingFriend)]
        for friend in friends:
            try:
                try:
                    if action == 'accept':
                        await friend.accept()
                    else:
                        if action == 'decline':
                            await friend.decline()
                except fortnitepy.HTTPException as e:
                    try:
                        if e.message_code == 'errors.com.epicgames.common.throttled':
                            await asyncio.sleep(int(e.message_vars[0]) + 30)
                    finally:
                        e = None
                        del e

                except Exception as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

            finally:
                await asyncio.sleep(0.3)

    @Cog.event()
    async def event_friend_presence(self, old_presence: Union[(None, fortnitepy.Presence)], presence: fortnitepy.Presence):
        if not self.client.is_ready():
            await self.client.wait_until_ready()
        if old_presence is None:
            friend = presence.friend
            try:
                await friend.send(self.client.main_client.friend_presence_message)
            except:
                pass
            else:
                if self.settings['friends']['invite_on_startup']:
                    if not self.client.party.member_count >= 16:
                        await self._Friends__invite_friend(friend)

    @Cog.event()
    async def event_friend_add(self, friend: fortnitepy.Friend):
        try:
            await friend.send(self.client.main_client.friend_added_message)
        finally:
            try:
                if self.settings['friends']['invite_on_added']:
                    await friend.invite()
            except:
                pass

    @Cog.event()
    async def event_friend_remove(self, friend: fortnitepy.Friend):
        if friend.id in self.client.main_client.banned_friends or self.name_contains_banned(friend.display_name):
            return
        try:
            if self.settings['friends']['add_on_removed']:
                await self.client.add_friend(friend.id)
        except:
            pass

    @Cog.event()
    async def event_friend_request(self, request: Union[(fortnitepy.IncomingPendingFriend, fortnitepy.OutgoingPendingFriend)]):
        if request.id in self.client.main_client.banned_friends or self.name_contains_banned(request.display_name):
            return
        try:
            if request.id in self.client.owner_ids:
                await request.accept()
            else:
                if self.settings['friends']['accept_all_requests']:
                    await request.accept()
                else:
                    if self.settings['friends']['decline_all_requests']:
                        await request.decline()
        except:
            pass


def extension_setup(client: Client):
    client.add_cog(Friends(client))