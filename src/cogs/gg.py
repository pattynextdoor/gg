import discord
import random
import urllib.request
from discord.ext import commands

class GGBot(commands.Cog):
    SPARRING_PARTNERS = 719403144190230648
    ARENAID_TRUNC_LEN = 10

    def __init__(self, client):
        self.client = client
        self.banned_set = set()
        self.arena_id = ''

    @commands.Cog.listener()
    async def on_ready(self):
        uname = self.client.user.name
        uid = self.client.user.id
        print(f'Initialized {uname} with id {uid}')

    @commands.command()
    async def arenaid(self, ctx, *args):
        if not args:
            if not self.arena_id:
                await ctx.send('Arena ID not currently set.')
            else:
                await ctx.send(self.arena_id)
        elif args[0] == 'clear':
            self.arena_id = ''
            await ctx.send('Arena ID cleared.')
        else:
            message = ctx.message.content[self.ARENAID_TRUNC_LEN:]
            self.arena_id = message
            await ctx.send(f'Arena ID set to \"{self.arena_id}\"')

    @commands.command()
    async def hiba(self, ctx, *args):
        channel_from = ctx.message.channel.id
        url = 'http://shibe.online/api/shibes'

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            await ctx.send(response.read()
                                   .decode("utf-8")
                                   .strip("[\"\"]"))

    @commands.command()
    async def lexi(self, ctx, *args):
        lexi_dog_pics = [
            "https://cdn.discordapp.com/attachments/738239982489174047/739628777440673812/image0.jpg",
            "https://cdn.discordapp.com/attachments/738239982489174047/739628777767960656/image1.jpg",
            "https://cdn.discordapp.com/attachments/738239982489174047/739628778069688380/image2.jpg",
            "https://cdn.discordapp.com/attachments/738239982489174047/739628778355163197/image3.jpg",
            "https://cdn.discordapp.com/attachments/738239982489174047/739628778707222588/image4.jpg",
            "https://cdn.discordapp.com/attachments/738239982489174047/739628778896228392/image5.jpg"
        ]

        await ctx.send(random.choice(lexi_dog_pics))


    @commands.command()
    async def ban(self, ctx, *args):
        await ctx.send(f'{args[0]} removed from the rankings forever.')

    @commands.command()
    async def saygg(self, ctx, *args):
        await ctx.send('gg! <:Corrinsmug:733995137126105158> ')

    @commands.command()
    async def gg(self, ctx, *args):
        
        def __get_sparring_partners_channel():
            return self.client.get_channel(self.SPARRING_PARTNERS)

        def isGG(msg):
            msg_lc = msg.lower()
            return 'gg' in msg_lc

        def generateMessage(map):
            msg = """```"""
            index = 1
            for entry in gg_map_sorted:
                author = entry[0]
                message_count = str(entry[1])

                msg += f"{str(index)}. {author}: {message_count} gg's\n"
                index += 1

            msg += "```"
            return msg

        await ctx.send(f'Calculating gg instances...')

        sp_channel = __get_sparring_partners_channel()
        gg_map = {}
        messages = await sp_channel.history(limit=None).flatten()

        for msg in messages:
            if isGG(msg.content):
                msg_author = msg.author.name
                
                if msg_author in gg_map.keys():
                    gg_map[msg_author] += 1
                else:
                    gg_map[msg_author] = 1

        gg_map_sorted = sorted(gg_map.items(),
                                key=lambda x: x[1],
                                reverse=True)

        outgoing_message = generateMessage(gg_map_sorted)

        await ctx.send(outgoing_message)

def setup(client):
    client.add_cog(GGBot(client))