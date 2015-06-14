#!/usr/bin/env python3
# from socket import gethostbyname
import re
import json
import pprint
import websocket
import time
# import slacker
from slacker import Slacker

# from mainbot.autoCommand import NickServLogin

pp = pprint.PrettyPrinter(indent=4)


class RTMHandler():
    events = ["hello", "message", "user_typing", "channel_marked",
              "channel_created", "channel_joined", "channel_left", "channel_deleted",
              "channel_rename", "channel_archive", "channel_unarchive", "channel_history_changed",
              "im_created", "im_open", "im_close", "im_marked",
              "im_history_changed", "group_joined", "group_left", "group_open",
              "group_close", "group_archive", "group_unarchive", "group_rename",
              "group_marked", "group_history_changed", "file_created", "file_shared",
              "file_unshared", "file_public", "file_private", "file_change",
              "file_deleted", "file_comment_added", "file_comment_edited", "file_comment_deleted",
              "pin_added", "pin_removed", "presence_change", "manual_presence_change",
              "pref_change", "user_change", "team_join", "star_added",
              "star_removed", "emoji_changed", "commands_changed", "team_plan_change",
              "team_pref_change", "team_rename", "team_domain_change", "email_domain_changed",
              "bot_added", "bot_changed", "accounts_changed", "team_migration_started",
              "reply_to"]

    def __init__(self, url):
        self.ws = websocket.create_connection(url)

        self.handlers = {}
        for event in self.events:
            self.handlers[event] = getattr(self, "on_"+event)

        self.msgid = 0

    #define all websocket message handlers (there's a lot...)
    def on_hello(self, msg):
        pass

    def on_message(self, msg):
        pass

    def on_user_typing(self, msg):
        pass

    def on_channel_marked(self, msg):
        pass

    def on_channel_created(self, msg):
        pass

    def on_channel_joined(self, msg):
        pass

    def on_channel_left(self, msg):
        pass

    def on_channel_deleted(self, msg):
        pass

    def on_channel_rename(self, msg):
        pass

    def on_channel_archive(self, msg):
        pass

    def on_channel_unarchive(self, msg):
        pass

    def on_channel_history_changed(self, msg):
        pass

    def on_im_created(self, msg):
        pass

    def on_im_open(self, msg):
        pass

    def on_im_close(self, msg):
        pass

    def on_im_marked(self, msg):
        pass

    def on_im_history_changed(self, msg):
        pass

    def on_group_joined(self, msg):
        pass

    def on_group_left(self, msg):
        pass

    def on_group_open(self, msg):
        pass

    def on_group_close(self, msg):
        pass

    def on_group_archive(self, msg):
        pass

    def on_group_unarchive(self, msg):
        pass

    def on_group_rename(self, msg):
        pass

    def on_group_marked(self, msg):
        pass

    def on_group_history_changed(self, msg):
        pass

    def on_file_created(self, msg):
        pass

    def on_file_shared(self, msg):
        pass

    def on_file_unshared(self, msg):
        pass

    def on_file_public(self, msg):
        pass

    def on_file_private(self, msg):
        pass

    def on_file_change(self, msg):
        pass

    def on_file_deleted(self, msg):
        pass

    def on_file_comment_added(self, msg):
        pass

    def on_file_comment_edited(self, msg):
        pass

    def on_file_comment_deleted(self, msg):
        pass

    def on_pin_added(self, msg):
        pass

    def on_pin_removed(self, msg):
        pass

    def on_presence_change(self, msg):
        pass

    def on_manual_presence_change(self, msg):
        pass

    def on_pref_change(self, msg):
        pass

    def on_user_change(self, msg):
        pass

    def on_team_join(self, msg):
        pass

    def on_star_added(self, msg):
        pass

    def on_star_removed(self, msg):
        pass

    def on_emoji_changed(self, msg):
        pass

    def on_commands_changed(self, msg):
        pass

    def on_team_plan_change(self, msg):
        pass

    def on_team_pref_change(self, msg):
        pass

    def on_team_rename(self, msg):
        pass

    def on_team_domain_change(self, msg):
        pass

    def on_email_domain_changed(self, msg):
        pass

    def on_bot_added(self, msg):
        pass

    def on_bot_changed(self, msg):
        pass

    def on_accounts_changed(self, msg):
        pass

    def on_team_migration_started(self, msg):
        pass

    def on_reply_to(self,msg):
        pass

    def on_any(self,msg):
        pass

    def send_message(self, channel, text, wait=False):
        jsonString = json.dumps({"id": self.msgid,
                                 "type": "message",
                                 "channel": channel,
                                 "text": text
                                 })
        print(jsonString)
        self.ws.send(jsonString)

        if wait:
            pass

        self.msgid += 1

    def wait_for_reply(self, id):
        pass

    def _onrecv(self, msg):
        parse = Message(json.loads(msg))
        self.on_any(parse)
        if hasattr(parse, "reply_to"):
            self.handlers["reply_to"](parse)
        else:
            if hasattr(parse, "message"):
                self.handlers[parse.type](parse.message)
            self.handlers[parse.type](parse)

    def start(self, scanInterval=1):
        while 1:
            self._onrecv(self.ws.recv())
            time.sleep(scanInterval)

