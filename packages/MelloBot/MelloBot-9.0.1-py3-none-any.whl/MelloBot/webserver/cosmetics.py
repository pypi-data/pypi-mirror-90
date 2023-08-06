import sanic
from EZFNSetup.webserver import Sanic

class Cosmetics:

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

        @self.webserver.get('/cosmetics/<bot_id>/set/<cosmetic_type>')
        @self.webserver.require_payload(['asset', 'variants'])
        @self.webserver.is_authorized()
        async def _(request, bot_id, asset, variants, cosmetic_type):
            client = self.get_client_by_id(bot_id)
            if isinstance(client, sanic.response.HTTPResponse):
                return client
            try:
                v = {'athenacharacter':'outfit',  'athenadance':'emote', 
                 'athenabackpack':'backpack', 
                 'athenapickaxe':'pickaxe', 
                 'athenpetcarrier':'pet', 
                 'athenaemoji':'emoji'}[cosmetic_type.lower()]
            except KeyError:
                return sanic.response.json({'status':'failed', 
                 'error_message':'Type was not added yet'})
            else:
                func = getattr(client.party.me, f"set_{v}")
                if v == 'emote':
                    await client.party.me.clear_emote()
                    await client.party.me.set_emote(asset=asset)
                else:
                    await func(asset=asset, variants=variants)
                return sanic.response.json({'status':'success', 
                 'message':f"Set {v} to {asset}."})


def extension_setup(webserver: Sanic):
    Cosmetics(webserver).start()
# okay decompiling cosmetics.pyc