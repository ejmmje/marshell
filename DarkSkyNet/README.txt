- Elliot Marshallsay
- 3238 5316

Hi there!
Welcome to my final project where I created a chat bot where you can ask for the weather in any city in the world!
It is very simple to run:

1. run the file 'chatbot.py' in a program such as terminal, GitBash, or simply double click it to run in your default window.
2. Be kind! Say hello to the bot and you can have a conversation if you would like.
3. To ask about the weather, it is important that you type in the correct syntax as it is CASE and PUNCTUATION SENSITIVE!
  You can ask one of these seven commands using the exact syntax and replacing the portion in parentheses with the city of your choice:
    What's the weather like in (city)?
    Is it going to rain in (city) today?
    How hot will it get in (city) today?
    How cold will it get in (city) today?
    Is it going to rain in (city) this week?
    How hot will it get in (city) this week?
    How cold will it get in (city) this week?
For each one of the statements, my weatherbot will return the answer to all of your weather desires.

For the rain statements, I have filtered for snow.
      If the average temperature through the day(for daily rain) or week(for weekly rain) is below 32.00 degrees, the bot will inform you that it may or may not snow instead of rain.

Lastly, if you enter an incorrect city, my bot will inform you that you may have made a typing error and feel free to re-enter the request with the correct spelling of a city.

Here is an example interaction:

----------------------------------------
Hello. I am your leader. You may call me Weather bot.

Please, say Hello.
...

> Hello
...What can I call you?

> Elliot
...Nice to meet you Elliot.

> Are you a robot?
...How did you know I am a machine?

> Are you human?
...No I am not. I am a robot.

> How are you today?
...I am functioning within normal parameters.

> What's the weather like in London?
...In London, it is 36.11 degrees and Clear

> How hot will it get in Chicago?
...Is this a joke?

> How hot will it get in Chicago this week?
...In Chicago, the high is 46.52 degrees

> Is it going to rain in Detroit today?
...The average hourly temperature is below 32.00 degrees Fahrenheit!
...It probably will snow in Detroit

> exit


Goodbye, thank you for using Elliot's Weather Bot.
----------------------------------------
