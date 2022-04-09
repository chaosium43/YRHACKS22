import discord
import json
import datetime
import time
import asyncio

#making the input receiver packet
client = discord.Client()

#returns the current day (EST)
def currentDate():
    #creating garbage datetime to get current datetime idk
    garbage = datetime.date(2000, 6, 9)
    return garbage.today()

#reads a parameter in a command string
def readParameter(string, start):
    concat = ""
    point = 0
    for i in range(start, len(string)):
        char = string[i]
        point = i
        if char == " ":
            #giving leeway for people who put extra spaces in everything
            if concat != "":
                break
        else:
            concat += char

    return concat, point + 1

#reading userdata from a person
def readUserData(user):
    filehandle = open(f"userdata\\{user}.json", "r")
    userdata = json.loads(filehandle.read())
    filehandle.close()
    return userdata 

#writing userdata from a person
def writeUserData(user, data):
    filehandle = open(f"userdata\\{user}.json", "w")
    filehandle.write(json.dumps(data))
    filehandle.close()















#Commands and logic related to commands outside of on_message will be sent here
cooldown = 600
prefix = "taskbot"

responses = {}
cycles = {}
function_cache = {}

async def testCommand(message, user):
    cycle = cycles[user]
    if cycle == 0:
        responses[user] = "anything"
    elif cycle == 1:
        await message.reply(responses[user])
        responses.pop(user)
commands = {
    "test": testCommand
}






















@client.event
async def on_ready():
    print("WE WIN YRHACKS 22")

@client.event
async def on_message(message):
    author = message.author
    if author != client.user:
        #find the data of the current user and remind them to do their tasks if it is their first time sending the message today
        try:
            #create the userdata if it doesn't exist
            userdata = open(f"userdata\\{author.id}.json", "x")
            userdata.close()
            
            #write default data to new file
            date = currentDate()
            data = {
                "last_message": {"year": date.year, "month": date.month, "day": date.day},
                "tasks": {}
            }
            writeUserData(author.id, data)

        except:
            date = currentDate()
            #grabbing current userdata
            userdata = readUserData(author.id)

            #reminding the user of what tasks they have due
            lastMessage = userdata["last_message"]
            if lastMessage["year"] != date.year or lastMessage["month"] != date.month or lastMessage["day"] != date.day:
                pass

        #respond to the message
        if author.id in responses:
            cycles[author.id] += 1
            responses[author.id] = message.content
            await function_cache[author.id](message, author.id)
        else:
            #parse the content of the message
            parameter, pointer = readParameter(message.content, 0)

            #person wants to use the bot
            if parameter == prefix:
                navigator = commands
                navigated = False
                while True:
                    #navigating through the table of all functions
                    nav, pointer = readParameter(message.content, pointer)
                    if nav in navigator:
                        navigated = True
                        navigator = navigator[nav]

                        #function has been found
                        if type(navigator) == type(currentDate):
                            break
                    else:
                        break

                if navigated:
                    cycles[author.id] = 0
                    function_cache[author.id] = navigator
                    await navigator(message, author.id)
                else: #introduce the bot to the user
                    message.reply(f"It seems like you are having some trouble figuring out how to use this bot. Consider using '{prefix} help' for a list of commands and how to use them.")


            
            


client.run("OTYyMTE0ODc3NzA5NzU0NDE4.YlC1Tg._vUFggMI37NZjUDhRezwD_aJDc4")