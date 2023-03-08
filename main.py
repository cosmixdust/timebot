from discord import app_commands
import discord
import time
from discord.ext import commands, tasks

intents = discord.Intents(
    messages= True,
    message_content= True
)

bot = commands.Bot(command_prefix="!", intents=intents)

class TimeLoop:
    def __init__(self):
        self.now = 0
        self.loop = tasks.loop(seconds=1)(self.update_time)

    async def update_time(self):
        self.now = int(time.time())

    async def start(self):
        self.loop.start()

time_loop = TimeLoop()

@bot.event
async def on_ready():
    print('Tick, tock...')
    await bot.change_presence(activity=discord.Game('with the clock.'))
    await time_loop.start()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name='time', description='what time is it?')
async def timeNow(interaction: discord.Interaction):
    await interaction.response.send_message('It is currently <t:{}:F>.'.format(time_loop.now))

@bot.tree.command(name='set-time', description='set a day for it to be seen as unix timestamp!')
@app_commands.describe(date_selected='Type here your date! Use YYYY-MM-DD HH:MM:SS format!')
async def setTime(interaction: discord.Interaction, date_selected: str):
    try:
        unix_time = time.mktime(time.strptime(date_selected, '%Y-%m-%d %H:%M:%S'))
        await interaction.response.send_message('Your date is: <t:{}:F>'.format(int(unix_time)))
    except Exception as e:
        await interaction.response.send_message('Sorry, but {} does not match the format!'.format(date_selected), ephemeral=True)

fileToken = open("token.txt", "r")
token = fileToken.read()
bot.run(token)