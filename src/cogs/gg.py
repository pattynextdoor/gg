import discord
from discord.ext import commands

class GGBot(commands.Cog):
    SPARRING_PARTNERS = 719403144190230648

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        uname = self.client.user.name
        uid = self.client.user.id
        print(f'Initialized {uname} with id {uid}')

    @commands.command()
    async def ban(self, ctx, *args):
        await ctx.send(f'{args[0]} removed from the rankings forever.')

    @commands.command()
    async def gg(self, ctx, *args):
        def __get_sparring_partners_channel():
            return self.client.get_channel(self.SPARRING_PARTNERS)

        def isGG(msg):
            msg_lc = msg.lower()
            return 'gg' in msg_lc

        channel_from = ctx.message.channel.id
        message_author = ctx.message.author

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

        outgoing_message = """```"""
        index = 1
        for entry in gg_map_sorted:
            author = entry[0]
            message_count = str(entry[1])

            outgoing_message += f"{str(index)}. {author}: {message_count} gg's\n"
            index += 1

        outgoing_message += "```"
        await ctx.send(outgoing_message)

def setup(client):
    client.add_cog(GGBot(client))