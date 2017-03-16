# -*- coding: utf-8 -*-
import socketserver
import json
import time
import ServerRequestParser
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

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
        self.connected = True
        self.currentRoom = None
        #self.server.change_handler_to_chatRoom(self,"main room")
        
        while self.connected: # Loop that listens for messages from the client while not disconnected
            try:
                payload_as_dict = self.recv_one_message() # receives payload as one regardless of how big it is, and returns as a dict 
                response_as_dict = parser.parse(payload_as_dict, self) # parse the request and return message
                if(response_as_dict != None): # if the response to the request is None, it should not send a message to Client
                    self.send_one_message(response_as_dict)
            except ConnectionResetError: # handle client disconnecting
                self.handle_disconnected_client()
            print()

    def recv_one_message(self): # receives request from the client regardless of size, by first receiving a declaring payload with size of request
        payload = self.connection.recv(4096)
        payload = payload.decode()
        payload = json.loads(payload)
        #print("---received payload:")
        #print(payload)
        if(payload["request"] == "recv_size"): # every sent message from client should send a "recv_size" request first
            payload = self.recv_all(int(payload["content"]))
            payload = payload.decode()
            payload = json.loads(payload)
            #print("---payload from client merged together and loaded to dict: ")
            #print(payload)
        return payload

    def recv_all(self, size):
        buf = b''
        while size:
            newbuf = self.connection.recv(size)
            if not newbuf : return None
            buf += newbuf
            size -= len(newbuf)
        return buf

    def send_one_message(self, payload_as_dict): # sends a daclaring message telling the size of the incoming payload, then sends the payload
        #print("---response sending to client:")
        #print(payload_as_dict)
        data = json.dumps(payload_as_dict)
        data = data.encode()
        length = len(data)
        declaring_dict = {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "recv_size", "content" : length}
        #print("--- declaring dict sending to client:")
        #print(declaring_dict) 
        declaring_dict = json.dumps(declaring_dict)
        declaring_dict = declaring_dict.encode()
        self.connection.sendall(declaring_dict)
        time.sleep(0.1)
        self.connection.sendall(data)
            
    def handle_disconnected_client(self): # handles disconnectes user by logging handler and username out, then closing socket and ending loop in this thread
        #print("--- " + self.username + " disconnected from the server. removing username and handler from connectedUsers, reseting username to "", then printing connectedUsers:")
        parser.parse({"request" : "logout" , "content" : None}, self) # log the clientHandler of the connectedUserslist dont need the return message
        self.connection.close()
        self.connected = False # stop loops receiveing from socket
        
        

       
       
       
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    #__slots__=("connectedUsers")
    connectedUsers = {}
    chatRoomHistory = {"main room" : [] }  # holds chatroomName and history
    chatRoomUsers = {"main room" : []} # holds chatroomName and connexted users in room
    messageHistory = []
    allow_reuse_address = True
    

    #TODO
    def send_broadcast_message(self, message_dict):
        for user in self.connectedUsers:
            self.connectedUsers[user].send_one_message(message_dict)
            
    def change_handler_to_chatRoom(self,client_handler, room_name):
        if(client_handler.currentRoom != room_name):
            self.chatRoomUsers[client_handler.currentRoom].remove(client_handler)
            self.chatRoomUsers[room_name].append(client_handler)
    
    def remove_handler_from_chatroom(self,client_handler):
        self.chatRoomUsers[client_handler.currentRoom].remove(client_handler)
            

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9001
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    parser = ServerRequestParser.ServerRequestParser(server)        ## TODO how to add variables in top to server????
    server.serve_forever()
