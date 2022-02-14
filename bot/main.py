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

    if state.channelId != 0:
        await bot.get_channel(state.channelId).send(f"{message} Last sent value was: {state.score}")


@bot.command()
@commands.has_role("Zircanian Tech Support")
async def channel(ctx):
    state.setChannel(ctx.channel.id)
    await ctx.send(f"I will only listen in {ctx.channel.name}")
    pass


@bot.command()
@commands.has_role("Zircanian Tech Support")
async def role(ctx, id):
    state.setRole(id)
    await ctx.send(f"Set fail role to: {id}")
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
        await ctx.send(f"High Score: {state.highestScore}")
    pass


@bot.command()
async def swap(ctx):
    if ctx.channel.id == state.channelId:
        if state.amountSinceLastSwitch < 1:
            if state.direction == 1:
                state.setDirection(-1)
            else:
                state.setDirection(1)
            await ctx.send("Count direction has swapped!")
        else:
            await ctx.send("Too soon!")
    pass


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        if message.channel.id == state.channelId:
            content = message.content.__str__().replace("\'", "").replace("\"", "")
            math = parser.parse(content).evaluate({})

            if (math == state.score + state.direction or (state.score + state.direction == 21 and "9+10" == message.content)) and state.lastAuthor != message.author.name:
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

                    await message.add_reaction("❌")
                    await message.channel.send(f"{message.author.mention} {get('https://evilinsult.com/generate_insult.php').text}")
                    await message.channel.send("Score set back to 0 and count direction reset")

                    if state.roleId != 0:
                        member = message.author
                        failRole = discord.utils.get(message.guild.roles, id=state.roleId)
                        await member.add_role(failRole)
    finally:
        await bot.process_commands(message)
        return


@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return

    try:
        if message.channel.id == state.channelId:
            content = message.content.__str__().replace("\'", "").replace("\"", "")
            math = parser.parse(content).evaluate({})

            if math == state.score:
                await message.channel.send(f"{message.author.mention} deleted their message! Last number was: {math}")
    finally:
        return

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "updated":
            state.updated = True

    with dbm.open("bot_state", "c") as data:
        if "score" not in data:
            data["score"] = state.score.__str__()
            data["highestScore"] = state.highestScore.__str__()
            data["channelId"] = state.channelId.__str__()
            data["role"] = state.roleId.__str__()
        else:
            state.score = int(data["score"])
            state.highestScore = int(data["highestScore"])
            state.channelId = int(data["channelId"])
            state.roleId = int(data["role"])

    bot.run(DISCORD_BOT_TOKEN)
