import asyncio
import aiohttp
import json

async def bot_info(id):
  async with aiohttp.ClientSession() as session:
      async with session.get(f'https://infinitybotlist.com/api/bots/{id}/info') as r:
        data = await r.json()
  class infoClass:
        def __init__(self, data):
          if data["error"] == False:
            self.bot_name = data["bot_name"]
            self.certified = data["certified"]
            self.tags = data["tags"]
            self.prefix = data["prefix"]
            self.owner = data["owner"]
            self.library = data["library"]
            self.short_desc = data["short_desc"]
            self.servers = data["servers"]
            self.shards = data["shards"]
            self.votes = data['votes']
            self.website = data["website"]
            self.donate = data["donate"]
            self.support = data["support"]
            self.staff = data["staff"]
            self.error = None
          else:
            self.bot_name = self.certified = self.tags = self.prefix = self.owner = self.library = self.short_desc = self.servers = self.shards = self.votes = self.website = self.donate = self.support = self.staff = "Undefined"
            self.error = data["error"]

  return infoClass(data)

async def user_info(id):
  async with aiohttp.ClientSession() as session:
      async with session.get(f'https://infinitybotlist.com/api/users/{id}') as r:
        data = await r.json()
  class infoClass:
        def __init__(self, data):
          if data["error"] == False:
            self.username = data["username"]
            self.about = data["about"]
            self.certified_dev = data["certified_dev"]
            self.staff = data["staff"]
            self.developer = data["developer"]
            self.error = data["error"]
          else:
            self.username = self.about = self.certified_dev = self.staff = self.developer = "Undefined"
            self.error = data["error"]
  return infoClass(data)


async def post_stats(id, auth_token, servers, shards=0):
  url = f"https://infinitybotlist.com/api/bots/{id}"
  headers = {"authorization":auth_token, "Content-Type":"application/json"}
  async with aiohttp.ClientSession(headers=headers) as session:
    async with session.post(url,json={"servers":servers, "shards":shards}) as r:
      try:
        if r.status == 200:
          js = await r.json()
          return js
        else:
          raise ConnectionError
      except ConnectionError:
        return "ConnectionRefused"