import pymongo
import random

client= pymongo.MongoClient("mongodb+srv://sowjanya:souji6819@cluster0-k3zzh.mongodb.net/test?retryWrites=true&w=majority")
db1 = client.db

def botResponse(input, uname):
    res = db1.messages.find_one({"user":input})
    # r = db1.messages.find_one({"bot"})
    if(db1.chat_history.find_one( {"username":uname}) == None):
        db1.chat_history.insert_one( {"username":uname,"bot":["Hey,"+uname+"!"],"user":[input] } )
    else:
        db1.chat_history.update_one( {"username":uname}, {"$push":{"user":input}} )
    if(res == None):
        reply = "Ask a different question!"
        db1.chat_history.update_one( {"username":uname}, {"$push":{"bot":reply}} )
        return reply
    db1.chat_history.update_one( {"username":uname}, {"$push":{"bot":res["bot"]}} )   
    return res["bot"] 

# def botResponse(input, userrname):
#     res = db1.messages.find_one({"user":input})
    
#     print('res:' +str(res))
#     if(db1.chat_history.find_one( {"username":userrname}) == None):
#         db1.chat_history.insert_one( {"username":userrname,"bot":["Hey,"+userrname+"!"],"username":[input] } )
#     else:
#         db1.chat_history.update_one( {"username":userrname}, {"$push":{"username":input}} )
#     if(res == None):
#         reply = "ask a different question!"
#         db1.chat_history.update_one( {"username":userrname}, {"$push":{"bot":reply}} )
#         return reply
   
#     db1.chat_history.update_one( {"username":userrname}, {"$push":{"bot":res["response"]}} )   
#     return res["response"] 

def chat_history(username):
    chat = db1.chat_history.find_one( {"username":username} )
    if(chat == None):
        return ""
    return chat 


    


    
