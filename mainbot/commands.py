#!/usr/bin/env python3

import json
import urllib.request

class Command():
    arguments = []
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callName = ""
    
    def __init__(self,bot):
        self.bot = bot
        self.bot.registerCommand(self)
    
    def on_call(self,event,*args):
        self.bot.do_command("help "+" ".join(args))
    
    def on_fail(self,event):
        self.notify(event.source.nick,\
        "The command must follow the syntax: /%s "% self.callName+" "+str(self.arguments))
    
    def checkPermissions(self,event,*args):
        pass
    
    def checkArgs(self,event,*args):
        pass
    
    def privMsg(self,*args):
        self.bot.send_PrivMsg(*args)

    def on_die(self,event):
        pass
    
    def pubMsg(self,event,msg):
        self.bot.send_PubMsg(msg)
        
        
class ping(Command):
    arguments = []
    permissionLevel = 2
    permitExtraArgs = False
    callName = "ping"
    defaultArgs = []
    
    def on_call(self, event, *args):
        self.bot.send_PrivMsg(event.channel, "PONG")
    
          
class die(Command):
    arguments = []
    permissionLevel = 3
    permitExtraArgs = False
    callName = "die"
    defaultArgs = []
    
    def on_call(self,event,*args):
        self.bot.die(event, " ".join(args))


class cnJoke(Command):
    arguemnts = []
    permissionLevel = 0
    permitExtraArgs = False
    callName = "cnjoke"
    defaultArgs = []
    
    def __init__(self,*args,**kwargs):
        Command.__init__(self,*args,**kwargs)


    def on_call(self,event,*args):
        x = urllib.request.urlopen("http://api.icndb.com/jokes/random")
        z = str(x.read(),"utf8")
        try:
            a = json.loads(z)
            self.bot.send_PubMsg(a["value"]["joke"])
        except ValueError:
            print(z)
    
    # def on_fail(self,event):
    #     self.notify(event.source.nick,\
    #     "You failed to type the command correctly puny human. \nChuck Norris will roundhouse kick you in the face shortly."% self.callName+" "+str(self.arguments))


class vote(Command):
    arguments = ["str","str"]
    permissionLevel = -1
    permitExtraArgs = True
    manArgCheck = True
    defaultArgs = []
    callName = "vote"
    
    class poll():
        def __init__(self,*args):
            self.votes = {}
            self.voteids = {}
            self.voted = []
            for vote in args:
                self.votes[vote] = 0
                self.voteids[args.index(vote)] = vote
        def getVote(self,id,data="name"):
            if data == "name":
                return self.voteids[id]
            elif data == "score":
                return self.votes[self.voteids[id]]
            
    def __init__(self,bot):
        Command.__init__(self, bot)
        self.polls = {}
        self.pollids = {}
        self.currentPoll = ""
    
    
        
    def createPoll(self,event,name,question,*options):
        self.currentPoll = name
        self.polls[name] = self.poll(*options)
        self.polls[len(self.polls.keys())] = name

        message = """%s has started a poll!""" % event.user+"\n"

        message += ("---%s---" % question)+"\n"
        
        for x in range(len(self.polls[name].voteids)):
            message += (str(x)+" :\t"+self.polls[name].getVote(x))+"\n"
        
        message += ("To vote, type in '%s:vote #', where '#' is your vote." % self.bot.callsign)+"\n"
        message += "---Note, you can't change your mind after you have voted, so think carefully."

        self.bot.send_PubMsg(message)
    
    def castVote(self,event,*args):
        if self.currentPoll == "":
            self.bot.send_PubMsg("Sorry %s, there is not vote running currently." % event.user)
            return
        
        curpoll = self.polls[self.currentPoll]
        if event.user in curpoll.voted:
            self.bot.send_PubMsg("Sorry %s, you can't vote again." % event.user)
            return
        
        curpoll = self.polls[self.currentPoll]
        curpoll.votes[curpoll.voteids[int(args[0])]] += 1
        alert = ("%s voted for '" +self.polls[self.currentPoll].voteids[int(args[0])]+"'!") % event.user

        curpoll.voted.append(event.user)
        self.bot.send_PubMsg(alert)
        
    def checkPermissions(self, event, *args):
        if len(args) == 0:
            return True
        base = args[0]
        if base in ("create", "results", "close"):
            if self.bot.getPermLevel(event) >= 1:
                return True
            else:
                return False
        else:
            if base.isdecimal() and (0<=int(base)<len(self.polls[self.currentPoll].voteids)):
                return True
            else:
                return False
    
    def checkArgs(self, event, *args):
        if len(args) == 0:
            return 0
        return True
    
    def getResults(self,event,*args):
        if self.currentPoll == "":
            self.bot.sendPubMsg(event,"Sorry %s, there is not vote running currently." % event.user)
            return
        
        message = "---Current poll results---" + "\n"
        for id in self.polls[self.currentPoll].voteids:
            x = self.polls[self.currentPoll].voteids[id]
            message += ("    '%s': "+str(self.polls[self.currentPoll].votes[x])+" votes.") % x +"\n"
        message += "--------------------------"
    
    def closePoll(self,event,name):
        message = "The voting has now ended. The final results are:\n"
        for id in self.polls[self.currentPoll].voteids:
            x = self.polls[self.currentPoll].voteids[id]
            message += ("    '%s': "+str(self.polls[self.currentPoll].votes[x])+" votes.") % x

        message += "--------------------------"
        self.bot.send_PubMsg(message)
        
        self.currentPoll = ""
        
    def on_call(self, event, *args):
        print(args)
        if args[0] == "create":
            args = " ".join(args[1:]).split(", ")
            try:
                self.createPoll(event,args[0],args[1],*args[2:])
            except IndexError:
                pass

        elif args[0] == "results":
            self.getResults(event)
        elif args[0] == "close":
            try:
                self.closePoll(event,self.currentPoll)
            except NameError:
                self.pubMsg("No poll to close.")
        else:
            if args[0].isdecimal():
                self.castVote(event,int(args[0]))


class help(Command):
    arguments = []
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callName = "help"
    
    def on_call(self,event,*args):
        commands = []
        print(self.bot.commands)
        for x in list(self.bot.commands.items()):
            print(x)
            if x[1].permissionLevel <= self.bot.getPermLevel(event):
                commands.append(x[0])
        
        commands.sort()
        # self.bot.send_PrivMsg(event.channel, "---Commands avaliable to you---\n"+ \
        #                       "\n".join(self.bot.callsign+":"+cmd for cmd in commands) + \
        #                       "\n-------------------------------")
        self.bot.send_PrivMsg(event.channel, "---Commands avaliable to you---\n"+ \
                                             "\n".join(self.bot.commandPrefix+cmd for cmd in commands) + \
                                             "\n-------------------------------")
       
class flushLog(Command):
    arguments = []
    permissionLevel = 3
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callName = "flushlog"
    
    def on_call(self, event, *args):
        # self.bot.logfile.flush()
        pass

class say(Command):
    arguments = []
    permissionLevel = 3
    permitExtraArgs = True
    manArgCheck = False
    defaultArgs = []
    callName = "say"
    
    def on_call(self, event, *args):
        self.bot.send_PrivMsg(event.channel, " ".join(args))
