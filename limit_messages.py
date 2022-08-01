import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, *args):
        pass
        # print('Message from {0.author}: {0.content}'.format(message))

    async def on_typing(self, *args):
        pass

client = MyClient()
client.run()