import socket, sys, select

def prompt():
	sys.stdout.write("[You] ")
	sys.stdout.flush()

def printMsg(msg):
	sys.stdout.write('\r')
	sys.stdout.write(msg)
	sys.stdout.flush()

def sendToSocket(socket, msg):
	socket.send(msg.encode('utf-8'))

def disconnectSocket(mySocket):
	mySocket.close()
	sys.exit()

def runClient():
	if(len(sys.argv) < 3) :
		sys.stdout.write('Usage : python chat_client.py hostname port\n')
		sys.exit()

	socket_list = [sys.stdin]
	host = sys.argv[1]
	port = int(sys.argv[2])

	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((host, port))
	socket_list.append(clientSocket)

	while True:
		try:
			prompt()
			readReady, writeReady, exceptReady = select.select(socket_list, [], [])
			for readSocket in readReady:
				# if server send msg to client,
				if readSocket == clientSocket:
					# receive data from server.
					recv_data = (readSocket.recv(1024))

					# if no data receive,
					if not recv_data:
						# print msg.
						printMsg("< You have been disconnected.\n")
						# disconnect socket.
						disconnectSocket(readSocket)
					# else data receive,
					else:
						# print received msg.
						printMsg(recv_data.decode('utf-8'))
				# if client want to send msg,
				else:
					# input msg.
					send_msg = sys.stdin.readline()
					# send to server.
					sendToSocket(clientSocket, send_msg)
		except KeyboardInterrupt:
			# disconnect socket.
			disconnectSocket(clientSocket)

if __name__ == "__main__":
	runClient()