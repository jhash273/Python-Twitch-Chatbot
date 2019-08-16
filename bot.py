import config
import utils
import socket
import re
import time
import _thread


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
        if response == "PING :tmi.twitch.tv\r\n": # Handle twitch ping to maintain connection
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(response)


if __name__ == "__main__":
    main()
