# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

from socket import *

# Message to send
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Our mail server is smtp.stud.ntnu.no
mailserver = 'smtp.stud.ntnu.no'

# Create socket called clientSocket and establish a TCP connection 
# (use the appropriate port) with mailserver
#Fill in start
serverPort = 25
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((mailserver,serverPort))
#Fill in end
recv = clientSocket.recv(1024)
print(recv)
if recv[:3] != '220':
	print('220 reply not received from server on connect.')


# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'.encode('utf-8')
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '250':
	print('250 reply not received from server when HELO.')
	

# Send MAIL FROM command and print server response.
# Fill in start
clientSocket.send("MAIL FROM:snorreob@stud.ntnu.no\r\n".encode('utf-8'))
recv3 = clientSocket.recv(1024)
print(recv3)
if recv3[:3] != '250':
	print('250 reply not received from server when MAIL FROM.')
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
clientSocket.send("RCPT To: snorreob@stud.ntnu.no\r\n".encode('utf-8'))
recv4 = clientSocket.recv(1024)
print(recv4)
if recv4[:3] != '250':
	print('250 reply not received from server when RCPT TO.')
# Fill in end

# Send DATA command and print server response.
# Fill in start
clientSocket.send("DATA\r\n".encode('utf-8'))
recv5 = clientSocket.recv(1024)
print(recv5)
if(recv5[:3] != '354'):
	print('354 reply not recieved from server when DATA.')
# Fill in end

# Send message data.
# Fill in start
clientSocket.send("From: Snorre test snorreob@stud.ntnu.no\r\n".encode('utf-8'))
clientSocket.send("To: Snorre snorreob@ntnu.no\r\n".encode('utf-8'))
clientSocket.send("Cc: SB snorrebortnes@gmail.com\r\n".encode('utf-8'))
clientSocket.send("Date: today\r\n".encode('utf-8'))
clientSocket.send("Subject: test message\r\n".encode('utf-8'))
clientSocket.send(" \r\n".encode('utf-8'))
clientSocket.send("Hello Snorre\r\n".encode('utf-8'))
clientSocket.send("Sending a test message using SMPT protocoll\r\n".encode('utf-8'))
clientSocket.send("Snorre\r\n".encode('utf-8'))
# Fill in end
# Message ends with a single period.
# Fill in start
clientSocket.send("\r\n.\r\n".encode('utf-8'))
recv6 = clientSocket.recv(1024)
print(recv6)
if(recv6[:3] != '250'):
	print('250 reply not recieved from server when ENDING DATA.')

# Fill in end

# Send QUIT command and get server response.
# Fill in start
clientSocket.send("QUIT: 221 Bye".encode('utf-8'))
recv7 = clientSocket.recv(1024)
print(recv7)
if(recv7[:3] != '221'):
	print('221 reply not recieved from server when QUIT.')
# Fill in end
