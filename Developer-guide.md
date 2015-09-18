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
