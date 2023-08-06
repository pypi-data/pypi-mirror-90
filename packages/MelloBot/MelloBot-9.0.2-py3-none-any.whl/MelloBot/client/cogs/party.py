# Embedded file name: <EZFNSetup-4.0.8>/EZFNSetup/client/cogs/party.py
# Compiled at: 2020-10-25 22:13:51
# Size of source mod 2**32: 8089 bytes
Instruction context:
   
 L.  47       394  LOAD_FAST                'ctx'
                 396  LOAD_METHOD              send
                 398  LOAD_STR                 'Failed to join '
                 400  LOAD_FAST                'friend'
                 402  LOAD_ATTR                display_name
                 404  FORMAT_VALUE          0  ''
                 406  LOAD_STR                 ' as he is already a part of this party.'
                 408  BUILD_STRING_3        3 
                 410  CALL_METHOD_1         1  ''
                 412  GET_AWAITABLE    
                 414  LOAD_CONST               None
                 416  YIELD_FROM       
                 418  ROT_FOUR         
->               420  POP_BLOCK        
                 422  POP_EXCEPT       
                 424  CALL_FINALLY        432  'to 432'
                 426  RETURN_VALUE     
               428_0  COME_FROM           390  '390'
                 428  POP_BLOCK        
                 430  BEGIN_FINALLY    
               432_0  COME_FROM           424  '424'
               432_1  COME_FROM_FINALLY   378  '378'
                 432  LOAD_CONST               None
                 434  STORE_FAST               'e'
                 436  DELETE_FAST              'e'
                 438  END_FINALLY      
                 440  POP_EXCEPT       
                 442  JUMP_FORWARD        576  'to 576'
               444_0  COME_FROM           368  '368'
Instruction context:
   
 L.  80       366  LOAD_FAST                'ctx'
                 368  LOAD_METHOD              send
                 370  LOAD_STR                 'Failed to invite '
                 372  LOAD_FAST                'friend'
                 374  LOAD_ATTR                display_name
                 376  FORMAT_VALUE          0  ''
                 378  LOAD_STR                 ' as he is already a part of this party.'
                 380  BUILD_STRING_3        3 
                 382  CALL_METHOD_1         1  ''
                 384  GET_AWAITABLE    
                 386  LOAD_CONST               None
                 388  YIELD_FROM       
                 390  ROT_FOUR         
->               392  POP_BLOCK        
                 394  POP_EXCEPT       
                 396  CALL_FINALLY        486  'to 486'
                 398  RETURN_VALUE     
               400_0  COME_FROM           362  '362'
import asyncio, datetime, fortnitepy
from typing import Union
from MelloBot.utils import Playlist
from MelloBot.client import Client
from fortnitepy.ext.commands import Cog, Context, command, group

