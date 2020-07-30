import discord
from discord.ext import commands

class GGBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        uname = self.client.user.name
        uid = self.client.user.id
        print(f'Initialized {uname} with id {uid}')

    @commands.command()
    async def gg(self, ctx, *args):

        # TODO: Implement the damn thing
        return False

def setup(client):
    client.add_cog(GGBot(client))