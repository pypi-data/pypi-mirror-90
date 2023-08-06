import os, sys, sanic, types, asyncio, importlib, traceback, EZFNSetup
from typing import List
from pathlib import Path
from functools import wraps
from psutil import process_iter

class Sanic(sanic.Sanic):

    def __init__(self, client, cogs, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.client = client
        for proc in process_iter():
            try:
                for conns in proc.connections(kind='inet'):
                    if conns.laddr.port == 8000:
                        os.system(f"kill -9 {proc.pid}")
                        self.client.loop.run_until_complete(asyncio.sleep(3))

            except:
                pass

        else:
            self.client.loop.run_until_complete(self.create_server(return_asyncio_server=True,
              host='0.0.0.0',
              debug=False,
              access_log=False))
            for location in cogs:
                for path in Path(f"{EZFNSetup.__path__[0]}/{location}").rglob('*.pyc'):
                    if not str(path).endswith('__init__.pyc'):
                        path = str(path).split(f"{EZFNSetup.__path__[0]}/{location}")[1]
                        try:
                            self.load_extension(f"EZFNSetup.{location}{str(path).replace('/', '.')[:-4]}")
                        except Exception as e:
                            try:
                                f"Failed to load the webserver cog: {path}\n\nTraceBack: {traceback.format_exc()}"
                            finally:
                                e = None
                                del e

                else:

                    @self.middleware('response')
                    async def _(request: sanic.request, response: sanic.response):
                        try:
                            response.headers['Access-Control-Allow-Origin'] = '*'
                        except:
                            pass
                        else:
                            return response

                    @self.get('/')
                    async def _(request):
                        return sanic.response.html(self.client.main_page)

    def _load_from_module_spec(self, spec: types.ModuleType, key: str) -> None:
        lib = importlib.util.module_from_spec(spec)
        sys.modules[key] = lib
        spec.loader.exec_module(lib)
        setup = getattr(lib, 'extension_setup')
        setup(self)

    def load_extension(self, name: str) -> None:
        spec = importlib.util.find_spec(name)
        self._load_from_module_spec(spec, name)

    def require_payload(self, payloads: list):

        def decorator(f):

            @wraps(f)
            async def decorated_function(request, *args, **kwargs):
                if not request.json:
                    return sanic.response.json({'status':'failed', 
                     'error_code':'payload.is_missing', 
                     'error_message':'You must provide the payload.', 
                     'error_vars':payloads},
                      status=400)
                for payload in payloads:
                    if not request.json.get(payload):
                        return sanic.response.json({'status':'failed', 
                         'error_code':'payload.is_missing', 
                         'error_message':f"{payload} is missing.", 
                         'error_vars':[
                          payload]},
                          status=400)
                    kwargs[payload] = request.json.get(payload)
                else:
                    return await f(request, *args, **kwargs)

            return decorated_function

        return decorator

    def is_authorized(self):

        def decorator(f):

            @wraps(f)
            async def decorated_function(request, *args, **kwargs):
                if not request.headers.get('Authorization') == self.client.secret_key:
                    if not request.args.get('Authorization') == self.client.secret_key:
                        return sanic.response.json({'status':'failed', 
                         'error_code':'Unauthorized', 
                         'error_message':'The secret key is missing or invalid!'},
                          status=401)
                return await f(request, *args, **kwargs)

            return decorated_function

        return decorator
# okay decompiling __init__.pyc