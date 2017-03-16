# -*- coding: utf-8 -*-
from threading import Thread
import ClientMessageParser
import json
import sys

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client):
        """
        This method is executed when creating a new MessageReceiver object
        """
        Thread.__init__(self)
        # Flag to run thread as a deamon
        self.daemon = True
        # TODO: Finish initialization of MessageReceiver
        self.client = client
        self.parser = ClientMessageParser.ClientMessageParser()

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while self.client.connected:
            try:
                payload = self.recv_one_message()
            except ConnectionResetError:
                self.client.receive_message("Either server has stopped, or the apocalypse has started... (program has stopped and exited)")
                self.client.disconnect()
                break
                            
            parsed_message = self.parser.parse(payload)
            #print("---client.receive_message: (let client print parsed and formated message for user message)")
            self.client.receive_message(parsed_message)
    
    def recv_one_message(self):
        payload = self.client.connection.recv(4096)
        payload = payload.decode()
        #print("---received payload:")
        payload = json.loads(payload)
        #print(payload)
        if(payload["response"] == "recv_size"):
            payload = self.recv_all(int(payload["content"]))
            payload = payload.decode()
            payload = json.loads(payload)
            #print("---payload merged together and loads to dict: ")
            #print(payload)
        #print("---payload received from server:")
        #print(payload)
        return payload
    
    def recv_all(self, size):
        buf = b''
        while size:
            newbuf = self.client.connection.recv(size)
            if not newbuf : return None
            buf += newbuf
            size -= len(newbuf)
        return buf
    