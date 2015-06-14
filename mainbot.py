#!/usr/bin/env python3
import irc.bot

from conf import settings

def main():
    from mainbot.main import BaseBot
    bot = BaseBot(settings.apikey, settings.channel, settings.username, \
                  settings.callSign, settings.manOpList, settings.commandPrefix, \
                  settings.filterBotMessages, settings.textReplacements)
    
    import mainbot.commands as commands
    commands.ping(bot)
    commands.die(bot)
    commands.cnJoke(bot)
    commands.vote(bot)
    commands.help(bot)
    commands.say(bot)
    commands.set(bot)
   
    import games.textAdv
    games.textAdv.cca(bot)

    import Commands.fun
    Commands.fun.asciiClock(bot)
    Commands.fun.cowsay(bot)
    Commands.fun.slap(bot)

    import games.card
    games.card.blackjack(bot)

    import mainbot.textReaders
    # mainbot.textReaders.youTubeScanner(bot, open("apikeys/youtube.apikey", "r").read().strip())

    mainbot.textReaders.imgurScanner(bot, *open("apikeys/imgur.apikey").read().strip().split("\n"))

    bot.start(1/30)

if __name__ == "__main__":
    main()
