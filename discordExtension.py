drivingcentre.comfrom discord.ext import commands, tasks
import threading
from findPracticals import *
import asyncio
from random import randint
from pass_from_config import get_cred, get_token, get_captcha
import pytz

bot = commands.Bot(command_prefix='$')
dict = {'W': 'None', 'A': 'None', 'T': '', 'F': ''}
switch = True
pwd = ''
token = get_token()

@bot.command()
async def ping(ctx, args=''):
    await ctx.send(f'```Pong! {args} ```')


@bot.command()
async def query(ctx, args=''):
    global switch, pwd, username, client
    # client = requests.Session()
    login(client, pwd, username)
    flag = main_scanner(client, dict, filter=args, username=username)

    if flag:
        #d = datetime.datetime.now()
        #s = d.astimezone(sg)
        await ctx.send(
	'```' + dict['F'] + '\nLocation_A: ' + dict['W'] + '\nLocation_B: ' + dict['A'] + '\nRecorded on ' +
	dict['T']+'```')


@bot.command()
async def start(ctx, args=''):
    global switch, pwd, username
    switch = True
    client = requests.Session()
    login(client, pwd, username)
    sg = pytz.timezone('Asia/Singapore')
    while switch:
        this_r = randint(30, 60)
        flag = main_scanner(client, dict, filter=args, username=username)
        if flag:
            d = datetime.datetime.now()
            s = d.astimezone(sg)
            await ctx.send(
                '```' + dict['F'] + '\nLocation_A: ' + dict['W'] + '\nLocation_B: ' + dict['A'] + '\nRecorded on ' +
                dict['T'] + f'\n\nNext scan in {this_r} mins\nat {datetime.datetime.fromtimestamp(s.timestamp() + (60 * this_r)).strftime("%d %b %y, %I:%M%p")}\n' + '```')

        if not switch:
            break

        await asyncio.sleep(60 * this_r)

@bot.command()
async def stop(ctx):
    global switch
    switch = False
    await ctx.send('Stopped monitoring process!')

async def get_req():
    global client
    while True:
    	client.get('https://www.drivingcentre.com.sg/User/Information', verify=False)
    await asyncio.sleep(60*5)


async def default_check():
    global pwd, username, client
    await bot.wait_until_ready()
    channel = bot.get_channel(869133877401235486)
    await channel.send('Bot is online!')
    #client = requests.Session()
    login(client, pwd, username, gCaptcha=get_captcha())
    #sg = pytz.timezone('Asia/Singapore')
    args=''
    while switch:

        this_r = randint(30, 60)
        flag = main_scanner(client, dict, filter=args, username=username)
        if flag:
            d = datetime.datetime.now()
            #s = sg.localize(d)
            await channel.send('```' + dict['F'] + '\nLocation_A: ' + dict['W'] + '\nLocation_B: ' + dict['A'] + '\nRecorded on ' +
                dict['T'] + f'\n\nNext scan in {this_r} mins\nat {datetime.datetime.fromtimestamp(d.timestamp()+(60*60*8) + (60 * this_r)).strftime("%d %b %y, %I:%M%p")}\n' + '```')

        if not switch:
            break

        await asyncio.sleep(60 * this_r)





if __name__ == '__main__':

    username, pwd = get_cred()
    client = requests.Session()
    bot.loop.create_task(get_req())
    bot.loop.create_task(default_check())

    bot.run(token)
