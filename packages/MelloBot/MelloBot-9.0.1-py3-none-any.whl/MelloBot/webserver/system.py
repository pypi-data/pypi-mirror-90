import os, sanic
from psutil import Process
from EZFNSetup.webserver import Sanic

class System:

    def __init__(self, webserver: Sanic):
        self.webserver = webserver
        self.process = Process(os.getpid())

    def start(self):

        @self.webserver.get('/info')
        async def _(request):
            clients = []
            for client in self.webserver.client.clients.values():
                try:
                    clients.append({'image_url':f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.outfit}/icon.png", 
                     'variants':[f"https://fortnite-api.com/images/cosmetics/br/{client.party.me.outfit}/variants/{v['channel']}/{v['variant']}.png" for v in client.party.me.outfit_variants], 
                     'display_name':client.user.display_name, 
                     'user_id':client.user.id, 
                     'online_since':client.online_since.strftime('%m/%d/%Y %H:%M:%S'), 
                     'party_members':client.party.member_count, 
                     'friends':len(list(client.friends)), 
                     'status':'Online'})
                except:
                    clients.append({'image_url':'', 
                     'variants':'', 
                     'display_name':'', 
                     'user_id':'', 
                     'online_since':'', 
                     'party_members':'', 
                     'friends':'', 
                     'status':'Offline'})

            else:
                return sanic.response.json({'ram':f"{self.process.memory_full_info().rss / 1048576:.2f}", 
                 'pid':os.getpid(), 
                 'bots_online':len(self.webserver.client.clients), 
                 'bots':clients, 
                 'from_old_version':self.webserver.client.from_old_version, 
                 'version':self.webserver.client.version})

        @self.webserver.delete('/exit')
        @self.webserver.is_authorized()
        async def _(request: sanic.request):
            os._exit(1)


def extension_setup(webserver: Sanic):
    System(webserver).start()
# okay decompiling system.pyc