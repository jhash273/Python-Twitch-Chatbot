# Contains bot configuration info

HOST = "irc.twitch.tv"
PORT = 6667
USER = "somename" # Insert twitch bot username here
PASS = "oauth" # Insert twitch bot oauth IRC password from https://twitchtools.com/chat-token
CHAN = "twitchchannel" # Insert twitch channel name to be connected to all lowercase -- NOT THE URL
RATE = (20/30) # Messages per second
CONNECT_MSG = "Hi Everyone!" # Message from bot when it connects to server

oplist = {}