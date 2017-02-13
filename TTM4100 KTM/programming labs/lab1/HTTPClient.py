from socket import *


serverName = 'localhost'
serverPort= 6789;
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

sentence = input('Input filename:')
clientSocket.send(sentence.encode())
response = clientSocket.recv(1024)
print('Recieved from server:')
print(response.decode())
clientSocket.close()


