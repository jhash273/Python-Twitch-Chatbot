import config
import utils
import socket
import re
import time
import _thread
import json


def main():
    # Networking functions
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send(f"PASS {config.PASS}\r\n".encode("utf-8"))
    s.send(f"NICK {config.USER}\r\n".encode("utf-8"))
    s.send(f"JOIN #{config.CHAN}\r\n".encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, config.CONNECT_MSG)

    _thread.start_new_thread(utils.threadFillOplist, ())

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":  # Handle twitch ping to maintain connection
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)

            # Open and load all chat commands
            chat_commands = json.load(open("./commands", "r"))

            if message[0] == "!":
                message = message.split(' ', 1)
                command = message[0]
                message = message[1]

            # First generic commands pre FILE IO
            # if message.strip() == '!time':
            #    utils.chat(s, "It is currently " + time.strftime("%I:%M %p %Z on %A, %B %d, %Y. "))
            # if message.strip() == "!messages" and utils.isAllowed(username):
            #    utils.chat(s, "Please give me a follow on ")
            #    utils.chat(s, "Support at ")
        time.sleep(1)


if __name__ == "__main__":
    main()
