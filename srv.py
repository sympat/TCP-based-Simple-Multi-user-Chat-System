import socket, select, sys

# send to me
def sendToSocket(socket, msg):
	socket.send(msg.encode('utf-8'))

# send to server
def printMsg(msg):
	sys.stdout.write(msg)

# send to other user
def sendToOtherSocket(socket_list, serverSocket, mySocket, msg):
	for socket in socket_list:
		if socket != serverSocket and socket != mySocket:
			socket.send(msg.encode('utf-8'))

# disconnect this user
def disconnectSocket(socket_list, users, mySocket):
	if mySocket in socket_list:
		socket_list.remove(mySocket)
	del users[mySocket]
	mySocket.close()

def runServer():
	socket_list = []
	users = {}
	host = ""
	port = 8888

	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.bind((host, port))
	serverSocket.listen()
	socket_list.append(serverSocket)

	sys.stdout.write("Chat Server started on port %d\n" %port)

	while True:
		try:	
			readReady, writeReady, exceptReady = select.select(socket_list, [], [])
			for readSocket in readReady:
				# if new user enter this chat,
				if readSocket == serverSocket:
					newSocket, newAddr = serverSocket.accept()

					# add new connected socket to read list to detect data.
					socket_list.append(newSocket)
					users[newSocket] = newAddr

					# send to this user.
					send_msg = "> Connected to the char server (%d user online)\n" %(len(users))
					sendToSocket(newSocket, send_msg)

					# send to server console and other users.
					send_msg = '> New User %s:%s entered (%d user online)\n' %(newAddr[0], newAddr[1], len(users))
					printMsg(send_msg)
					sendToOtherSocket(socket_list, serverSocket, newSocket, send_msg)
				# if any user send message to chat server,
				else:
					try:
						# receive data from client.
						userAddr = users[readSocket]
						recv_data = readSocket.recv(1024)

						# if no data receive,
						if not recv_data:
							# disconnect socket.
							disconnectSocket(socket_list, users, readSocket)

							# send msg to server console and other users.
							send_msg = '< The User %s:%s left (%d user online)\n' %(userAddr[0], userAddr[1], len(users))
							printMsg(send_msg)
							sendToOtherSocket(socket_list, serverSocket, readSocket, send_msg)
						# else data receive,
						else:
							# decode received data to msg.
							recv_msg = recv_data.decode('utf-8')

							# send msg to server console and other users.
							send_msg = "[%s:%s] %s" % (userAddr[0], userAddr[1], recv_msg)
							printMsg(send_msg)
							sendToOtherSocket(socket_list, serverSocket, readSocket, send_msg)
					except:
						# disconnect socket.
						disconnectSocket(socket_list, users, readSocket)
						sys.stdout.write("Error occur\n")
		except KeyboardInterrupt:
			serverSocket.close()
			sys.exit()

if __name__ == "__main__":
	runServer()