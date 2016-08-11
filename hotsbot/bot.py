import asyncio
import discord

helpmessage = '`!region [region]` - select a region or regions and the bot will do the rest of the work!\n'
helpmessage += 'I can accept more than one input for each category as long as they\'re properly spaced!'
helpmessage += '\nI currently understand these region names: ***\'NA\' \'EU\' and \'ASIA\'***!\n'
helpmessage += '\n\n`!region remove` - too many roles? Move across the world? Run this command to start fresh!'
helpmessage += '\n\nEXAMPLES:\n  `!region NA` \n  `!region NA ASIA`'


class HotSBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = '!'
        self.lockroles = ['85625338150817792', '137975812858052608', '136291402719035393']
        self.token = 'token'
        print('end of init')

    # noinspection PyMethodOverriding
    def run(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.start(self.token))
            loop.run_until_complete(self.connect())
        except Exception:
            loop.run_until_complete(self.close())
        finally:
            loop.close()

    async def on_ready(self):

        print('Connected!\n')
        print('Username: ' + self.user.name)
        print('ID: ' + self.user.id)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == self.user:
            return
        if message.channel.is_private:
            return
        if message.author.id == '135288293548883969':
            return
        if '!restart' in message.content.lower() and message.author.id == '77511942717046784':
            self.logout()
        if '!region' in message.content.lower():
            if message.content.lower() == '!region':
                helpmsg = await self.send_message(message.channel, helpmessage)
                await asyncio.sleep(30)
                await self.delete_message(message)
                await self.delete_message(helpmsg)
            if 'remove' in message.content.lower() and not [role for role in message.author.roles if role.id in self.lockroles]:
                await self.replace_roles(message.author)
                print('setting ' + message.author.name + ' to have no class')
            else:
                if 'na' in message.content.lower():
                    await self.add_roles(message.author, *[discord.utils.get(message.server.roles, id='125001205561688064')])
                    print('got past it! NA')
                if 'eu' in message.content.lower():
                    await self.add_roles(message.author, *[discord.utils.get(message.server.roles, id='125009932687769600')])
                    print('got past it! EU')
                if 'asia' in message.content.lower():
                    await self.add_roles(message.author, *[discord.utils.get(message.server.roles, id='125009993102524417')])
                    print('got past it! ASIA')
            await self.delete_message(message)
        elif message.content.startswith('!help'):
            helpmsg = await self.send_message(message.channel, helpmessage)
            await asyncio.sleep(30)
            await self.delete_message(message)
            await self.delete_message(helpmsg)

if __name__ == '__main__':
    bot = HotSBot()
    bot.run()
