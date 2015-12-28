## About 

This is the developer guide for any further implementations of this library in another programming language. 

## Message Format

Messages are simple dictionaries, represented in JSON format. Mandatory keys of a message are as follows: 

  * sender: Array of strings. First element is creator's, rest is forwarders' `id`'s.
  * timestamp: [Unix time stamp](http://www.unixtimestamp.com/)
  * msg_id: a unique message id. practically concatenate `creator_id` and `i` where `i` is sequence number of message
  * payload: a dictionary, described below. 

Payload is basically in `{'Subject': data}` format. Here are some examples: 
  
  * To set `green-led` pin to `True`, one must send the following message: 
  
    Python: 
    
        msg = { 'IoMessage': { 'pin_name': 'green-led', 'val': True } }
              
    Javascript: 
    
        var msg = { IoMessage: { pin_name: 'green-led', val: true } }
  
    LiveScript:
    
        msg = IoMessage: pin_name: \green-led, val: on

        or 
        
        msg = IoMessage: 
               pin_name: \green-led
               val: on 
          
    
So, a full message should look like this:

    {"sender":["5fa6c6d7-077a-4467-9bb3-1f2c2ee58d78","5e7b8786-4885-4e2d-b4c6-98dc21856ba9","3444aadc-ed01-4ce6-94bc-ae144510eb31","41dl-Gj3"],"timestamp":1440885632.49,"msg_id":"5fa6c6d7-077a-4467-9bb3-1f2c2ee58d78.147","payload":{"IoMessage":{"pin_name":"green-led","val":true}}}


# Example C# Implementation Pattern 

1. Create an application that can send and receive strings (eg. 'Hello' and 'Hello back!') via ZeroMQ .
2. Install [aktos-dcs](https://github.com/ceremcem/aktos-dcs). 
3. Edit and set `DEBUG_NETWORK_MESSAGES = True` in `aktos_dcs/gevent_actor.py` file to see the debug messages. 
4. Run `examples/ponger.py`.
5. Send following string (`the_raw_msg`) as is from the new implementation code and see if `broker got message` message is printed in `ponger.py`: 
     
         "{ \"timestamp\": 1451168495.814, \"msg_id\": \"MZ9YV.6\", \"sender\": [\"MZ9YV\", \"cKsNg\"], \"payload\": {\"PongMessage\": {\"text\": \"Hello ponger, this is pinger 1!\"}}}"

  > Note that field strings (like `timestamp` or `msg_id` etc...) SHOULD be in double quotes (like `"msg_id"`, not single quotes (not like `'msg_id'`), else message won't be unpacked by `ponger.py`. 
   
6. Because `timestamp` is too old, message will be dropped. See the following message: 
 
          dropping timeouted message (XXXXX seconds old.)
          filter process done...

7. Update `timestamp` field with a current unix time value. 
   > Note that if you see "key name of object must be string" error, you should check the timestamp value if its decimal separator is dot(`.`), not comma (`,`). 


8. See that messages are not dropped because of they are too old, but they are dropped because they are duplicates. 
9. Append a sequence number to `msg_id` field value. 
10. See messages are reaching `ponger.py` correctly. 
11. Listen for `ponger.py`'s answers. 
12. Move the listener (the subscriber) to a different thread (or `BackgroundWorker`). 
13. Create `msg_id`s and `sender` id randomly. 
