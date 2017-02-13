from socket import *
import threading


class Connection(threading.Thread):
	def __init__(self, connectionSocket):
		self.connectionSocket = connectionSocket
		super(Connection, self).__init__()
		

	def run(self):
		while True:
			try:
				message = self.connectionSocket.recv(1024)
				message.decode('utf-8')
				filepath = message.split()[1]
				f = open(filepath[1:])
				outdata = f.read
				self.connectionSocket.send("HTTP/1.1 200\r\n\r\n".encode('utf-8'))
				for i in range(0, len(outdata)):
					self.connectionSocket.send(outdata[i].encode('utf-8'))
				self.connectionSocket.send("\r\n".encode('utf-8'))
				self.connectionSocket.close()
			except IOError:
				self.connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode('utf-8'))
				self.connectionSocket.close()


class server:
	def __init__(self):
		self.serverPort = 6789
		self.serverSocket = socket(AF_INET,SOCK_STREAM)
		
	def startServer(self):
		self.serverSocket.bind(('',self.serverPort))
		self.serverSocket.listen(5)
		while True:
			print("Waiting for connection...")
			connectionSocket, addr = self.serverSocket.accept()
			print("Someone connected!")
			connectionHandler = Connection(connectionSocket)
			connectionHandler.start()
		serverSocket.close()


server = server()
server.startServer()
