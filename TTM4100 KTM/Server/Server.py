# -*- coding: utf-8 -*-
import socketserver
import json
import time
import ServerRequestParser

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

## TODO    HOW TO PUT THESE VARIABLE TO BE CONTAINED BY SERVER SO THAT I CAN USE THEM FROM ServerMessageParser???????
chatRooms = {"main room" : ""}  # holds chatroomName and message history
usersInRooms = {}
connectedUsers = {} # holds userName and handler


def broadcast_message():
    pass


class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """


    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.username = ""
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            payload = self.connection.recv(4096)
            payload = payload.decode()
            payload = json.loads(payload) # payload becomes dict
            
            print("---receives payload:")
            print(payload)
                        
            response = parser.parse(payload, self)
            
            print("---response sending to client:")
            print(response)
            
            response = json.dumps(response)
            response = response.encode()
            
            self.connection.send(response)
            

    def disconnet(self):
        self.connection.close()
    
    def send_broadcast_message(self):
       # self.connection.
       pass
       
       
       
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True



if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    parser = ServerRequestParser.ServerRequestParser(server)        ## TODO how to add variables in top to server????

    server.serve_forever()
