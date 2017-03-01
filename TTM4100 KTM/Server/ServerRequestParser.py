import time

class ServerRequestParser():
    def __init__(self, server):
        self.server = server
        self.possible_requests = {
            "login" : self.login_user,
            "logout" : self.logout_user,
            "msg" : self.incoming_message,
            "names" : self.list_users,
            "help" : self.view_help,
            # more requests are optional
        }
    
    def parse(self, payload, client_handler):
        if(payload["request"] in self.possible_requests):
            
            print("---request receives IS valid")
            
            return self.possible_requests[payload["request"]](payload, client_handler) # calls correct function with payload argument
        else:
            
            print("---request received is NOT valid")
            
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),
                    "sender" : "server",
                    "response" : "error",
                    "content" : '"'  + payload["request"] + '" is not a valid request' }
        
    def login_user(self, payload, client_handler):
        if(payload["content"] in self.server.connectedUsers or payload["content"] == "server"): # username alrady taken
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
            self.server.connectedUsers.append(client_handler.username)
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),
                "sender" : "server",
                "response" : "info",
                "content" : "Succsessfull login. Your username is: " + payload["content"] }
            
    
    def logout_user(self,payload, client_handler):
        if(client_handler.username in self.server.connectedUsers):
            self.server.connectedUsers.remove(client_handler.username)
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

