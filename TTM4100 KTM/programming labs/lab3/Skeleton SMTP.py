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
	print('220 reply not received from server.')


# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '250':
	print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
# Fill in start
clientSocket.send("MAIL FROM:snorreob@ntnu.no\r\n")
recv3 = clientSocket.recv(1024)
print(recv3)
if recv3[:3] != '250':
	print('250 reply not received from server.')
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start
clientSocket.send("RCPT To: snorreob@stud.ntnu.no\r\n")
recv4 = clientSocket.recv(1024)
print(recv4)
if recv4[:3] != '250':
	print('250 reply not received from server.')
# Fill in end

# Send DATA command and print server response.
# Fill in start
clientSocket.send("DATA\r\n")
recv5 = clientSocket.recv(1024)
print(recv5)
if(recv5[:3] != '354'):
	print('354 reply not recieved from server.')
# Fill in end

# Send message data.
# Fill in start
clientSocket.send("From: Snorre test snorreob@stud.ntnu.no\r\n")
clientSocket.send("To: Snorre snorreob@ntnu.no\r\n")
clientSocket.send("Cc: SB snorrebortnes@gmail.com\r\n")
clientSocket.send("Date: today\r\n")
clientSocket.send("Suvject: test message\r\n")
clientSocket.send(" \r\n")
clientSocket.send("Hello Snorre\r\n")
clientSocket.send("Sending a test message usiong SMPT protocoll\r\n")
clientSocket.send("Snorre\r\n")
# Fill in end
# Message ends with a single period.
# Fill in start
clientSocket.send("\r\n.\r\n")
recv6 = clientSocket.recv(1024)
print(recv6)
if(recv6[:3] != '250'):
	print('250 reply not recieved from server.')

# Fill in end

# Send QUIT command and get server response.
# Fill in start
clientSocket.send("QUITS: 221 Bye")
# Fill in end
