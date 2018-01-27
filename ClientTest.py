import socket, sys, select

if __name__ == "__main__":

    host = socket.gethostname()
    port = 12354

    s = socket.socket()

    try:
        s.connect((host, port))
    except:
        print 'Unable to connect'
        sys.exit()

    rlist = [sys.stdin, s]

    try:

        while True:
            readList, writeList, errorList = select.select(rList, [], [])

            quitProgram = False

            for element in readList:
                if element == s:
                    data = s.recv(4096)
                    if not data:
                        print "this connection is not available"
                    else:
                        print data
                else:
                    data = sys.stdin.readline()
                    s.send(data)
                    if data == 'q':
                        quitProgram = True
                        break

            if quitProgram:
                s.close()
                break
    except:
        s.close()


