from sqlite3 import Date
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

def format_tasks(tasks):
    concat = ""
    for tk in tasks:
        id = tk[0]
        task = tk[1]
        concat += f"ID: {id}, Task: {task[0]}, Task Type: {task[4]}, Due on: {task[1]}/{task[2]}/{task[3]}\n"

    if concat == "":
        return "None"
    else:
        return concat

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

async def createTask(message, user):
    cycle = cycles[user]
    if cycle == 0:
        responses[user] = "anything"
        await message.reply("What is the name of this task? Make it concise and descriptive.")
    elif cycle == 1:
        userdata = readUserData(user)
        userdata["tasks"].append([responses[user]])
        writeUserData(user, userdata)
        await message.reply("What month is this task going to be due on?")
    elif cycle == 2:
        monthTable = {
            "1": 1, "january": 1, 
            "2": 2, "february": 2,
            "3": 3, "march": 3,
            "4": 4, "april": 4,
            "5": 5, "may": 5,
            "6": 6, "june": 6,
            "7": 7, "july": 7,
            "8": 8, "august": 8,
            "9": 9, "september": 9,
            "10": 10, "october": 10,
            "11": 11, "november": 11,
            "12": 12, "december": 12
        }
        if responses[user].lower() in monthTable:
            month = monthTable[responses[user].lower()]
            userdata = readUserData(user)
            tasks = userdata["tasks"]
            tasks[len(tasks) - 1].append(month)
            writeUserData(user, userdata)
            await message.reply("What day is this task going to be due on?")
        else:
            cycles[user] -= 1
            await message.reply("Invalid month entered. Try again.")
    
    elif cycle == 3:
        try:
            day = int(responses[user])
            if day > 0 and day < 32:
                userdata = readUserData(user)
                tasks = userdata["tasks"]
                tasks[len(tasks) - 1].append(day)
                writeUserData(user, userdata)
                await message.reply("What year is this task going to be due on?")
            else:
                cycles[user] -= 1
                await message.reply("Invalid day entered. Try again.")
        except:
            cycles[user] -= 1
            await message.reply("Invalid day entered. Try again.")

    elif cycle == 4:
        try:
            year = int(responses[user])
            date = currentDate()
            if year >= date.year and year <= 3000:
                userdata = readUserData(user)
                tasks = userdata["tasks"]
                task = tasks[len(tasks) - 1]

                task.append(year)

                #Figure out the type of task (Long, Medium or Short Term)
                dateUnix = time.mktime(date.timetuple())
                taskUnix = time.mktime(datetime.date(year, task[1], task[2]).timetuple())

                days = taskUnix - dateUnix
                days = days / 86400

                if days <= 7:
                    task.append("Short Term")
                elif days <= 28:
                    task.append("Medium Term")
                else:
                    task.append("Long Term")



                writeUserData(user, userdata)
                responses.pop(user)
                await message.reply("Your task has been successfully entered.")
            else:
                cycles[user] -= 1
                await message.reply("Invalid year entered. Try again.")
        except:
            cycles[user] -= 1
            await message.reply("Invalid year entered. Try again.")

async def getTasks(message, user):
    userdata = readUserData(user)
    tasks = userdata["tasks"]
    embed = discord.Embed()
    date = currentDate()
    dateUnix = time.mktime(date.timetuple())
    embed.set_author(name = "Here is a list of all the tasks you need to do!", icon_url = client.user.avatar_url)
    task_table = {
        "Long Term": [[], [], []],
        "Medium Term": [[], [], []],
        "Short Term": [[], [], []]
    }

    if len(tasks) > 0:
        #sort tasks by priority
        id = -1
        for task in tasks:
            id += 1
            timeUnix = time.mktime(datetime.date(task[3], task[1], task[2]).timetuple())
            dt = timeUnix - dateUnix
            dt = dt / 86400
            if dt <= 2:
                task_table[task[4]][0].append([id, task])
            elif dt <= 7:
                task_table[task[4]][1].append([id, task])
            else:
                task_table[task[4]][2].append([id, task])


        #Sort tasks first by urgency and then by long vs short term
        urgent_tasks = task_table["Long Term"][0] + task_table["Medium Term"][0] + task_table["Short Term"][0]
        medium_tasks = task_table["Long Term"][1] + task_table["Medium Term"][1] + task_table["Short Term"][1]
        funny_tasks = task_table["Long Term"][2] + task_table["Medium Term"][2] + task_table["Short Term"][2]

        urgentDisplay = format_tasks(urgent_tasks)
        mediumDisplay = format_tasks(medium_tasks)
        funnyDisplay = format_tasks(funny_tasks)



        embed.add_field(name = "Urgent Tasks:", value = f"```{urgentDisplay}```", inline = False)
        embed.add_field(name = "Medium Tasks:", value = f"```{mediumDisplay}```", inline = False)
        embed.add_field(name = "Other Tasks:", value = f"```{funnyDisplay}```", inline = False)
    else:
        embed.add_field(name = "You do not currently have any tasks due!", value = "If there are any tasks to do, feel free to add it using 'taskbot create'!", inline = True)

    await message.reply(embed = embed)


async def markTask(message, user):
    cycle = cycles[user]
    if cycle == 0:
        responses[user] = "anything"
        await message.reply("Enter the ID of the task you would like to mark as completed.")
    elif cycle == 1:
        userdata = readUserData(user)
        try:
            if responses[user].lower() == "cancel":
                await message.reply("Cancelling action.")
            else:
                id = int(responses[user])
                if id >= 0 and id < len(userdata["tasks"]):
                    userdata["tasks"].pop(id)
                    responses.pop(user)
                    writeUserData(user, userdata)
                    await message.reply("Your task has been successfully marked as completed.")
                else:
                    cycles[user] -= 1
                    await message.reply("Unfortunately, the ID of the task you were looking for wasn't found. Please try entering a different ID.")

        except:
            cycles[user] -= 1
            await message.reply("Unfortunately, the ID of the task you were looking for wasn't found. Please try entering a different ID.")

commands = {
    "test": testCommand,
    "create": createTask,
    "tasks": getTasks,
    "mark": markTask
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
                "tasks": [],
                "coins": 0,
                "backpack": []
            }
            writeUserData(author.id, data)

        except:
            date = currentDate()
            #grabbing current userdata
            userdata = readUserData(author.id)

            #reminding the user of what tasks they have due
            lastMessage = userdata["last_message"]
            if lastMessage["year"] != date.year or lastMessage["month"] != date.month or lastMessage["day"] != date.day:
                userdata = readUserData(author.id)

                #finding tasks that are already completed and automatically delete them
                completeTasks = []
                for i in range(len(userdata["tasks"])):
                    task = userdata["tasks"][i]
                    taskUnix = time.mktime(datetime.date(task[3], task[1], task[2]).timetuple())
                    dateUnix = time.mktime(date.timetuple())
                    if dateUnix > taskUnix:
                        completeTasks.append(i)

                if len(completeTasks) > 0:
                    i = len(completeTasks)
                    while i != 0:
                        i -= 1
                        userdata["tasks"].pop(completeTasks[i])
                
                await getTasks(message, author.id)
                
                #update userdata
                userdata["last_message"] = {"year": date.year, "month": date.month, "day": date.day}
                writeUserData(author.id, userdata)

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
                    await message.reply(f"It seems like you are having some trouble figuring out how to use this bot. Consider using '{prefix} help' for a list of commands and how to use them.")


            
            


client.run("OTYyMTE0ODc3NzA5NzU0NDE4.YlC1Tg._vUFggMI37NZjUDhRezwD_aJDc4")