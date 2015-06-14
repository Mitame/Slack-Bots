MMI-Bot Base and Test Bots for slack
====================================
(In development)
------------------------------------
 
These are some testbots for IRC servers.
They are easily configurable and should be easy to make new commands for.
Written in python.



Dependencies
------------
####For everything:
[Slack API implementation for Python](https://github.com/os/slacker)

[Websockets in Python](https://pypi.python.org/pypi/websocket-client)

####For Commands/fun (These can be disabled)
[pyfiglet](https://pypi.python.org/pypi/pyfiglet) for generating ascii clocks in ```asciiClock()``` command.

[cowsay](http://en.wikipedia.org/wiki/Cowsay) for generating cowsay ascii art in ```cowsay()``` command.

[pexpect](http://pexpect.sourceforge.net/pexpect.html) and [adventure](http://en.wikipedia.org/wiki/Colossal_Cave_Adventure) for ```cca()``` command.

[google-api-python-client] For ```mainbot.textReaders.youTubeScanner``` and a YouTube Data API key.

[imgurpython](https://github.com/Imgur/imgurpython) For ```mainbot.textReaders.imgurScanner```




Running a bot
-------------
1. Edit ```conf/__init__.py``` to include you're configurations (most importantly, your apikey)
2. Copy mainbot.py and edit to your liking. Comment out lines to remove commands.

Creating commands
-----------------
To create commands, create a new class which inherits `mainbot.commands.Command`
```python
from mainbot.commands import Command

class newCommand(Command):
    pass
```
Next, set the variables for the command that the bot reads when calling it to check parameters.
```python
class newCommand(Command):
    arguments = ["str"]
        permissionLevel = 3
        permitExtraArgs = False
        manArgCheck = False
        defaultArgs = []
        callName = "new"
```
When a command is recieved and is allowed to be executed, ```Commands.on_call(self,event,*args)``` is called for the command. Add a class method to recieve this.

```python
class newCommand(Command):
    argu...

    def on_call(self,event,*args):
        "do stuff"
```

The bot will receive messages from both the channel it has joined and private messages. Use ```self.bot.send_PubMsg(message)```, ```self.bot.send_PrivMsg(userID,message)``` and ```self.bot.send_reply(event,message)``` to send channel, private and reply messages, respectively.
