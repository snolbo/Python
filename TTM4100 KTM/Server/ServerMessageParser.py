import json
from Server.Server import ClientHandler
import time

class ServerMessageParser():
    def __init__(self):
        self.possible_requests = {
            "login" : self.login_user,
            "logout" : self.logout_user,
            "msg" : self.incoming_message,
            "names" : self.list_users,
            "help" : self.view_help,
            # more requests are optional
        }
    
    def parse(self, payload, client_handler):
        payload = json.loads(payload) # payload is not dict
        if(payload["request"] in self.possible_requests):
            return self.possible_requests(payload["request"])(payload, client_handler) # calls correct function with payload argument
        else:
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),
                    "sender" : "server",
                    "response" : "error",
                    "content" : '"'  + payload["request"] + '" is not a valid request' }
        
    def login_user(self, payload, client_handler):
        if(payload["content"] in connectedUsers or payload["content"] == "server"): # username alrady taken
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),
                    "sender" : "server",
                    "response" : "error",
                    "content" : "username " + '"'  + payload["content"] + '" is already taken' }
        elif(payload["content"] == ""):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),
                    "sender" : "server",
                    "response" : "error",
                    "content" : "not a valid username" }
        elif(client_handler.username != ""):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),
                "sender" : "server",
                "response" : "error",
                "content" : "you already have a username for this session" }
        else:
            client_handler.username = payload["content"]
            connectedUsers.append(client_handler.username)
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),
                "sender" : "server",
                "response" : "info",
                "content" : "Succsessfull login. Your username is: " + payload["content"] }
            
    
    def logout_user(self,payload, client_handler):
        if(client_handler.username in connectedUsers):
            connectedUsers.remove(client_handler.username)
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),
                "sender" : "server",
                "response" : "info",
                "content" : "You have been logged out" }
    
    def incoming_message(self,payload):
        pass
    
    def list_users(self, payload):
        pass
    
    def view_help(self, payload):
        pass

