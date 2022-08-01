# limit-messages-by-period-discord-bot

###features

####roll dice
Users can post __roll_die@N__ in any channel and the bot will post back the roll result. Valid __N__'s are 4, 6, 8, 10, 12, 20, or 100.

####user timeout
This will allow only a single post in a specific channel per user in a 24 hour period.

I use this for a mini-game channel that allows my members one chance to guess the answer every 24 hours.

###environment variables 
####client_token
The token for your app, https://discord.com/developers/applications
####guild_name (used by user timeout)
The name of your server.
####channel_name (used by user timeout)
The channel that will timeout users. Defaults to _general_
####role_name (used by user timeout)
Only apply timeout to users in this role. Defaults to _@everyone_
