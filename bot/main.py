import subprocess
import sys
import dbm
import discord
from discord.ext import commands
from discord import Game
from py_expression_eval import Parser
from requests import get
from random import randrange
from state import State
from constants import *

bot = commands.Bot(command_prefix='!')
state = State()
parser = Parser()


@bot.event
async def on_ready():
    print(f"Successfully logged in as: {bot.user}")
    await bot.change_presence(activity=Game("Ur Mom"))
    message = "I have risen!"
    if state.updated:
        message = "Updated!"

    if state.channelId is not None:
        await bot.get_channel(state.channelId).send(f"{message} Last sent value was: {state.score}")


@bot.command()
@commands.has_role("Zircanian Tech Support")
async def channel(ctx):
    state.setChannel(ctx.channel.id)
    await ctx.send(f"I will only listen in {ctx.channel.name}")
    pass


@bot.command()
@commands.has_role("Zircanian Tech Support")
async def role(ctx, name, name2):
    state.role = name + " " + name2
    await ctx.send("Set fail role to: " + name)
    pass


@bot.command()
@commands.has_role("Zircanian Tech Support")
async def update(ctx):
    await ctx.send("Updating!")
    subprocess.call(["sh", "./update.sh"])
    quit(0)


@bot.command()
async def score(ctx):
    if ctx.channel.id == state.channelId:
        await ctx.send("High Score: " + state.highestScore.__str__())
    pass


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        if message.channel.id == state.channelId:
            content = message.content.__str__().replace("\'", "").replace("\"", "")
            math = parser.parse(content).evaluate({})

            if (math == state.score + 1 or (state.score + 1 == 21 and "9+10" in message.content)) and state.lastAuthor != message.author.name:
                state.incrementScore()
                state.setLastAuthor(message.author.name)

                if state.score > state.highestScore:
                    await message.add_reaction("☑️")
                else:
                    await message.add_reaction("✅")
            else:
                random = randrange(0, 100)
                if random == 1:
                    await message.channel.send("Im gonna pretend I didn't see that")
                else:
                    state.resetScore()

                    member = message.author
                    failRole = discord.utils.get(message.guild.roles, name=state.role)
                    member.add_role(failRole)

                    await message.add_reaction("❌")
                    await message.channel.send(message.author.mention + " " + get("https://evilinsult.com/generate_insult.php").text)
                    await message.channel.send("Score set back to 0")
    finally:
        await bot.process_commands(message)
        return


@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return

    if message.channel.id == state.channelId:
        await message.channel.send("Message deleted")

    try:
        if message.channel.id == state.channelId:
            content = message.content.__str__().replace("\'", "").replace("\"", "")
            math = parser.parse(content).evaluate({})
            await message.channel.send(message.author.mention + " deleted their message! Last number was: " + math.__str__())
    finally:
        return

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "updated":
            state.updated = True

    with dbm.open("bot_state", "c") as data:
        if "score" not in data:
            state.save()

        state.score = int(data["score"])
        state.highestScore = int(data["highestScore"])
        state.channelId = int(data["channelId"])
        state.role = data["role"]

    bot.run(DISCORD_BOT_TOKEN)
