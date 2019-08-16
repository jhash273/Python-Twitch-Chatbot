# Utility functions

import config
import urllib.request
import json
import time

def chat(socket, msg):
    """
    Send chat message to server
    :param socket: socket to send the message (int)
    :param msg: message to send (string)
    """
    socket.send(f"PRIVMSG #{config.CHAN} :{msg}\r\n")

def ban(socket, user):
    """
    Ban a user
    :param socket: socket to send the ban command (int)
    :param user: user to ban (string)
    """
    chat(socket, f".ban {user}")

def timeout(socket, user, seconds=600):
    """
    Time out a user
    :param socket: socket to send the timeout command (int)
    :param user: user to be timed out (string)
    :param seconds: time to timout user (int) (default: 600)
    :return: 
    """
    chat(socket, f".timeout {user, seconds}")

# TODO find more effective way to iteratr through JSON list only once or use JSON as oplist
def threadFillOplist():
    """
    Fills Oplist to distinguish moderators
    http://tmi.twitch.tv/group/user/***CHANNEL_NAME_HERE***/chatters
    Channel name is based off CHAN from config.py
    """
    while True:
        try:
            url = f"http://tmi.twitch.tv/group/user/{config.CHAN}/chatters"
            req = urllib.request.Request(url, headers={"accept": "*/*"})
            response = urllib.request.urlopen(req).read()
            if response.find("502 Bad Gateway") == -1:
                config.oplist.clear()
                data = json.loads(response)["chatters"]
                for p in data["moderators"]:
                    config.oplist[p] = "mod"
                for p in data["global_mods"]:
                    config.oplist[p] = "global_mod"
                for p in data["admins"]:
                    config.oplist[p] = "admin"
                for p in data["staff"]:
                    config.oplist[p] = "staff"
        except:
            'do nothing'
        time.sleep(5)


def isAllowed(user):
    """
    Determine if user is permitted to access/use bot
    :param user: twitch username
    :return: Bool if username is in the oplist
    """
    return user in config.oplist

