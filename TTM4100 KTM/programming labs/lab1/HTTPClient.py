from socket import *
import time



serverName = 'localhost'
serverPort= 6793;
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = "GET /HelloWorld.html HTTP/1.1"
#sentence += input('Input filename:')
print(sentence)
clientSocket.send(sentence.encode('utf-8'))

string = ""
#for i in range(0,100): #this will fail if response is long
startTime = time.time()
while (time.time() - startTime < 0.5):
	response = clientSocket.recv(1024)
	response.decode('utf-8')
	string+=response



print(string)
clientSocket.close()


