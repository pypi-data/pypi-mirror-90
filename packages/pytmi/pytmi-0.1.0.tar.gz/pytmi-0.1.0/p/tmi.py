import socket
import time
import random
from typing import Optional, Union


MAX_MESSAGE_SIZE = 512
PING_MESSAGE = "PING :tmi.twitch.tv\r\n"
PONG_MESSAGE = "PONG :tmi.twitch.tv\r\n"


__all__ = [MAX_MESSAGE_SIZE]


class TmiClient:
    def __init__(self, ssl: bool = False, host: str = "irc.chat.twitch.tv", port: Union[str, int] = -1):
        self.ssl = ssl
        self.host = host

        if isinstance(port, str):
            self.port = int(port)
        elif port == -1:
            self.port = 6697 if ssl else 6667
        else:
            self.port = port

        self.sent = 0
        self.recvd = 0
        self.__sock: Optional[socket.socket] = None


    def connect(self, nick: Optional[str] = None, token: Optional[str] = None, auth: bool = True, max_retry: int = 8) -> bool:
        nologin = not auth

        if not nick or not token or nologin:
            nick = "justinfan" + str(123)
            token = "random_token_123"

        retry = max_retry
        backoff = 0

        while retry >= 0:
            retry -= 1
            
            if backoff <= 1:
                backoff += 1
            else:
                backoff *= 2
                time.sleep(backoff)

            try:
                if nologin:
                    nick + str(random.randint(123, 789))

                if self.__connect(nick, token):
                    return True
            except:
                break

        return False


    def __connect(self, nick: str, token: str) -> bool:
        if self.__sock != None:
            return

        self.__sock = socket.socket()
        addr_tuple = (self.host, self.port)
        self.__sock.connect(addr_tuple)

        if not token.startswith("oauth:"):
            token = "oauth:" + token

        token_buf = "PASS " + token + "\r\n"
        nick_buf = "NICK " + nick + "\r\n"

        self.sent += self.__sock.send(token_buf.encode())
        self.sent += self.__sock.send(nick_buf.encode())

        buf = self.__sock.recv(MAX_MESSAGE_SIZE)
        self.recvd += len(buf)

        if not buf.decode().find(":Welcome, GLHF!"):
            return False

        # Enables TMI extensions over the IRC protocol
        self.sent += self.__sock.send("CAP REQ :twitch.tv/membership\r\n".encode())
        self.sent += self.__sock.send("CAP REQ :twitch.tv/tags\r\n".encode())
        self.sent += self.__sock.send("CAP REQ :twitch.tv/commands\r\n".encode())

        return True


    def disconnect(self) -> None:
        try:
            self.__sock.close()
        except:
            pass

        self.__sock = None


    def send(self, message: Union[str, bytes]) -> None:
        if isinstance(message, str):
            self.sent += self.__sock.send(message.encode())

        elif isinstance(message, bytes):
            self.sent += self.__sock.send(message)


    def recv(self) -> bytes:
        buf = self.__sock.recv(MAX_MESSAGE_SIZE)
        buflen = len(buf)

        # if buflen < MAX_MESSAGE_SIZE:
        #     while buflen < MAX_MESSAGE_SIZE or not buf.endswith("\r\n".encode()):
        #         buf += self.__sock.recv(MAX_MESSAGE_SIZE)
        #         buflen = len(buf)

        if buflen < MAX_MESSAGE_SIZE or not buf.endswith("\r\n".encode()):
            buf += self.__sock.recv(MAX_MESSAGE_SIZE)
            buflen = len(buf)

        self.sent += buflen

        buf = buf.decode()

        if PING_MESSAGE in buf:
            self.send(PONG_MESSAGE)
            return buf.replace(PING_MESSAGE, "", 1)

        return buf


    def join(self, channel: str) -> None:
        if not channel.startswith("#"):
            channel = "#" + channel

        self.send("JOIN " + channel + "\r\n")


    def part(self, channel: str) -> None:
        if not channel.startswith("#"):
            channel = "#" + channel

        self.send("PART " + channel + "\r\n")


__all__.append(TmiClient)
