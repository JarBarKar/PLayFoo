import json
import amqp_setup
import os, sys
import requests
from invokes import invoke_http
from threading import Thread



def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log by " + __file__)
    processOrderLog(body)
    print() # print a new line feed

def processOrderLog(data):
    print(json.loads(data)['code'])
    data = data.decode('UTF-8')
    #check if send to activity or error depending on code
    url = "http://localhost:5006/error"
    message = "\n--Worker is passing JSON to error_log.py--\n"
    if(json.loads(data)['code'] in range(200, 300)):
        url = "http://localhost:5005/activity_log"
        print("\n--Worker is passing JSON to activity_log.py--\n")
    print(url, message)
    invoke_http(url, method='POST', json=data)


amqp_setup.check_setup() # to make sure connection and channel are running




#Setting up activity_log exchange and queue
print('--Setting up exchange-- \n')
amqp_setup.channel.exchange_declare(exchange='activity_error_exchange', exchange_type='topic', durable=True)



#Setting up error queue
print('--Setting up error queue-- \n')
amqp_setup.channel.queue_declare(queue='error_queue', durable=True)
amqp_setup.channel.queue_bind(exchange='activity_error_exchange', queue='error_queue', routing_key='error')

print('--Initiate error worker-- \n')
amqp_setup.channel.basic_consume(queue='error_queue', on_message_callback=callback, auto_ack=True)


print('--Setting up activity_log queue-- \n')
amqp_setup.channel.queue_declare(queue='activity_log_queue', durable=True)
amqp_setup.channel.queue_bind(exchange='activity_error_exchange', queue='activity_log_queue', routing_key='info')

print('--Initiate activity_log worker-- \n')
amqp_setup.channel.basic_consume(queue='activity_log_queue', on_message_callback=callback, auto_ack=True)
amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 



print('\n--Start listening for messages....-- \n')
amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 









    
