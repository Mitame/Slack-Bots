#!/usr/bin/env python3

class Command():
    arguments = []
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = ""
    
    def __init__(self,bot):
        self.bot = bot
        bot.commands[self.callname] = self
    
    def on_call(self,event,*args):
        pass
    
    def on_fail(self,event):
        self.bot.cnnection.notice(event.source.nick,\
        "The command must follow the syntax: /%s "% self.callname+" "+str(self.arguments))
    
    def checkPermissions(self,event,*args):
        pass
    
    def checkArgs(self,event,*args):
        pass
    
    def notify(self,event,msg):
        self.notify(msg)


class ping(Command):
    arguments = []
    permissionLevel = 2
    permitExtraArgs = False
    callname = "ping"
    defaultArgs = []
    
    def on_call(self,event,*args):
        self.notify("PONG")
    
          
class die(Command):
    arguments = []
    permissionLevel = 3
    permitExtraArgs = False
    callname = "die"
    defaultArgs = []
    
    def on_call(self,event,*args):
        self.bot.die(" ".join(args))


class cnJoke(Command):
    arguemnts = []
    permissionLevel = 0
    permitExtraArgs = False
    callname = "cnjoke"
    defaultArgs = []
    
    def __init__(self,*args,**kwargs):
        Command.__init__(self,*args,**kwargs)
        global json, urllib
        import json
        import urllib.request
        
        
    def on_call(self,event,*args):
        x = urllib.request.urlopen("http://api.icndb.com/jokes/random")
        z = str(x.read(),"utf8")
        try:
            a = json.loads(z)
            self.bot.sendMsg(event, a["value"]["joke"])
        except ValueError:
            print(z)
    
    def on_fail(self,event):
        self.bot.cnnection.notice(event.source.nick,\
        "You failed to type the command correctly puny human. \nChuck Norris will roundhouse kick you in the face shortly."% self.callname+" "+str(self.arguments))


class vote(Command):
    arguments = ["str","str"]
    permissionLevel = -1
    permitExtraArgs = True
    manArgCheck = True
    defaultArgs = []
    callname = "vote"
    
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
    
    def alert(self,event,msg):
        self.bot.sendPubMsg(event,msg)
        
    def createPoll(self,event,name,question,*options):
        self.currentPoll = name
        self.polls[name] = self.poll(*options)
        self.polls[len(self.polls.keys())] = name
        self.alert(event,"""%s has started a poll!""" % event.source.nick)
        self.alert(event,"---%s---" % question)
        
        for x in range(len(self.polls[name].voteids)):
            self.alert(event,str(x)+" :\t"+self.polls[name].getVote(x))
        
        self.alert(event,"To vote, type in '%s:vote #', where '#' is your vote." % self.bot.callsign)
        self.alert(event,"---Note, you can't change your mind after you have voted, so think carefully.")
    
    def castVote(self,event,*args):
        if self.currentPoll == "":
            self.bot.sendPubMsg(event,"Sorry %s, there is not vote running currently." % event.source.nick)
            return
        
        curpoll = self.polls[self.currentPoll]
        if event.source.nick in curpoll.voted:
            self.bot.sendPubMsg(event,"Sorry %s, you can't vote again." % event.source.nick)
            return
        
        curpoll = self.polls[self.currentPoll]
        curpoll.votes[curpoll.voteids[int(args[0])]] += 1
        alert = ("%s voted for '" +self.polls[self.currentPoll].voteids[int(args[0])]+"'!")%event.source.nick

        curpoll.voted.append(event.source.nick)
        self.bot.sendPubMsg(event,alert)
        
    def checkPermissions(self, event, *args):
        base = args[0]
        if base in ("create","results","close"):
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
        return True
    
    def getResults(self,event,*args):
        if self.currentPoll == "":
            self.bot.sendPubMsg(event,"Sorry %s, there is not vote running currently." % event.source.nick)
            return
        
        self.bot.sendPubMsg(event,"---Current poll results---")
        for id in self.polls[self.currentPoll].voteids:
            x = self.polls[self.currentPoll].voteids[id]
            
            self.bot.sendPubMsg(event,("    '%s': "+str(self.polls[self.currentPoll].votes[x])+" votes.") % x )
        self.bot.sendPubMsg(event,"--------------------------")
    
    def closePoll(self,event,name):        
        self.alert(event, "The voting has now ended. The final results are:")
        for id in self.polls[self.currentPoll].voteids:
            x = self.polls[self.currentPoll].voteids[id]
            
            self.bot.sendPubMsg(event,("    '%s': "+str(self.polls[self.currentPoll].votes[x])+" votes.") % x )
        self.bot.sendPubMsg(event,"--------------------------")
        
        self.currentPoll = ""
        
    def on_call(self, event, *args):
        print(args)
        if args[0] == "create":
            args = " ".join(args[1:]).split(", ")
            self.createPoll(event,args[0],args[1],*args[2:])
        elif args[0] == "results":
            self.getResults(event)
        elif args[0] == "close":
            try:
                self.closePoll(event,self.currentPoll)
            except NameError:
                self.alert("No poll to close.")
        else:
            if args[0].isdecimal():
                self.castVote(event,int(args[0]))


class help(Command):
    arguments = []
    permissionLevel = 0
    permitExtraArgs = False
    manArgCheck = False
    defaultArgs = []
    callname = "help"
    
    def on_call(self,event,*args):
        commands = []
        print(self.bot.commands)
        for x in list(self.bot.commands.items()):
            print(x)
            if x[1].permissionLevel <= self.bot.getPermLevel(event):
                commands.append(x[0])
        
        commands.sort()
        self.notify("---Commands avaliable to you---")
        for cmd in commands:
            self.notify(self.bot.callsign+":"+cmd)
        self.notify("-------------------------------")
        
    
    
        