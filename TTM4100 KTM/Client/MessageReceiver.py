# -*- coding: utf-8 -*-
from threading import Thread
import ClientMessageParser
import json

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
        while True:
            payload = self.client.connection.recv(4096)
            payload = payload.decode()
            payload = json.loads(payload)
            print("---payload receives from server:")
            print(payload)
            parsed_message = self.parser.parse(payload)
            print("---parsed message for user:")
            print(parsed_message)
            
            print("---client.receive_message: (let client print message)")
            self.client.receive_message(parsed_message)
            print()
