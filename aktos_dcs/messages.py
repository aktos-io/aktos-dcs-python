import time
import uuid
import copy
#import msgpack
import ujson as json

# message functions
def unpack(message):
    #return msgpack.unpackb(message)
    return json.loads(message)

def pack(msg):
    #assert(isinstance(msg, Message)) # this does not consume cpu
    #return msgpack.packb(msg)
    return json.dumps(msg)

def envelp(message, msg_id):
    return {
        'sender': [],
        'timestamp': time.time(),
        'msg_id': msg_id, # {{.actor_id}}.{{serial}}
        'payload': message,
    }

def msg_body(msg):
    print "WARNING: This method is depreciated, use get_msg_body() instead."
    return msg['payload'].values()[0]

def get_msg_body(msg):
    return msg['payload'].values()[0]

