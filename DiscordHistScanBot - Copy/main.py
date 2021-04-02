import discord
import os
import sys
import random
import time
import datetime
from datetime import date

# discord access info -----------------------------------------------------------------
client = discord.Client()
bot_id = 'REMOVED'
channel_id = 00000
channel_name = "bot-testing"
# end--------------------------------------------------------------------------------------

def fixString(message) -> str:
    finalStr = message
    finalStr = finalStr.replace(" .", ".")
    finalStr = finalStr.replace(" .  ", ". ")
    finalStr = finalStr.replace(" ,", ",")
    finalStr = finalStr.replace(" ,  ", ", ")
    finalStr = finalStr.replace(" !", "!")
    finalStr = finalStr.replace(" !  ", "! ")
    finalStr = finalStr.replace("  ", " ")
    return finalStr


@client.event # run the code when the bot goes online
async def on_ready():
    bot_testing = client.get_channel(channel_id) # accessing the channel
    await bot_testing.send("Auto Hist Scan bot is now online!")

@client.event
async def on_message(message):
    bot_testing = client.get_channel(channel_id)
    gate = True
    message_list = []
    final_message = ""
    MAX_COUNTER = 5000

    while gate == True:
        f = open(os.path.join(sys.path[0], "HistMessages.txt"), "a", encoding="utf-8")

        if message.content == ">>quit()" and message.channel.id == channel_id:
            await message.channel.send("Program Terminated Successfully! (SystemExit: 0)")
            sys.exit(0)

        if message.content.find(">>scan history") != -1 and message.channel.id == channel_id:
            int_temp ='' # user input for scan num
            for c in message.content:
                if c.isdigit():
                    int_temp += str(c)
            int_temp = int(int_temp)

            if int_temp == 0:
                await message.channel.send("**ERROR** - Cannot scan zero messages!")
                break
            elif int_temp >= MAX_COUNTER:
                await message.channel.send("**ERROR** - Max threshold exceeded (>= 5000)")
                break

            if int_temp != None:
                retrived_messages = await message.channel.history(limit=int_temp + 1).flatten()
            else:
                retrived_messages = await message.channel.history(limit=None).flatten()

            for message in retrived_messages:
                message_list.append(message.content)

            for m in reversed(message_list):
                final_message += f"{m} "

            f.write(fixString(final_message))
            await message.channel.send(f"Past messages ({int_temp}) has successfully been scanned. (output at HistMessages.txt)")

        f.close()
        gate = False

while True:
    client.run(bot_id)