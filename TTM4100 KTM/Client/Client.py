# -*- coding: utf-8 -*-
import socket
import MessageReceiver
import json
import sys
import time

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
        self.connected = True
        self.host = host
        self.server_port = server_port
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        print("---Connected to server")
        receiver = MessageReceiver.MessageReceiver(self)
        receiver.start()
        while self.connected: 
            self.read_and_send_data()
            
        
    def disconnect(self):
        self.connected = False
        self.connection.close()
        

    def receive_message(self, message):
        print(message)

    def read_and_send_data(self):
        data = input()
        data = self.format_payload(data) # format the data to json and send via socket
        try:
            self.send_one_message(data)
        except Exception:
            if(not self.connected):
                print("No longer connected, cant send data...")
            else:
                print(Exception.__cause__)
                
            
    
    def read_input(self): 
        return input()

    def format_payload(self, data):
        data_list = data.partition(" ") # partition data at first space
        if(data_list[0] == "disconnect"):
            self.disconnect()
            self.connected = False
            return
        elif(data_list[2] != ""):
            payload = { "request" : data_list[0], "content" : data_list[2]}
        else: 
            payload = { "request" : data_list[0], "content" : None}
        #print("---payload formated from user input:")
        #print(payload)
        return payload
        
    
    def send_one_message(self, data): # sends a daclaring message telling the size of the incomiing data, then sends the data
        #print("---request sending to server:")
        #print(data)
        data = json.dumps(data)
        data = data.encode()
        length = len(data)
        declaring_dict = {"request": "recv_size", "content" : length}
        #print("--- declaring dict sending to server:")
        #print(declaring_dict)
        declaring_dict = json.dumps(declaring_dict)
        declaring_dict = declaring_dict.encode()
        self.connection.sendall(declaring_dict)
        time.sleep(0.1)
        self.connection.sendall(data)
    # More methods may be needed!
    



if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9001)
