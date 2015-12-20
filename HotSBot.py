import asyncio
import discord
import re
import datetime
import youtube_dl
import pafy

try:
    import creds
except:
    print("Need valid creds.py to login")
    exit()

isPlaying = False
firstTime = True

helpmessage = '`!flair [play style] [region]` - select a role and the bot will do the rest of the work!\n'
helpmessage += 'I can accept more than one input for each category as long as they\'re properly spaced! \nI currently understand these play styles: ***\"Competitive (or Comp)\" and \"Casual\"*** '
helpmessage += '\nI currently understand these region names: ***\"NA\" \"EU\" and \"ASIA\"***!\n'
helpmessage += '\n\n`!flair remove` - too many roles? Move across the world? Run this command to start fresh!'
#helpmessage += '\n\n`!play [youtube link]` - HotSBot is now playing music! just link your favorite youtube video containing music and it\'ll be added to the playlist!'
helpmessage += '\n\nEXAMPLES:\n  `!flair comp NA` \n  `!flair casual NA ASIA`'

lockroles = ["Moderator", "Competitive Manager"]

playlist = []


client = discord.Client()

@client.async_event
def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print('--Server List--')
    for server in client.servers:
        print(server.name)
@client.async_event
def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    if '!flair' in message.content.lower() or '!flare' in message.content.lower():
        roleset = False
        doit = True
        roles_to_be_added = []
        print(' role is true')
        for role in message.author.roles:
            if role.name in lockroles:
                doit = False
        if 'remove' in message.content.lower() and doit:
            yield from client.replace_roles(message.author,client.servers[0].roles[0])
            roleset = True
            print('setting ' + message.author.name + ' to have no class')
        if 'comp player' in message.content.lower() or 'competitive' in message.content.lower() or 'comp' in message.content.lower() and doit:
            if 'na' in message.content.lower():
                roles_to_be_added.append(discord.utils.get(client.servers[0].roles, name='Competitive Player NA'))
                print('got past it! NA Comp')
                roleset = True
            if 'eu' in message.content.lower():
                roles_to_be_added.append(discord.utils.get(client.servers[0].roles, name='Competitive Player EU'))
                print('got past it! EU Comp')
                roleset = True
            if 'asia' in message.content.lower():
                roles_to_be_added.append(discord.utils.get(client.servers[0].roles, name='Competitive Player ASIA'))
                print('got past it! ASIA comp')
                roleset = True
        if 'casual player' in message.content.lower() or 'casual' in message.content.lower() and doit:
            if 'na' in message.content.lower():
                roles_to_be_added.append(discord.utils.get(client.servers[0].roles, name='Casual Player NA'))
                print('got past it! NA Cas')
                roleset = True
            if 'eu' in message.content.lower():
                roles_to_be_added.append(discord.utils.get(client.servers[0].roles, name='Casual Player EU'))
                print('got past it! EU Cas')
                roleset = True
            if 'asia' in message.content.lower():
                roles_to_be_added.append(discord.utils.get(client.servers[0].roles, name='Casual Player ASIA'))
                print('got past it! ASIA Cas')
                roleset = True
        if roleset:
            yield from client.delete_message(message)
            if roles_to_be_added: yield from client.add_roles(message.author, *roles_to_be_added)
    elif message.content.startswith('!help'):
        helpmsg = yield from client.send_message(message.channel, helpmessage)
        yield from asyncio.sleep(30)
        yield from client.delete_message(message)
        yield from client.delete_message(helpmsg)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(client.login(creds.discordid, creds.discordpw))
    loop.run_until_complete(client.connect())
except Exception:
    loop.run_until_complete(client.close())
finally:
    loop.close()
