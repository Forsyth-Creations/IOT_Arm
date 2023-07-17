ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/uvicorn/protocols/websockets/websockets_impl.py", line 254, in run_asgi
    result = await self.app(self.scope, self.asgi_receive, self.asgi_send)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 78, in __call__
    return await self.app(scope, receive, send)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/fastapi/applications.py", line 289, in __call__
    await super().__call__(scope, receive, send)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/applications.py", line 122, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/middleware/errors.py", line 149, in __call__
    await self.app(scope, receive, send)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/middleware/cors.py", line 75, in __call__
    await self.app(scope, receive, send)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
    raise exc
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
    await self.app(scope, receive, sender)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 20, in __call__
    raise e
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 17, in __call__
    await self.app(scope, receive, send)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/routing.py", line 718, in __call__
    await route.handle(scope, receive, send)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/routing.py", line 341, in handle
    await self.app(scope, receive, send)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/routing.py", line 82, in app
    await func(session)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/fastapi/routing.py", line 324, in app
    await dependant.call(**values)
  File "/home/forsythcreations/git/IOT_Arm/backend/main.py", line 44, in websocket_endpoint
    message = await websocket.receive_text()
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/websockets.py", line 113, in receive_text
    self._raise_on_disconnect(message)
  File "/home/forsythcreations/git/IOT_Arm/backend/.venv/lib/python3.10/site-packages/starlette/websockets.py", line 105, in _raise_on_disconnect
    raise WebSocketDisconnect(message["code"])
starlette.websockets.WebSocketDisconnect: 1006
INFO:     connection closed