class Party(Cog):

    def __init__(self, client: Client):
        self.client = client

    @command(aliases=['gamemode'])
    async def playlist(self, ctx: Context, *, playlist: Playlist):
        await self.client.party.set_playlist(playlist=(playlist['dev_name']))
        await ctx.send(f"Playlist set to {playlist['names']['en']}.")

    @command()
    async def join--- This code section failed: ---

 L.  20         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                client
                4  LOAD_ATTR                settings
                6  LOAD_STR                 'party'
                8  BINARY_SUBSCR    
               10  LOAD_STR                 'dont_leave_if_owner_in_party'
               12  BINARY_SUBSCR    
               14  POP_JUMP_IF_FALSE    66  'to 66'

 L.  21        16  LOAD_GLOBAL              any
               18  LOAD_CLOSURE             'self'
               20  BUILD_TUPLE_1         1 
               22  LOAD_GENEXPR             '<code_object <genexpr>>'
               24  LOAD_STR                 'Party.join.<locals>.<genexpr>'
               26  MAKE_FUNCTION_8          'closure'
               28  LOAD_DEREF               'self'
               30  LOAD_ATTR                client
               32  LOAD_ATTR                owner_ids
               34  GET_ITER         
               36  CALL_FUNCTION_1       1  ''
               38  CALL_FUNCTION_1       1  ''
               40  POP_JUMP_IF_FALSE    66  'to 66'

 L.  22        42  LOAD_FAST                'ctx'
               44  LOAD_ATTR                author
               46  LOAD_METHOD              send
               48  LOAD_DEREF               'self'
               50  LOAD_ATTR                client
               52  LOAD_ATTR                main_client
               54  LOAD_ATTR                not_allowed_to_join_message
               56  CALL_METHOD_1         1  ''
               58  GET_AWAITABLE    
               60  LOAD_CONST               None
               62  YIELD_FROM       
               64  RETURN_VALUE     
             66_0  COME_FROM            40  '40'
             66_1  COME_FROM            14  '14'

 L.  24        66  LOAD_GLOBAL              isinstance
               68  LOAD_FAST                'ctx'
               70  LOAD_ATTR                message
               72  LOAD_GLOBAL              fortnitepy
               74  LOAD_ATTR                PartyMessage
               76  CALL_FUNCTION_2       2  ''
               78  POP_JUMP_IF_FALSE   104  'to 104'
               80  LOAD_FAST                'display_name'
               82  LOAD_CONST               None
               84  COMPARE_OP               is
               86  POP_JUMP_IF_FALSE   104  'to 104'

 L.  25        88  LOAD_FAST                'ctx'
               90  LOAD_METHOD              send
               92  LOAD_STR                 'Failed to join you as you are already a part of this party.'
               94  CALL_METHOD_1         1  ''
               96  GET_AWAITABLE    
               98  LOAD_CONST               None
              100  YIELD_FROM       
              102  RETURN_VALUE     
            104_0  COME_FROM            86  '86'
            104_1  COME_FROM            78  '78'

 L.  26       104  LOAD_GLOBAL              isinstance
              106  LOAD_FAST                'ctx'
              108  LOAD_ATTR                message
              110  LOAD_GLOBAL              fortnitepy
              112  LOAD_ATTR                FriendMessage
              114  CALL_FUNCTION_2       2  ''
              116  POP_JUMP_IF_FALSE   144  'to 144'
              118  LOAD_FAST                'display_name'
              120  LOAD_CONST               None
              122  COMPARE_OP               is
              124  POP_JUMP_IF_FALSE   144  'to 144'

 L.  27       126  LOAD_DEREF               'self'
              128  LOAD_ATTR                client
              130  LOAD_METHOD              get_friend
              132  LOAD_FAST                'ctx'
              134  LOAD_ATTR                author
              136  LOAD_ATTR                id
              138  CALL_METHOD_1         1  ''
              140  STORE_FAST               'friend'
              142  JUMP_FORWARD        204  'to 204'
            144_0  COME_FROM           124  '124'
            144_1  COME_FROM           116  '116'

 L.  29       144  LOAD_DEREF               'self'
              146  LOAD_ATTR                client
              148  LOAD_METHOD              fetch_profile
              150  LOAD_FAST                'display_name'
              152  CALL_METHOD_1         1  ''
              154  GET_AWAITABLE    
              156  LOAD_CONST               None
              158  YIELD_FROM       
              160  STORE_FAST               'user'

 L.  30       162  LOAD_FAST                'user'
              164  POP_JUMP_IF_TRUE    190  'to 190'

 L.  31       166  LOAD_FAST                'ctx'
              168  LOAD_METHOD              send
              170  LOAD_STR                 'Can not find any user with the name '
              172  LOAD_FAST                'display_name'
              174  FORMAT_VALUE          0  ''
              176  LOAD_STR                 '.'
              178  BUILD_STRING_3        3 
              180  CALL_METHOD_1         1  ''
              182  GET_AWAITABLE    
              184  LOAD_CONST               None
              186  YIELD_FROM       
              188  RETURN_VALUE     
            190_0  COME_FROM           164  '164'

 L.  32       190  LOAD_DEREF               'self'
              192  LOAD_ATTR                client
              194  LOAD_METHOD              get_friend
              196  LOAD_FAST                'user'
              198  LOAD_ATTR                id
              200  CALL_METHOD_1         1  ''
              202  STORE_FAST               'friend'
            204_0  COME_FROM           142  '142'

 L.  34       204  LOAD_FAST                'friend'
              206  LOAD_CONST               None
              208  COMPARE_OP               is
          210_212  POP_JUMP_IF_FALSE   282  'to 282'

 L.  35       214  SETUP_FINALLY       240  'to 240'

 L.  36       216  LOAD_DEREF               'self'
              218  LOAD_ATTR                client
              220  LOAD_METHOD              add_friend
              222  LOAD_FAST                'user'
              224  LOAD_ATTR                id
              226  CALL_METHOD_1         1  ''
              228  GET_AWAITABLE    
              230  LOAD_CONST               None
              232  YIELD_FROM       
              234  POP_TOP          
              236  POP_BLOCK        
              238  BEGIN_FINALLY    
            240_0  COME_FROM_FINALLY   214  '214'

 L.  38       240  LOAD_FAST                'ctx'
              242  LOAD_METHOD              send
              244  LOAD_FAST                'display_name'
          246_248  POP_JUMP_IF_FALSE   258  'to 258'
              250  LOAD_FAST                'display_name'
              252  LOAD_STR                 ' is'
              254  BINARY_ADD       
              256  JUMP_FORWARD        260  'to 260'
            258_0  COME_FROM           246  '246'
              258  LOAD_STR                 'You are'
            260_0  COME_FROM           256  '256'
              260  FORMAT_VALUE          0  ''
              262  LOAD_STR                 ' not my friend.'
              264  BUILD_STRING_2        2 
              266  CALL_METHOD_1         1  ''
              268  GET_AWAITABLE    
              270  LOAD_CONST               None
              272  YIELD_FROM       
              274  POP_TOP          
              276  END_FINALLY      
          278_280  JUMP_FORWARD        576  'to 576'
            282_0  COME_FROM           210  '210'

 L.  39       282  LOAD_GLOBAL              isinstance
              284  LOAD_FAST                'friend'
              286  LOAD_GLOBAL              fortnitepy
              288  LOAD_ATTR                Friend
              290  CALL_FUNCTION_2       2  ''
          292_294  POP_JUMP_IF_FALSE   576  'to 576'

 L.  40       296  LOAD_DEREF               'self'
              298  LOAD_ATTR                client
              300  LOAD_ATTR                party
              302  LOAD_METHOD              get_member
              304  LOAD_FAST                'friend'
              306  LOAD_ATTR                id
              308  CALL_METHOD_1         1  ''
          310_312  POP_JUMP_IF_FALSE   340  'to 340'

 L.  41       314  LOAD_FAST                'ctx'
              316  LOAD_METHOD              send
              318  LOAD_STR                 'Failed to join '
              320  LOAD_FAST                'friend'
              322  LOAD_ATTR                display_name
              324  FORMAT_VALUE          0  ''
              326  LOAD_STR                 ' as he is already a part of this party.'
              328  BUILD_STRING_3        3 
              330  CALL_METHOD_1         1  ''
              332  GET_AWAITABLE    
              334  LOAD_CONST               None
              336  YIELD_FROM       
              338  RETURN_VALUE     
            340_0  COME_FROM           310  '310'

 L.  43       340  SETUP_FINALLY       360  'to 360'

 L.  44       342  LOAD_FAST                'friend'
              344  LOAD_METHOD              join
              346  CALL_METHOD_0         0  ''
              348  GET_AWAITABLE    
              350  LOAD_CONST               None
              352  YIELD_FROM       
              354  POP_TOP          
              356  POP_BLOCK        
              358  JUMP_FORWARD        576  'to 576'
            360_0  COME_FROM_FINALLY   340  '340'

 L.  45       360  DUP_TOP          
              362  LOAD_GLOBAL              fortnitepy
              364  LOAD_ATTR                PartyError
              366  COMPARE_OP               exception-match
          368_370  POP_JUMP_IF_FALSE   444  'to 444'
              372  POP_TOP          
              374  STORE_FAST               'e'
              376  POP_TOP          
              378  SETUP_FINALLY       432  'to 432'

 L.  46       380  LOAD_GLOBAL              str
              382  LOAD_FAST                'e'
              384  CALL_FUNCTION_1       1  ''
              386  LOAD_STR                 'You are already a member of this party.'
              388  COMPARE_OP               ==
          390_392  POP_JUMP_IF_FALSE   428  'to 428'

 L.  47       394  LOAD_FAST                'ctx'
              396  LOAD_METHOD              send
              398  LOAD_STR                 'Failed to join '
              400  LOAD_FAST                'friend'
              402  LOAD_ATTR                display_name
              404  FORMAT_VALUE          0  ''
              406  LOAD_STR                 ' as he is already a part of this party.'
              408  BUILD_STRING_3        3 
              410  CALL_METHOD_1         1  ''
              412  GET_AWAITABLE    
              414  LOAD_CONST               None
              416  YIELD_FROM       
              418  ROT_FOUR         
              420  POP_BLOCK        
              422  POP_EXCEPT       
              424  CALL_FINALLY        432  'to 432'
              426  RETURN_VALUE     
            428_0  COME_FROM           390  '390'
              428  POP_BLOCK        
              430  BEGIN_FINALLY    
            432_0  COME_FROM           424  '424'
            432_1  COME_FROM_FINALLY   378  '378'
              432  LOAD_CONST               None
              434  STORE_FAST               'e'
              436  DELETE_FAST              'e'
              438  END_FINALLY      
              440  POP_EXCEPT       
              442  JUMP_FORWARD        576  'to 576'
            444_0  COME_FROM           368  '368'

 L.  48       444  DUP_TOP          
              446  LOAD_GLOBAL              fortnitepy
              448  LOAD_ATTR                Forbidden
              450  COMPARE_OP               exception-match
          452_454  POP_JUMP_IF_FALSE   510  'to 510'
              456  POP_TOP          
              458  STORE_FAST               'e'
              460  POP_TOP          
              462  SETUP_FINALLY       498  'to 498'

 L.  49       464  LOAD_FAST                'ctx'
              466  LOAD_METHOD              send
              468  LOAD_STR                 'Failed to join '
              470  LOAD_FAST                'friend'
              472  LOAD_ATTR                display_name
              474  FORMAT_VALUE          0  ''
              476  LOAD_STR                 ' his party is private.'
              478  BUILD_STRING_3        3 
              480  CALL_METHOD_1         1  ''
              482  GET_AWAITABLE    
              484  LOAD_CONST               None
              486  YIELD_FROM       
              488  ROT_FOUR         
              490  POP_BLOCK        
              492  POP_EXCEPT       
              494  CALL_FINALLY        498  'to 498'
              496  RETURN_VALUE     
            498_0  COME_FROM           494  '494'
            498_1  COME_FROM_FINALLY   462  '462'
              498  LOAD_CONST               None
              500  STORE_FAST               'e'
              502  DELETE_FAST              'e'
              504  END_FINALLY      
              506  POP_EXCEPT       
              508  JUMP_FORWARD        576  'to 576'
            510_0  COME_FROM           452  '452'

 L.  50       510  DUP_TOP          
              512  LOAD_GLOBAL              Exception
              514  COMPARE_OP               exception-match
          516_518  POP_JUMP_IF_FALSE   574  'to 574'
              520  POP_TOP          
              522  STORE_FAST               'e'
              524  POP_TOP          
              526  SETUP_FINALLY       562  'to 562'

 L.  51       528  LOAD_FAST                'ctx'
              530  LOAD_METHOD              send
              532  LOAD_STR                 'Failed to parse error: '
              534  LOAD_GLOBAL              str
              536  LOAD_FAST                'e'
              538  CALL_FUNCTION_1       1  ''
              540  FORMAT_VALUE          0  ''
              542  BUILD_STRING_2        2 
              544  CALL_METHOD_1         1  ''
              546  GET_AWAITABLE    
              548  LOAD_CONST               None
              550  YIELD_FROM       
              552  ROT_FOUR         
              554  POP_BLOCK        
              556  POP_EXCEPT       
              558  CALL_FINALLY        562  'to 562'
              560  RETURN_VALUE     
            562_0  COME_FROM           558  '558'
            562_1  COME_FROM_FINALLY   526  '526'
              562  LOAD_CONST               None
              564  STORE_FAST               'e'
              566  DELETE_FAST              'e'
              568  END_FINALLY      
              570  POP_EXCEPT       
              572  JUMP_FORWARD        576  'to 576'
            574_0  COME_FROM           516  '516'
              574  END_FINALLY      
            576_0  COME_FROM           572  '572'
            576_1  COME_FROM           508  '508'
            576_2  COME_FROM           442  '442'
            576_3  COME_FROM           358  '358'
            576_4  COME_FROM           292  '292'
            576_5  COME_FROM           278  '278'

