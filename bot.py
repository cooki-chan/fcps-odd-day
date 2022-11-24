import discord
from discord import app_commands
from discord.ext import tasks
import time
import requests
import icalendar
import requests
from datetime import datetime, date, timedelta

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
busChannel = CHANNEL ID
guild = GUILD ID

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild))
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name="what the fuck man"))
    creeper.start()

@tasks.loop(minutes=1)
async def creeper():
    time = datetime.today()
    #if time.hour == 7 and time.minute == 00:
    if True:
        await client.get_channel(busChannel).send(embed=buildEmbed())

@tree.command(name = "today", description = "What day is today?", guild=discord.Object(id=guild))
async def today(ctx):
    await ctx.response.send_message(embed = buildEmbed())

@tree.command(name = "tommorow", description = "How about tommorow?", guild=discord.Object(id=guild))
async def today(ctx):
    await ctx.response.send_message(embed = buildEmbed(date.today() + timedelta(days=1)))

@tree.command(name = "day", description = "How about tommorow?", guild=discord.Object(id=guild))
async def today(ctx, days_from_now: int = 0):
    await ctx.response.send_message(embed = buildEmbed(date.today() + timedelta(days=days_from_now)))

def buildEmbed(date:date = date.today()):
    status = getDay(date)

    if status == None:
        embedVar = discord.Embed(title=f":x: No School!", description=f"{date.strftime('%a, %b %d')}", color=0x00ffff)
        embedVar.add_field(name=f"Enjoy your day off!", value="made with love by cookie! :sparkles:", inline=False)
        return embedVar
    if status == "Even Day":
        embedVar = discord.Embed(title=f":two: :four: :six: :eight: Even Day!", description=f"{date.strftime('%a, %b %d')}", color=0x00ffff)
        embedVar.add_field(name="Even Day today, no 3rd period", value="made with love by cookie! :sparkles:", inline=False)
        return embedVar

    embedVar = discord.Embed(title=f":one: :three: :five: :seven: Odd Day!", description=f"{date.strftime('%a, %b %d')}", color=0x00ffff)
    embedVar.add_field(name=f"Odd Day: {status}", value="made with love by cookie! :sparkles:", inline=False)
    return embedVar

def getDay(date:date = date.today()):
    file = requests.get("http://www.calendarwiz.com/CalendarWiz_iCal.php?crd=wtw22-23").content.decode("utf-8")
    gcal = icalendar.Calendar.from_ical(file)

    events = []
    iter = 0
    for i in gcal.walk():
        events.append(i)
        iter+=1

    for i in range(1, iter - 1):
        dt = events[i].decoded("DTSTART")
        event = events[i]
        print(dt)
        print(type(dt))
        print(date)
        print(type(date))

        if(type(event.decoded("DTSTART")) == datetime):
            dt = event.decoded("DTSTART").date()

        if dt == date and event["CATEGORIES"].to_ical() == b"3rd Period":
            print(i)
            print(event.content_lines())
            print(event.decoded("SUMMARY").decode('utf-8'))
            return event.decoded("SUMMARY").decode('utf-8')
        elif dt == date and event["CATEGORIES"].to_ical() == b"Even Day":
            print(i)
            print(event.content_lines())
            print(event.decoded("SUMMARY").decode('utf-8'))
            return "Even Day"
    return None


client.run('BOT KEY')
