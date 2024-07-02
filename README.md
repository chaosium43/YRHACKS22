This is a discord bot I created for YRHACKS 2022 which has been updated to work with the current discord.py
library.
The main idea of this discord bot was to be a virtual calendar of sorts where tasks could be added and
retrieved in one place, and where tasks would automatically sort by urgency.
This bot is command based like a traditional discord bot, and all command documentation can be retrieved with
"taskbot help" once you get your instance of taskbot running on a discord server.

This application requires a working installation on your operating system (3.0+) and requires you to install an extra module called "discord"
(do pip install discord in the terminal to install it)

In order to get the bot to work, you first need to create a bot on the Discord developer portal 
(https://discord.com/developers/applications) and set the bot to have message sending and message history
permissions, in addition to the Message Content Intent in privileged intents.

Next, go to the OAuth2 section of the developer portal, give it the bot scope, and then give the bot the 
same permissions as you gave it in the "Bot" section of the developer portal to generate an invite to
add in your discord server.

Don't forget to give your bot an avatar profile picture as it will break without it. You can use the
profile picture that my team used for YRHACKS 2022 provided in this folder as "taskbot pfp.png"

Then, there should be a string "your token here" on the last line of "main.py". Change the string to have
your bot's token and run main.py to start the bot.