
import socket, sys, select

from SocketWrapper import *

class Client:

    clientSock = None
    port = 12354
    host = None

    RECV_BUFFER = 4096

    def __init__(self):
        self.host = socket.gethostname()
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect()

    def __connect(self):
        try:
            self.clientSock.connect((self.host, self.port))
        except:
            print "unable to connect server"
        else:
            self.__mainLoop()

    def __closeClient(self):
        self.clientSock.send("CLIENT_SHUTDOWN")
        self.clientSock.close()

    def __mainLoop(self):

        rList = [self.clientSock, sys.stdin]

        try:

            while True:
                readList, writeList, errorList = select.select(rList, [], [])

                quitProgram = False

                for element in readList:
                    if element == self.clientSock:
                        data = socketRecv(self.clientSock, self.RECV_BUFFER)
                        if not data:
                            print "this connection is not available"
                            quitProgram = True
                        else:
                            if data == 'SERVER_SHUTDOWN':
                                quitProgram = True
                                break
                            print data
                    else:
                        data = sys.stdin.readline()

                        if data == 'esc\n':
                            quitProgram = True
                            break
                        else:
                            # remove '\n' and append EOD as segmentation sign
                            socketSend(self.clientSock, data[:-1])

                if quitProgram:
                    self.__closeClient()
                    break

        except KeyboardInterrupt:
            self.__closeClient()

if __name__ == "__main__":

    client = Client()

