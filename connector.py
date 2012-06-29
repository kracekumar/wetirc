#! /usr/bin/env python
#! -*- utf:8 -*-

#twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

#system imports
import datetime
import sys
import random

import settings


def generate_nick(nickname):
    return nickname + str(random.randint(settings.NICK_START, settings.NICK_END ))


class LogBot(irc.IRCClient):
    """
    A Logging IRC bot
    """
    nickname = generate_nick(settings.NICKNAME)
    is_joined = False

    def get_current_time(self):
        return datetime.datetime.utcnow()

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.is_joined = True
        with open(''.join(['meta', '_', self.get_current_time().strftime("%Y-%m-%d"), '.log']), "a") as f:
            f.write("[connected at %s] \n" % self.get_current_time().strftime("[%H:%M:%S]"))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        with open(''.join(['meta', '_', self.get_current_time().strftime("%Y-%m-%d"), '.log']), "a") as f:
            f.write("[disconnected at %s]" % self.get_current_time().strftime("[%H:%M:%S]"))


    def dataReceived(self, data):
        irc.IRCClient.dataReceived(self, data)
        #print data
        if data not in ('', None) and data.find('#') != -1:
            pass

    #callbacks for events
    def signedOn(self):
        for channel in self.factory.details:
            print self.join(channel)

    def joined(self, channel):
        self.is_joined = True
        with open(''.join(['meta', '_', self.get_current_time().strftime("%Y-%m-%d"), '.log']), "a") as f:
            f.write("[I have joined %s at %s]\n" % (channel, self.get_current_time().strftime("%H:%M:%S")))

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        with open(''.join([channel, '_', self.get_current_time().strftime("%Y-%m-%d"), '.log']), "a") as f:
            print msg
            f.write("[%s]: <%s> %s\n" % (self.get_current_time().strftime("%H:%M:%S"), user, msg))

        #check if someone sends private message
        if channel == self.nickname:
            msg = "I am bot"
            self.msg(user, msg)
            return

        #check if someone is directing message to me
        if msg.find(self.nickname) >= 0:
            msg = "%s I am bot" % user
            self.msg(channel, msg)

    def action(self, user, channel, msg):
        user = user.split('!', 1)[0]
        with open(''.join([channel, '_', self.get_current_time().strftime("%Y-%m-%d"), '.log']), "a") as f:
            f.write("[%s]: * %s %s" % (self.get_current_time().strftime("%H:%M:%S"), user, msg))


    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nicknames."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        with open(''.join(['meta', '_', self.get_current_time().strftime("%Y-%m-%d"), '.log']), "a") as f:
            f.write("[%s]: %s is now known as %s\n" % (self.get_current_time().strftime("%H:%M:%S"), old_nick, new_nick))


    def irc_JOIN(self, prefix, params):
        print "user joined the channel"

    def irc_ERR_NICKNAMEINUSE(self, prefix, params):
        self._attemptedNick = self.alterCollidedNick(self._attemptedNick)
        self.setNick(self._attemptedNick)

    def userJoined(self, user, channel):
        with open(''.join(['meta', '_', self.get_current_time().strftime("%Y-%m-%d"), '.log']), "a") as f:
            f.write("<[%s]: [%s] joined the channel %s>\n" % (self.get_current_time().strftime("%H:%M:%S"), user, channel))

    def userLeft(self, user, channel):
        with open(''.join(['meta', '_', self.get_current_time().strftime("%Y-%m-%d"), '.log']), "a") as f:
            f.write("<[%s]: [%s] user Left the channel %s>" % (self.get_current_time().strftime("%H:%M:%S"), user, channel))


    def userKicked(self, user, channel):
        with open(''.join(['meta', '_', self.get_current_time().strftime("%Y-%m-%d"), '.log']), "a") as f:
            f.write("<[%s]: [%s] kicked from the channel %s>" % (self.get_current_time().strftime("%H:%M:%S"), user, channel))

    def irc_PING(self, prefix, params):
        irc.IRCClient.irc_PING(self, prefix, params)

class LogBotFactory(protocol.ClientFactory):
    """
    Factory for LogBots
    """

    def __init__(self, details):
        self.details = details

    def buildProtocol(self, addr):
        temp = LogBot()
        temp.factory = self
        return temp

    def clientConnectionLost(self, connector, reason):
        """reconnect if disconnected"""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Connection Failed: %s", reason
        reactor.stop()


if __name__ == '__main__':
    #initialize Logging
    log.startLogging(sys.stdout)

    #create factory protocol and application
    now = datetime.date.today().strftime("%Y-%m-%d")
    channels = ["hasgeek", "pocoo", "brubeck", "crunchbang", "twisted"]
    details = {channel: channel + now + '.log' for channel in channels}
    #channels = ["twisted"]
    reactor.connectTCP("irc.freenode.net", 6667, LogBotFactory(details))
    reactor.run()
