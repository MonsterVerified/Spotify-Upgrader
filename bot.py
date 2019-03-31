import discord
from discord.ext.commands import Bot
import asyncio, json, requests
import random
from bs4 import BeautifulSoup
import os, time, re, subprocess
with open('config.json') as (f):
    data = json.load(f)
TOKEN = data['token']
BOT_PREFIX = data['prefix']
client = Bot(command_prefix=BOT_PREFIX)

def grab_accounts(US, GB, DE, CA, CH, FR, SE):
    f = open('Accounts/US.txt', 'r')
    for line in f:
        clean = line.split('\n')
        US.append(clean[0])

    f.close()
    f = open('Accounts/GB.txt', 'r')
    for line in f:
        clean = line.split('\n')
        GB.append(clean[0])

    f.close()
    f = open('Accounts/DE.txt', 'r')
    for line in f:
        clean = line.split('\n')
        DE.append(clean[0])

    f.close()
    f = open('Accounts/CA.txt', 'r')
    for line in f:
        clean = line.split('\n')
        CA.append(clean[0])

    f = open('Accounts/CH.txt', 'r')
    for line in f:
        clean = line.split('\n')
        CH.append(clean[0])

    f = open('Accounts/FR.txt', 'r')
    for line in f:
        clean = line.split('\n')
        FR.append(clean[0])

    f = open('Accounts/SE.txt', 'r')
    for line in f:
        clean = line.split('\n')
        SE.append(clean[0])


    f.close()


@client.event
async def on_ready():
    print('Ready')


@client.command(pass_context=True)
async def redeem(ctx, arg1, arg2):
    allowed_countries = ['US', 'GB', 'DE', 'CA', 'CH', 'FR', 'SE']
    accounts = []
    keys = []
    country = arg1.upper()
    if country in allowed_countries:
        f = open('Accounts/' + str(country) + '.txt', 'r')
        for line in f:
            clean = line.split('\n')
            accounts.append(clean[0])

        f.close()
    if country not in allowed_countries:
        return await (client.say('Sorry But the Country you Specified is Not Currently Offered'))
    else:
        check = re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)')
        mat = check.match(str(arg2))
        if mat:
            result = None
            while result != ',"success":true}':
                if len(accounts) == 0:
                    await client.say('Sorry We Are Out of Stock on That Country')
                    os.remove('Accounts/' + str(country) + '.txt')
                    f = open('Accounts/' + str(country) + '.txt', 'a')
                    for ELEM in accounts:
                        f.write(ELEM + '\n')

                    f.close()
                    break
                account = accounts.pop()
                account = random.choice(accounts)
                combo = account.split(':')
                USER = combo[0]
                PASS = combo[1]
                try:
                    with requests.Session() as (c):
                        url = 'https://accounts.spotify.com/en/login?continue=https:%2F%2Fwww.spotify.com%2Fint%2Faccount%2Foverview%2F'
                        headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
                        page = c.get(url, headers=headers)
                        CSRF = page.cookies['csrf_token']
                        headers = {'Accept':'*/*',  'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',  'Referer':'https://accounts.spotify.com/en/login/?continue=https:%2F%2Fwww.spotify.com%2Fus%2Fgooglehome%2Fregister%2F&_locale=en-US'}
                        url = 'https://accounts.spotify.com/api/login'
                        login_data = {'remember':'true',  'username':USER,  'password':PASS,  'csrf_token':CSRF}
                        cookies = dict(__bon='MHwwfC0xNDAxNTMwNDkzfC01ODg2NDI4MDcwNnwxfDF8MXwx')
                        login = c.post(url, headers=headers, data=login_data, cookies=cookies)
                        if '{"displayName":"' in login.text:
                            url = 'https://www.spotify.com/us/account/overview/'
                            capture = c.get(url, headers=headers)
                            csr = capture.headers['X-Csrf-Token']
                            url = 'https://www.spotify.com/us/family/api/master-invite-by-email/'
                            headers = {'Accept':'*/*',  'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',  'x-csrf-token':csr}
                            login_data = {'firstName':'thomas',  'lastName':'Payne',  'email':arg2}
                            invite = c.post(url, headers=headers, json=login_data)
                            print(invite.text)
                            if '"success":true}' in invite.text:
                                await client.say('Success, check your email')
                                f.close()
                                break
                            if 'message":"Invite limit reached' in invite.text:
                                result = None
                                return await(client.say('Invite limit reached. Please try again'))
                                accounts.pop()
                            if 'message":"No family plan found for user' in invite.text:
                                result = None
                                return await(client.say('No plan found please try again'))
                                accounts.pop()
                        if '{"error":"errorInvalidCredentials"}' in login.text:
                            result = None
                            return await(client.say('Invalid account was used from the DB please try again'))
                            accounts.pop()
                except:
                    pass

        if not mat:
            return await (client.say('Sorry But an Invalid Email Was Given'))


@client.command()
async def stock():
    US_stock = []
    GB_stock = []
    DE_stock = []
    CA_stock = []
    CH_stock = []
    FR_stock = []
    SE_stock = []
    grab_accounts(US_stock, GB_stock, DE_stock, CA_stock, CH_stock, FR_stock, SE_stock)
    embed = discord.Embed(title='Stock',
      colour=discord.Colour.blue())
    embed.set_author(name='Inviter Bot', icon_url='https://cdn.discordapp.com/avatars/513839414322135062/b759fed29c2186046bfd6b7eff0bba5f.webp?size=128')
    embed.add_field(name='US', value=len(US_stock), inline=True)
    embed.add_field(name='GB', value=len(GB_stock), inline=True)
    embed.add_field(name='DE', value=len(DE_stock), inline=True)
    embed.add_field(name='CA', value=len(CA_stock), inline=True)
    embed.add_field(name='CH', value=len(CH_stock), inline=True)
    embed.add_field(name='FR', value=len(FR_stock), inline=True)
    embed.add_field(name='SE', value=len(SE_stock), inline=True)
    await client.say(embed=embed)



client.run(TOKEN)