class dictObj():
    def __init__(self, Dict):
        for a,b in Dict.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [type(self)(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, type(self)(b) if isinstance(b,dict) else b)

class Message(dictObj):
    pass


class User(dictObj):
    def getImID(self, slack):
        if not hasattr(self, "imID"):
            im = slack.im.open(self.id).body
            if im["ok"] == True:
                self.imID = im["channel"]["id"]
        return self.imID


class Group(dictObj):
    pass


class Channel(dictObj):
    pass


def getAllUsers(slack):
    userObjs = {}
    users = slack.users.list().body["members"]
    for x in users:
        userObjs[x["id"]] = User(x)

    return userObjs

def getAllGroups(slack):
    groupObjs = {}
    users = slack.groups.list().body["groups"]
    for x in users:
        groupObjs[x["id"]] = Group(x)

    return groupObjs

def getAllChannels(slack):
    channelObjs = {}
    users = slack.channels.list().body["channels"]
    for x in users:
        channelObjs[x["id"]] = Channel(x)

    return channelObjs


class BaseBot(RTMHandler):

    def __init__(self, apikey, channel, username, callsign, manOpList, commandPrefix, filterBotMessages, textReplacements):
        self.apikey = apikey

        self.slack = Slacker(apikey)

        #fill lists of users, channels dms and groups
        self.users = getAllUsers(self.slack)
        self.channels = getAllChannels(self.slack)
        self.groups = getAllGroups(self.slack)

        self.channel = self.getID(channel)
        if self.channel is False:
            raise ValueError("No channel exists")

        self.username = username
        self.callsign = callsign
        self.manOpList = manOpList
        self.commandPrefix = commandPrefix
        self.filterBotMessages = filterBotMessages
        self.textReplacements = textReplacements

        self.commands = {}
        self.textReaders = {}

        self.allowExclaimCommand = commandPrefix != ""
        RTMHandler.__init__(self, self.slack.rtm.start().body["url"])

    def on_message(self, msg):
        print(self.users[msg.user].name + " said:", msg.text)

        if hasattr(msg,"message"):
            self.on_message(msg.message)
            return

        if msg.channel[0] == "D": # find direct messages
            self.do_command(msg.text, msg)

        # for channel (public) messages
        text = msg.text
        if text.strip() == "": return

        for regexp in self.textReaders.keys():
            positions = re.search(regexp, text)
            if positions is not None:
                self.textReaders[regexp].on_call(msg, positions)

        a = text.split(":", 1)
        if len(a) > 1 and a[0].lower() == self.callsign:
            self.do_command(a[1].strip(), msg)

        if self.allowExclaimCommand:
            if text[0] == self.commandPrefix:
                if text.split(" ")[0][1:] in self.commands.keys():
                    self.do_command(text.strip()[1:], msg)

        return

    def _onrecv(self, msg):
        print(msg)
        RTMHandler._onrecv(self, msg)

    def send_PubMsg(self, message):
        self.send_message(self.channel, message)

    def send_PrivMsg(self, userID, text):
        self.send_message(self.users[userID].getImID(self.slack), text)

    def send_reply(self, event, text):
        self.send_message(event.channel, text)

    def registerTextReader(self, textReader):
        self.textReaders[textReader.re] = textReader

    def registerCommand(self, command):
        self.commands[command.callName] = command

    def die(self):
        raise SystemExit

    def join(self, *channels):
        for channel in channels:
            self.slack.channels.join(channel)

    def isPermitted(self,userID):
        return self.users[userID].name in self.manOpList

    def isOp(self,userID):
        return self.users[userID].is_admin

    def getPermLevel(self,userID):
        if self.users[userID].name in self.manOpList:
            return 3
        elif self.users[userID].is_owner:
            return 2
        elif self.users[userID].is_admin:
            return 1
        else:
            return 0

    def getID(self, name):
        for id, user in self.users.items():
            if user.name == name:
                return id

        for id, channel in self.channels.items():
            if channel.name == name:
                return id

        for id, group in self.groups.items():
            if group.name == name:
                return id
        return False

    def getName(self, ID):
        firstchar = ID[0]
        if firstchar == "U":
            try:
                return self.users[ID].name
            except IndexError:
                return False

        elif firstchar == "G":
            try:
                return self.groups["ID"].name
            except IndexError:
                return False

        elif firstchar == "C":
            try:
                return self.channels["ID"].name
            except IndexError:
                return False
        else:
            return False

    def do_command(self, cmd, event):
        args = cmd.split(" ")[1:]
        cmd = cmd.split(" ")[0]
        if cmd.lower() in self.commands.keys():
            cmdclass = self.commands[cmd.lower()]
            if cmdclass.permissionLevel == -1:
                if not cmdclass.checkPermissions(event, *args):
                    return
            else:
                if self.getPermLevel(event.user) < cmdclass.permissionLevel:
                    self.send_PrivMsg(event.user, "This command requires elevated privilages, which you do not possess. Level %s privilages are required." % str(cmdclass.permissionLevel))
                    return

            if not cmdclass.manArgCheck:
                if not (len(args) == len(cmdclass.arguments) or (len(args) >= len(cmdclass.arguments) and cmdclass.permitExtraArgs)):
                    self.send_PrivMsg(event.user, "This command requires %s arguments" % str(len(cmdclass.arguments)))
                    return

                for x in range(len(cmdclass.arguments)):
                    if cmdclass.arguments[x] == "int":
                        if not (args[x].isdecimal() or "." in args[x]):
                            if cmdclass.defaultArgs[x] == "":
                                cmdclass.on_fail(event)
                                return
                            else:
                                args[x] = cmdclass.defaultArgs[x]
                        else:
                            args[x] = int(args[x])

                    elif cmdclass.arguments[x] == "float":
                        if not (args[x].isdecimal()):
                            if cmdclass.defaultArgs[x] == "":
                                cmdclass.on_fail(event)
                                return
                            else:
                                args[x] = cmdclass.defaultArgs[x]
                        else:
                            args[x] = float(args[x])
                    elif cmdclass.arguments[x] == "str":
                        if len(cmdclass.defaultArgs) > x:
                            if cmdclass.defaultArgs[x] == "":
                                cmdclass.on_fail(event)
                                return
                            else:
                                args[x] = cmdclass.defaultArgs[x]
            else:
                if cmdclass.checkArgs(event, *args):
                    pass
                else:
                    return

            cmdclass.on_call(event, *args)
        else:
            pass
            self.send_PrivMsg(event.user, "%s is not a valid command." % cmd)