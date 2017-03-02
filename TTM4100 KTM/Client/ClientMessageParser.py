import json
import time


class ClientMessageParser():
    def __init__(self):

        self.possible_responses = {
            "error": self.parse_error, 
            "info": self.parse_info,
            "message": self.parse_message,
            "history": self.parse_history # done
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
        #print("---receives history payload:")
        #print(payload)
        history_string =""
        content = payload["content"] # gets the dict of dicts
        #print("---content is dict?:  " + str(type(content) == dict))
        #print("---length of content: " + str(len(content)))
        for i in range(0,len(content)): # for all elements in dict, as they are saved with index of message since dicts are nonordered
            saved_dict = content[str(i)]
            #print(saved_dict) #prints the dict that is the original sent message
            history_string += saved_dict["timestamp"] + "    " + saved_dict["sender"] + ": " + saved_dict["content"] + "\n"
        return history_string
    
        # Include more methods for handling optional responses... 
