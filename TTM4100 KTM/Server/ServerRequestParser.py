import time
import json

class ServerRequestParser():
    def __init__(self, server):
        self.server = server
        self.possible_requests = {
            "login" : self.login_user, # done
            "logout" : self.logout_user, # done
            "msg" : self.incoming_message, # done
            "names" : self.list_users, # done
            "help" : self.view_help, # done
            "history" : self.history, # done
            "chatrooms" : self.chatrooms,
            "roomchange" : self.change_chatroom,
            "roomcreate" : self.create_chatroom
            # more requests are optional
        }
        self.possible_unlogged_request = ['login', 'names', 'help', 'history']
    
    
    
    
    
    def parse(self, payload_as_dict, client_handler):
        if(payload_as_dict["request"] in self.possible_requests):
            if(client_handler.username != "" or payload_as_dict["request"] in self.possible_unlogged_request):     
                print("---request receives IS valid")
                return self.possible_requests[payload_as_dict["request"]](payload_as_dict, client_handler) # calls correct function with payload argument
            else:
                return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),"sender" : "server","response" : "error", 
                    "content" : "Must be logged in with a username to use this functionality. Enter 'help' for a quick guide" }
        else:
            print("---request received is NOT valid")
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),
                    "sender" : "server",
                    "response" : "error",
                    "content" : '"'  + payload_as_dict["request"] + '" is not a valid request' }  
        
    def chatrooms(self, payload_as_dict, client_handler):
        pass    
    
    def change_chatroom(self, payload_as_dict, client_handler):
        pass  
    
    def create_chatroom(self, payload_as_dict, client_handler):
        pass  
    
    def login_user(self, payload, client_handler):
        if(payload["content"] in self.server.connectedUsers or payload["content"] == "server"): # username alrady taken
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "error", 
                    "content" : "Username " + '"'  + payload["content"] + '" is already taken by connected user. Log in with another username' }
        elif(payload["content"] == None):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),"sender" : "server","response" : "error", 
                    "content" : "You must login with a username. Log in with command: 'login <username>'" }
        elif(client_handler.username != ""):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),"sender" : "server", "response" : "error", 
                    "content" : "You already have a username for this session" }
        elif(len(payload["content"]) > 30):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'),"sender" : "server", "response" : "error", 
                    "content" : "Username must be less than 30 characters" }
        else:
            client_handler.username = payload["content"]
            self.server.send_broadcast_message({"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "message",
                                                 "content" : client_handler.username + " has just logged in!" })
            self.server.connectedUsers[client_handler.username] = client_handler
            #print("---printing connectedUsers AFTER trying to add username and client_handler:")
            #print(self.server.connectedUsers)
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server","response" : "info",
                "content" : "Succsessfull login. Your username is: " + payload["content"] }
            
    
    def logout_user(self,payload, client_handler):
        if(client_handler.username in self.server.connectedUsers and payload["content"] == None):
            #print("---printing connectedUsers BEFORE trying to delete username and client_handler:")
            #print(self.server.connectedUsers)
            del self.server.connectedUsers[client_handler.username] # remove username and client_handler from connectesd users
            self.server.send_broadcast_message({"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "message",
                                     "content" : client_handler.username + " has just logged out..." })
            #print("---printing connectedUsers after trying to delete username and client_handler:")
            #print(self.server.connectedUsers)
            client_handler.username = "" # reset username for this clientHandler
            client_handler.currentRoom = "main room"
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "info",
                "content" : "You have been logged out" }
        elif(payload["content"] != None):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "error",
                "content" : "logout is only done with command: 'logout'" }
        #=======================================================================
        # else:
        #     return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "error",
        #         "content" : "You are not logged in, so you cant log out, duh..." }
        #=======================================================================
    
    def incoming_message(self,payload,client_handler):
        message_dict = {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : client_handler.username, "response" : "message", "content" : payload["content"]}
        self.server.messageHistory.append(message_dict)
        self.server.send_broadcast_message(message_dict)
            
    
    def list_users(self, payload, client_handler):
        if(len(self.server.connectedUsers) == 0 and payload["content"] is None):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "info",
                "content" : "\nNo users are currently logged in" }
        elif(payload["content"] is not None):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "error",
                "content" : "listing active usernames is only done with command: 'names'" }   
        else:
            usernamesConnected = "\n"
            for username in self.server.connectedUsers:
                usernamesConnected += username + "\n"
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "info",
                    "content" : usernamesConnected }
    
    def view_help(self, payload, client_handler):
        if(payload["content"] is not None):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "error",
                "content" : "simply type 'help' for help command" }   
        return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "info",
                "content" : "\nValid requests:\n" 
                + "login <username> -> log in with given username\n"
                + "logout -> log out with current username\n"
                + "disconnect -> disconnect from the server\nmsg <message content> -> sends a message to the server with the message content\n"
                + "names -> return username of connected users\n"
                + "history -> returns the history of all messages sent by users to the server\n" }
    
    def history(self, payload, client_handler):
        if(payload["content"] is not None):
            return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "error",
                "content" : "To get message history, type only 'history'" } 
        else:
            if(len(self.server.messageHistory) == 0):
                return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server", "response" : "info",
                "content" : "No messages in history..." } 
            else:
                dict_history = {}
                i = 0
                for saved_dict in self.server.messageHistory:
                    dict_history[i] = saved_dict
                    i+=1
                #print("---dict history sent in content:")
                #print(dict_history)
                return {"timestamp" : time.strftime('%Y/%m/%d %H:%M:%S'), "sender" : "server","response" : "history",
                        "content" : dict_history }
            
            
    

