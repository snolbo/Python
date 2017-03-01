import json
import time


class ClientMessageParser():
    def __init__(self):

        self.possible_responses = {
            "error": self.parse_error,
            "info": self.parse_info,
            "message": self.parse_message,
            "history": self.parse_history
	    # More key:values pairs are optional	
        }

    def parse(self, payload):
        if payload["response"] in self.possible_responses:
            return self.possible_responses[payload["response"]](payload) # calls the corrent function in dict with payload argument
        else:
            # Response not sopported, tell client that response is not supported TODO
            print('"'+ payload["response"] + '"' + " is not a response that is supported")
            

    def parse_error(self, payload):
        return "Error message recieved from server: " + payload["content"]
    
    def parse_info(self, payload):
        return "Information message recieved from server: " + payload["content"] 
    
    def parse_message(self, payload):
        return payload["sender"] + ": " + payload["content"]
        
    
    def parse_history(self, payload):
        history_string =""
        for message_payload in payload["content"]: # for every string in the list
            message_payload_dict =  json.loads(message_payload) # decode json streing to dict
            history_string += message_payload_dict["timestamp"] + "  " + message_payload_dict["sender"] + ": " + message_payload_dict["content"] +"\n" # format message time, sender and content
        return history_string
    
        # Include more methods for handling optional responses... 




#===============================================================================
# dict = {"key1" : 1 , "key2" : 2}
# dictString = json.dumps(dict)
# print(dictString)
# print(dict["key1"])
# dict2 = json.loads(dictString)
# print(dict2)
# print(dict2["key2"])
#   
#===============================================================================
#===============================================================================
# print("request:","  ", end ="")
# string = input()
# print("content:","  ", end ="")
# string2 = input()
# print(type(string2) == int)
#   
# data = input()
# print(data)
# data = data.partition(" ")
# print(data)
# data = [data[0], data[2]]
# print(data)
# 
# a = time.strftime('%Y/%m/%d %H:%M:%S')
# print(a)
# string = "hei"
# split = string.partition(" ")
# print(split)
#===============================================================================
