import sanic
from EZFNSetup.webserver import Sanic

class Dashboard:

    def __init__(self, webserver: Sanic):
        self.webserver = webserver
        self.clients = webserver.client.clients

    def get_client_by_id(self, account_id: str):
        client = [c for c in list(self.clients.values()) if c.user.id == account_id]
        if not client:
            return sanic.response.json({'status':'failed',  'error_code':'account.not_found',  'error_message':'Could not find a client by this account id'}, status=400)
        else:
            client = client[0]
            return client.is_ready() or sanic.response.json({'status':'failed',  'error_code':'account.not_ready',  'error_message':'The client is not ready'}, status=500)
        return client

    def start(self):

        @self.webserver.get('/dashboard/<bot_id>')
        @self.webserver.is_authorized()
        async def _(request, bot_id):
            client = self.get_client_by_id(bot_id)
            if isinstance(client, sanic.response.HTTPResponse):
                return client
            friends = [{'display_name':friend.display_name, 
             'user_id':friend.id,  'added':friend.created_at.strftime('%m/%d/%Y %H:%M:%S'),  'is_online':friend.is_online()} for friend in client.friends][:100]
            return sanic.response.json({'friends':friends, 
             'party':{'cosmetics':{'backpack':client.party.me.backpack, 
               'backpack_variants':client.party.me.backpack_variants,  'banner':client.party.me.banner,  'battlepass_info':client.party.me.battlepass_info,  'emoji':client.party.me.emoji,  'emote':client.party.me.emote,  'outfit':client.party.me.outfit,  'outfit_variants':client.party.me.outfit_variants,  'pet':client.party.me.pet,  'pickaxe':client.party.me.pickaxe,  'pickaxe_variants':client.party.me.pickaxe_variants}, 
              'match':{'match_players_left':client.party.me.match_players_left,  'match_started_at':client.party.me.match_started_at,  'in_match':client.party.me.in_match()} if client.party.me.in_match() else None,  'party':{'id':client.party.id,  'member_count':client.party.member_count,  'members':[{'user_id':member.id,  'display_name':member.display_name,  'joined_at':member.joined_at.strftime('%m/%d/%Y %H:%M:%S')} for member in client.party.members],  'playlist_info':client.party.playlist_info,  'privacy':client.party.privacy.name.capitalize(),  'squad_fill':client.party.squad_fill},  'enlightenments':client.party.me.enlightenments,  'in_match':client.party.me.in_match(),  'input':client.party.me.input,  'is_just_chatting':client.party.me.is_just_chatting(),  'is_chatbanned':client.party.me.is_chatbanned(),  'joined_at':client.party.me.joined_at.strftime('%m/%d/%Y %H:%M:%S'),  'is_leader':client.party.me.leader,  'leader':client.party.leader.display_name if client.party.leader else '',  'platform':client.party.me.platform.name.capitalize(),  'position':client.party.me.position}, 
             'settings':client.settings, 
             'commands':client.command_perms})


def extension_setup(webserver: Sanic):
    Dashboard(webserver).start()
# okay decompiling dashboard.pyc