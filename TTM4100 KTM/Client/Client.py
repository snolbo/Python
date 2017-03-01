# -*- coding: utf-8 -*-
import socket
import MessageReceiver
import json

class Client:
    """
    This is the chat client class
    """
    

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        print("Connected to server")
        receiver = MessageReceiver.MessageReceiver(self)
        receiver.start()
        while True: 
            self.read_and_send_data()
            
        
    def disconnect(self):
        self.connection.close()

    def receive_message(self, message):
        print(message)

    def read_and_send_data(self):
        data = input()
        self.send_payload(data) # format the data to json and send via socket
    
    def read_input(self): 
        return input()

    def send_payload(self, data):
        data_list = data.partition(" ") # partition data at first space 
        if(data_list[2] != ""):
            payload = { "request" : data_list[0], "content" : data_list[2]}
        else: 
            payload = { "request" : data_list[0], "content" : None}
        
        print("---payload formated from user input:")
        print(payload)
        
        payload = json.dumps(payload) # payload is now string in json format
        payload = payload.encode()  #payload is now byte-like
        self.connection.send(payload)
    
    # More methods may be needed!
    
    


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
