# This skeleton is valid for both Python 2.7 and Python 3.
# You should be aware of your additional code for compatibility of the Python version of your choice.

import time
from socket import *
from builtins import str

# Get the server hostname and port as command line arguments                    
host = 'localhost'# FILL IN START		# FILL IN END
port = 12000# FILL IN START		# FILL IN END
timeout = 1 # in seconds
 
# Create UDP client socket
# FILL IN START		

# Note the second parameter is NOT SOCK_STREAM
# but the corresponding to UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind((host,port))
# Set socket timeout as 1 second
clientSocket.settimeout(timeout)

# FILL IN END

# Sequence number of the ping message
ptime = 0  

RTT = []
# Ping for 10 times
while ptime < 10: 
    ptime += 1
    # Format the message to be sent as in the Lab description	
    sendTime = time.time()
    
    data = ("Ping " +  str(ptime) + " " + sendTime.__str__()).encode('utf-8')  # FILL IN START		# FILL IN END
    
    try:
    	# FILL IN START
    	
    # Record the "sent time"
        # already done in sendTime
    # Send the UDP packet with the ping message
        clientSocket.sendto(data,(host,port))
    # Receive the server response
        response,addr = clientSocket.recvfrom(2048)
    # Record the "received time"
        RTT.append(time.time() - sendTime)
    # Display the server response as an output
        response.decode('utf-8')
        print(response)
    # Round trip time is the difference between sent and received time
        #fantastic mathematics! negative times
        
        # FILL IN END
    except:
        # Server does not respond
	# Assume the packet is lost
        print("Request timed out.")
        continue

# Close the client socket
clientSocket.close()
print(RTT)
 
