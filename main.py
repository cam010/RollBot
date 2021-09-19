# VERSION 1.0.0 #

# @author Cameron Clarke
# Last Updated 19/9/21


import os
import discord
import random
from datetime import datetime
from keep_alive import keep_alive

token = os.environ['TOKEN']

def get_users(guild):
  file = f"users{guild}.txt"
  with open(file, "r") as f:
      text = f.read()
      users = [x for x in text.split("\n")]
      return users

client = discord.Client()

def log_num(num):
  with open("log.txt", "a") as f:
    now = datetime.now()
    f.write(f"{now}\trolled {num}\n")

def return_str_based_on_range(num):
  if num <= 5:
    return f"u are a legend, you got {num}"
  if num <= 100:
    return f"sheesh... u got a wow number: {num}"
  if num <= 500:
    return f"u got pretty gud... {num}"
  if num <= 1000:
    return f"alright! {num}"
  if num > 1000 and num <= 5000:
    return f"u got an alright number i guess: {num}"
  if num > 5000 and num != 9999:
    return f"big L, you got {num}"
  if num == 9999:
    return f"9999... gotta say gg ig"
  if num == 69:
    return f"OMG U ABSOLUTE BEAST U GOT THE BEST NUMBER EVER... 69!!!!!"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
  await guild.text_channels[0].send("Hi!! I'm roll bot. To get started, type $help.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$help"):
        help_text = """
$roll_perms: prints out a list of all users who can use $roll

$roll [max_num]: prints a random number between 1 and [max_num]. -needs roll perms
        
$add_user [user]: gives a user roll perms. -needs administrator
        
EXAMPLES:
        
$roll_perms
$roll 9999
$add_user cam010#1842
        
Need more help? DM cam010#1842
        """
        await message.channel.send(help_text)

    if message.content.startswith('$roll_perms'):
        users = get_users()
        to_print = "User(s) with $roll perms are:"
        for x in users:
            to_print += "\n\t- "
            to_print += x
        await message.channel.send(to_print)

    if message.content.startswith('$add_user'):
        if not message.author.guild_permissions.administrator:
            await message.channel.send("You don't have permission to do that.")
            return
        user = message.content.split('$add_user ', 1)[1]
        guild = message.author.guild.id
        print("guild")
        file = f"users{guild}.txt"
        with open(file, "a") as f:
            f.write(f"\n{user}")

    if message.content.startswith('$roll'):
        if not message.content.startswith('$roll '):
            return
        users = get_users()
        perm = False
        for x in users:
          if str(message.author) == str(x):
              perm = True

        if perm == False:
            await message.channel.send("You don't have permission to do that")
            return

        try:
            bound2 = int(message.content.split('$roll ', 1)[1])
        except:
            await message.channel.send("Please input a number!!")
            return

        if bound2 <= 0:
            await message.channel.send("Please input a number bigger than 0")
            return

        try:
            roll = random.randint(1, bound2)
            log_num(roll)
            to_print = return_str_based_on_range(roll)
            await message.channel.send(to_print)
            return
        except IndexError:
            await message.channel.send("Please specify a maximum number for the roll!")
            return
        except Exception as e:
            print(e)
            await message.channel.send("Internal Error, please contact cam010#1842")
            return

keep_alive()
client.run(token)