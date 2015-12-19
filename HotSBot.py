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
    if '!play' in message.content.lower():
            discord.opus.load_opus('libopus-0.dll')
            global firstTime
            msg = message.content
            msg2 = msg
            substrStart = msg.find('!play') + 6
            msg = msg[substrStart: ]
            msg.strip()
            if message.author.id == '77511942717046784':
                timer = message.content
                timer = timer[ :msg2.find('!play')]
                timer = timer.replace(' ', '')
                channel = discord.utils.get(message.server.channels, name=timer)
                vce = yield from client.join_voice_channel(channel)
                firstTime = False
            else:
                yield from client.send_message(message.channel,'Hi! I\'m currently disconnected for unknown reasons! Alert Rhino and he\'ll get me back ASAP!')
            playlist.append(msg)
            yield from client.delete_message(message)
            
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
        
@asyncio.coroutine
def some_task():
    global isPlaying
    global firstTime
    yield from client.wait_for_ready()
    while not client.is_closed:
        if isPlaying is False and firstTime is False:
            print('ding')
            vce = client.voice
            thing = playlist[0]
            player = vce.create_ytdl_player(thing)
            isPlaying = True
            player.start()
            video = pafy.new(thing)
            while thing in playlist: playlist.remove(thing)
            yield from asyncio.sleep(video.length)
            player.stop()
            isPlaying = False
        else:
            print('dong')
            yield from asyncio.sleep(1)


loop = asyncio.get_event_loop()
try:
    loop.create_task(some_task())
    loop.run_until_complete(client.login(creds.discordid, creds.discordpw))
    loop.run_until_complete(client.connect())
except Exception:
    loop.run_until_complete(client.close())
finally:
    loop.close()
