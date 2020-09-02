import os
import pickle
import time

from twitchio.ext import commands

from pickledqueue import Queue

bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

with open("my_saved_queue.obj", "rb") as queue_save_file:
    my_queue: Queue = pickle.load(queue_save_file)


def save():
    with open("my_saved_queue.obj", "wb+") as queue_save_file:
        pickle.dump(my_queue, queue_save_file)


#save()


@bot.event
async def event_ready():
    print(f"{os.environ['BOT_NICK']} is online!")
    #ws = bot._ws
    #await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    await bot.handle_commands(ctx)

    # await ctx.channel.send(ctx.content)

    if ctx.author.name.lower() == "realmaniox".lower():
        if 'heisann' in ctx.content.lower():
            await ctx.channel.send(f"Halla, @{ctx.author.name}!")
        return


@bot.command(name='test')
async def test(ctx):
    await ctx.send('Nei du')


@bot.command(name='recentadd')
async def recentadd(ctx):
    if ctx.author.is_mod:
        try:
            my_queue.add(ctx.content[11:])
            my_queue.check()
            print(my_queue.queue)
            save()
        except Exception as e:
            print(e)
    else:
        return


@bot.command(name='recent')
async def recent(ctx):
    try:
        for i in my_queue.queue:
            await ctx.send(i)
        time.sleep(300)
    except Exception as e:
        print(e)


@bot.command(name='hallgeir')
async def recent(ctx):
    try:
        await ctx.channel.send(f"Hei, @{ctx.author.name}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    bot.run()