Parse error at or near `POP_BLOCK' instruction at offset 420

    @command()
    async def invite--- This code section failed: ---

 L.  55         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'ctx'
                4  LOAD_ATTR                message
                6  LOAD_GLOBAL              fortnitepy
                8  LOAD_ATTR                PartyMessage
               10  CALL_FUNCTION_2       2  ''
               12  POP_JUMP_IF_FALSE    38  'to 38'
               14  LOAD_FAST                'display_name'
               16  LOAD_CONST               None
               18  COMPARE_OP               is
               20  POP_JUMP_IF_FALSE    38  'to 38'

 L.  56        22  LOAD_FAST                'ctx'
               24  LOAD_METHOD              send
               26  LOAD_STR                 'Failed to invite you as you are already a part of this party.'
               28  CALL_METHOD_1         1  ''
               30  GET_AWAITABLE    
               32  LOAD_CONST               None
               34  YIELD_FROM       
               36  RETURN_VALUE     
             38_0  COME_FROM            20  '20'
             38_1  COME_FROM            12  '12'

 L.  57        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'ctx'
               42  LOAD_ATTR                message
               44  LOAD_GLOBAL              fortnitepy
               46  LOAD_ATTR                FriendMessage
               48  CALL_FUNCTION_2       2  ''
               50  POP_JUMP_IF_FALSE    78  'to 78'
               52  LOAD_FAST                'display_name'
               54  LOAD_CONST               None
               56  COMPARE_OP               is
               58  POP_JUMP_IF_FALSE    78  'to 78'

 L.  58        60  LOAD_FAST                'self'
               62  LOAD_ATTR                client
               64  LOAD_METHOD              get_friend
               66  LOAD_FAST                'ctx'
               68  LOAD_ATTR                author
               70  LOAD_ATTR                id
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'friend'
               76  JUMP_FORWARD        138  'to 138'
             78_0  COME_FROM            58  '58'
             78_1  COME_FROM            50  '50'

 L.  60        78  LOAD_FAST                'self'
               80  LOAD_ATTR                client
               82  LOAD_METHOD              fetch_profile
               84  LOAD_FAST                'display_name'
               86  CALL_METHOD_1         1  ''
               88  GET_AWAITABLE    
               90  LOAD_CONST               None
               92  YIELD_FROM       
               94  STORE_FAST               'user'

 L.  61        96  LOAD_FAST                'user'
               98  POP_JUMP_IF_TRUE    124  'to 124'

 L.  62       100  LOAD_FAST                'ctx'
              102  LOAD_METHOD              send
              104  LOAD_STR                 'Can not find any user with the name '
              106  LOAD_FAST                'display_name'
              108  FORMAT_VALUE          0  ''
              110  LOAD_STR                 '.'
              112  BUILD_STRING_3        3 
              114  CALL_METHOD_1         1  ''
              116  GET_AWAITABLE    
              118  LOAD_CONST               None
              120  YIELD_FROM       
              122  RETURN_VALUE     
            124_0  COME_FROM            98  '98'

 L.  63       124  LOAD_FAST                'self'
              126  LOAD_ATTR                client
              128  LOAD_METHOD              get_friend
              130  LOAD_FAST                'user'
              132  LOAD_ATTR                id
              134  CALL_METHOD_1         1  ''
              136  STORE_FAST               'friend'
            138_0  COME_FROM            76  '76'

 L.  65       138  LOAD_FAST                'friend'
              140  LOAD_CONST               None
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   212  'to 212'

 L.  66       146  SETUP_FINALLY       172  'to 172'

 L.  67       148  LOAD_FAST                'self'
              150  LOAD_ATTR                client
              152  LOAD_METHOD              add_friend
              154  LOAD_FAST                'user'
              156  LOAD_ATTR                id
              158  CALL_METHOD_1         1  ''
              160  GET_AWAITABLE    
              162  LOAD_CONST               None
              164  YIELD_FROM       
              166  POP_TOP          
              168  POP_BLOCK        
              170  BEGIN_FINALLY    
            172_0  COME_FROM_FINALLY   146  '146'

 L.  69       172  LOAD_FAST                'ctx'
              174  LOAD_METHOD              send
              176  LOAD_FAST                'display_name'
              178  POP_JUMP_IF_FALSE   188  'to 188'
              180  LOAD_FAST                'display_name'
              182  LOAD_STR                 ' is'
              184  BINARY_ADD       
              186  JUMP_FORWARD        190  'to 190'
            188_0  COME_FROM           178  '178'
              188  LOAD_STR                 'You are'
            190_0  COME_FROM           186  '186'
              190  FORMAT_VALUE          0  ''
              192  LOAD_STR                 ' not my friend.'
              194  BUILD_STRING_2        2 
              196  CALL_METHOD_1         1  ''
              198  GET_AWAITABLE    
              200  LOAD_CONST               None
              202  YIELD_FROM       
              204  POP_TOP          
              206  END_FINALLY      
          208_210  JUMP_FORWARD        564  'to 564'
            212_0  COME_FROM           144  '144'

 L.  70       212  LOAD_GLOBAL              isinstance
              214  LOAD_FAST                'friend'
              216  LOAD_GLOBAL              fortnitepy
              218  LOAD_ATTR                Friend
              220  CALL_FUNCTION_2       2  ''
          222_224  POP_JUMP_IF_FALSE   564  'to 564'

 L.  71       226  LOAD_FAST                'self'
              228  LOAD_ATTR                client
              230  LOAD_ATTR                party
              232  LOAD_METHOD              get_member
              234  LOAD_FAST                'friend'
              236  LOAD_ATTR                id
              238  CALL_METHOD_1         1  ''
          240_242  POP_JUMP_IF_FALSE   270  'to 270'

 L.  72       244  LOAD_FAST                'ctx'
              246  LOAD_METHOD              send
              248  LOAD_STR                 'Failed to invite '
              250  LOAD_FAST                'friend'
              252  LOAD_ATTR                display_name
              254  FORMAT_VALUE          0  ''
              256  LOAD_STR                 ' as he is already a part of this party.'
              258  BUILD_STRING_3        3 
              260  CALL_METHOD_1         1  ''
              262  GET_AWAITABLE    
              264  LOAD_CONST               None
              266  YIELD_FROM       
              268  RETURN_VALUE     
            270_0  COME_FROM           240  '240'

 L.  73       270  LOAD_FAST                'self'
              272  LOAD_ATTR                client
              274  LOAD_ATTR                party
              276  LOAD_ATTR                member_count
              278  LOAD_CONST               16
              280  COMPARE_OP               ==
          282_284  POP_JUMP_IF_FALSE   312  'to 312'

 L.  74       286  LOAD_FAST                'ctx'
              288  LOAD_METHOD              send
              290  LOAD_STR                 'Failed to invite '
              292  LOAD_FAST                'friend'
              294  LOAD_ATTR                display_name
              296  FORMAT_VALUE          0  ''
              298  LOAD_STR                 ' the party is full.'
              300  BUILD_STRING_3        3 
              302  CALL_METHOD_1         1  ''
              304  GET_AWAITABLE    
              306  LOAD_CONST               None
              308  YIELD_FROM       
              310  RETURN_VALUE     
            312_0  COME_FROM           282  '282'

 L.  76       312  SETUP_FINALLY       332  'to 332'

 L.  77       314  LOAD_FAST                'friend'
              316  LOAD_METHOD              invite
              318  CALL_METHOD_0         0  ''
              320  GET_AWAITABLE    
              322  LOAD_CONST               None
              324  YIELD_FROM       
              326  POP_TOP          
              328  POP_BLOCK        
              330  JUMP_FORWARD        564  'to 564'
            332_0  COME_FROM_FINALLY   312  '312'

 L.  78       332  DUP_TOP          
              334  LOAD_GLOBAL              fortnitepy
              336  LOAD_ATTR                PartyError
              338  COMPARE_OP               exception-match
          340_342  POP_JUMP_IF_FALSE   498  'to 498'
              344  POP_TOP          
              346  STORE_FAST               'e'
              348  POP_TOP          
              350  SETUP_FINALLY       486  'to 486'

 L.  79       352  LOAD_GLOBAL              str
              354  LOAD_FAST                'e'
              356  CALL_FUNCTION_1       1  ''
              358  LOAD_STR                 'Friend is already in your party.'
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   400  'to 400'

 L.  80       366  LOAD_FAST                'ctx'
              368  LOAD_METHOD              send
              370  LOAD_STR                 'Failed to invite '
              372  LOAD_FAST                'friend'
              374  LOAD_ATTR                display_name
              376  FORMAT_VALUE          0  ''
              378  LOAD_STR                 ' as he is already a part of this party.'
              380  BUILD_STRING_3        3 
              382  CALL_METHOD_1         1  ''
              384  GET_AWAITABLE    
              386  LOAD_CONST               None
              388  YIELD_FROM       
              390  ROT_FOUR         
              392  POP_BLOCK        
              394  POP_EXCEPT       
              396  CALL_FINALLY        486  'to 486'
              398  RETURN_VALUE     
            400_0  COME_FROM           362  '362'

 L.  81       400  LOAD_GLOBAL              str
              402  LOAD_FAST                'e'
              404  CALL_FUNCTION_1       1  ''
              406  LOAD_STR                 'The party is full.'
              408  COMPARE_OP               ==
          410_412  POP_JUMP_IF_FALSE   448  'to 448'

 L.  82       414  LOAD_FAST                'ctx'
              416  LOAD_METHOD              send
              418  LOAD_STR                 'Failed to invite '
              420  LOAD_FAST                'friend'
              422  LOAD_ATTR                display_name
              424  FORMAT_VALUE          0  ''
              426  LOAD_STR                 ' the party is full.'
              428  BUILD_STRING_3        3 
              430  CALL_METHOD_1         1  ''
              432  GET_AWAITABLE    
              434  LOAD_CONST               None
              436  YIELD_FROM       
              438  ROT_FOUR         
              440  POP_BLOCK        
              442  POP_EXCEPT       
              444  CALL_FINALLY        486  'to 486'
              446  RETURN_VALUE     
            448_0  COME_FROM           410  '410'

 L.  84       448  LOAD_FAST                'ctx'
              450  LOAD_METHOD              send
              452  LOAD_STR                 'Failed to parse error: '
              454  LOAD_GLOBAL              str
              456  LOAD_FAST                'e'
              458  CALL_FUNCTION_1       1  ''
              460  FORMAT_VALUE          0  ''
              462  BUILD_STRING_2        2 
              464  CALL_METHOD_1         1  ''
              466  GET_AWAITABLE    
              468  LOAD_CONST               None
              470  YIELD_FROM       
              472  ROT_FOUR         
              474  POP_BLOCK        
              476  POP_EXCEPT       
              478  CALL_FINALLY        486  'to 486'
              480  RETURN_VALUE     
              482  POP_BLOCK        
              484  BEGIN_FINALLY    
            486_0  COME_FROM           478  '478'
            486_1  COME_FROM           444  '444'
            486_2  COME_FROM           396  '396'
            486_3  COME_FROM_FINALLY   350  '350'
              486  LOAD_CONST               None
              488  STORE_FAST               'e'
              490  DELETE_FAST              'e'
              492  END_FINALLY      
              494  POP_EXCEPT       
              496  JUMP_FORWARD        564  'to 564'
            498_0  COME_FROM           340  '340'

 L.  85       498  DUP_TOP          
              500  LOAD_GLOBAL              Exception
              502  COMPARE_OP               exception-match
          504_506  POP_JUMP_IF_FALSE   562  'to 562'
              508  POP_TOP          
              510  STORE_FAST               'e'
              512  POP_TOP          
              514  SETUP_FINALLY       550  'to 550'

 L.  86       516  LOAD_FAST                'ctx'
              518  LOAD_METHOD              send
              520  LOAD_STR                 'Failed to parse error: '
              522  LOAD_GLOBAL              str
              524  LOAD_FAST                'e'
              526  CALL_FUNCTION_1       1  ''
              528  FORMAT_VALUE          0  ''
              530  BUILD_STRING_2        2 
              532  CALL_METHOD_1         1  ''
              534  GET_AWAITABLE    
              536  LOAD_CONST               None
              538  YIELD_FROM       
              540  ROT_FOUR         
              542  POP_BLOCK        
              544  POP_EXCEPT       
              546  CALL_FINALLY        550  'to 550'
              548  RETURN_VALUE     
            550_0  COME_FROM           546  '546'
            550_1  COME_FROM_FINALLY   514  '514'
              550  LOAD_CONST               None
              552  STORE_FAST               'e'
              554  DELETE_FAST              'e'
              556  END_FINALLY      
              558  POP_EXCEPT       
              560  JUMP_FORWARD        564  'to 564'
            562_0  COME_FROM           504  '504'
              562  END_FINALLY      
            564_0  COME_FROM           560  '560'
            564_1  COME_FROM           496  '496'
            564_2  COME_FROM           330  '330'
            564_3  COME_FROM           222  '222'
            564_4  COME_FROM           208  '208'

Parse error at or near `POP_BLOCK' instruction at offset 392

    @command()
    async def promote(self, ctx: Context, *, party_member: str=None):
        if not self.client.party.me.leader:
            return await ctx.send('Party leader permission needed.')
            if party_member is None:
                party_member = self.client.party.get_member(ctx.author.id)
                if party_member is None:
                    return await ctx.send(f"{ctx.author.display_name} is not a member of the party.")
            else:
                user = await self.client.fetch_user(party_member)
                if user is None:
                    return await ctx.send(f"Can not find any user with the name {party_member}.")
                party_member = self.client.party.get_member(user.id)
                if party_member is None:
                    return await ctx.send(f"{user.display_name} is not a member of the party.")
        else:
            try:
                await party_member.promote
                await ctx.send(f"Promoted {party_member.display_name}.")
            except Exception as e:
                try:
                    await ctx.send(f"Failed to parse error: {str(e)}")
                finally:
                    e = None
                    del e

    @command(aliases=['ingame', 'game'])
    async def match(self, ctx: Context, players_left: int=100, started_at: int=0):
        await self.client.party.me.set_in_match(players_left=players_left, started_at=(datetime.datetime.utcnow - datetime.timedelta(minutes=started_at)))
        await ctx.send(f"Set state to ingame with {players_left} players left.")

    @command()
    async def ready(self, ctx: Context):
        await self.client.party.me.set_ready(fortnitepy.ReadyState.READY)
        await ctx.send('Set readiness to "Ready".')

    @command(aliases=['sitin'])
    async def unready(self, ctx: Context):
        await self.client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        await ctx.send('Set readiness to "Not Ready".')

    @command()
    async def sitout(self, ctx: Context):
        await self.client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
        await ctx.send('Set readiness to "Sitout".')

    @group()
    async def leave(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('What should I leave?\nPlease add match or party.')

    @leave.command(name='party')
    async def leave_party(self, ctx: Context):
        if self.client.settings['party']['dont_leave_if_owner_in_party']:
            if any((owner_id in self.client.party.members for owner_id in self.client.owner_ids)):
                return await ctx.author.send(self.client.main_client.not_allowed_to_join_message)
        try:
            await self.client.party.me.set_emote('EID_Wave')
            await self.client.party.send(self.client.main_client.leave_party_message)
            await asyncio.sleep(2)
        except:
            pass

        try:
            await self.client.party.me.leave
            await ctx.send('Left the party.')
        except:
            await ctx.send("Something wen't wrong, please try again later.")

    @leave.command(name='match', aliases=['ingame', 'game'])
    async def leave_match(self, ctx: Context):
        await self.client.party.me.clear_in_match
        await ctx.send('Set state to lobby.')


def extension_setup(client: Client):
    client.add_cog(Party(client))