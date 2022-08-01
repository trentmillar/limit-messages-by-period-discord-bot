import discord
import os
import sys
import re
import logging
import random
from datetime import datetime, timedelta

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s - %(message)s")
logging.getLogger("py.warnings").setLevel(logging.ERROR)
logging.captureWarnings(True)

guild_name = os.environ.get("guild_name").lower()
channel_name = os.environ.get("channel_name").lower() if os.environ.get("channel_name") else "general"
role_name = os.environ.get("role_name").lower() if os.environ.get("role_name") else "@everyone"
client_token = os.environ.get("client_token")
id = None


class BotClient(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents)

    async def on_ready(self):
        logging.debug('logged on as {0}'.format(self.user))

        self.bot_guild = [g for g in self.guilds if g.name.lower() == guild_name][0]

        yesterday = datetime.now() - timedelta(days=1)
        for channel in client.get_all_channels():
            if channel.name.lower() == channel_name:
                id = channel.id
                break

        if not id:
            error_message = "could not find channel, {0}".format(channel_name)
            logging.error(error_message)
            raise error_message

        channel = client.get_channel(id)

        """
        Set send message on all role members
        """
        valid_users = [c for c in channel.members if
                       not c.bot and not c.guild_permissions.administrator and [r for r in c.roles if
                                                                                r.name.lower() == role_name]]

        for user in valid_users:
            channel.set_permissions(user, read_messages=True, send_messages=True)

        timeout_users = []
        async for msg in channel.history(after=yesterday):
            if not msg.author.id in [u.id for u in valid_users]:
                continue
            logging.debug("user {0} will time out".format(msg.author.name))
            timeout_users.append(msg.author.id)

        for tou in set(timeout_users):
            user = client.get_user(tou)
            logging.info("{0} timing out".format(user.name))
            await channel.set_permissions(user, read_messages=True, send_messages=False)

    async def on_message(self, message):
        logging.info('Message from {0.author}: {0.content}'.format(message))

        channel = message.channel

        """
        handlers
        """
        def help(content):
            logging.debug("help handler")
            return ["""Here is what Dungeon Joe does,
                
                1) You can roll a dice using "roll_die@N" where N can be any of; 4, 6, 8, 10, 12, 20, or 100.
                2) In the "riddle" channel, you are only allowed one message per 24 hour period. Don't waste your guess."""]

        def roll_die(content):
            logging.debug("roll die handler")
            response = []
            for result in [int(d) for d in re.findall("roll_die@([0-9]{1,3})", content, re.IGNORECASE & re.MULTILINE)]:
                if result in [4, 6, 8, 10, 12, 20, 100]:
                    roll = random.randint(1, result)
                    response.append("d{0} rolled {1}".format(result, roll))
                else:
                    response.append("Unknown die {0}".format(result))
            return response

        """
        process
        """
        content = message.content.lower()
        tokens = {
            "roll_die@": roll_die,
            "help@joe": help,
        }
        for key in tokens.keys():
            if key in content:
                for result in tokens[key](content):
                    await message.channel.send(result)

    async def on_typing(self, *args):
        logging.info("{0} is typing in {1} at {2}".format(args[0], args[1], args[2]))


client = BotClient()
client.run(client_token)
