# Discord NFT bot
NFT bot for Discord, uses slash commands with a clear prompt.

### Commands
`/floor`
Get the floor price from OpenSea

`/stats`
Get collection sales information from OpenSea.

`/token {token_number}`
Get the traits and image for the reqested token.



## Setup Guide

### Create Your Bot - Discord Setup Guide
https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot


### Discord Server Token
1. In discord, click the gear icon next to your username
1. Select Advanced from the left nav menu
1. Trun on developer mode
1. Go to the server you want to add the bot to
1. Click the down arrow next to the Server's name
1. Select Server Settings -> Widget
1. Copy the Server ID

### Registering Slash Commands
TODO


### Bot Server Setup

Install pip
`sudo apt install python3-pip`

Install discord.py
`python3 -m pip install -U discord.py`

Install discord_slash.py
`pip3 install -U discord-py-slash-command`
