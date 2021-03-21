import json
import amqp_setup
import os, sys
import requests
from invokes import invoke_http



def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log by " + __file__)
    processOrderLog(body)
    print() # print a new line feed

def processOrderLog(data):
    print('inside order log')
    data = data.decode('UTF-8')
    url = "http://localhost:5005/activity_log"
    invoke_http(url, method='POST', json=data)
    # requests.request('POST', "http://localhost:5005/activity_log", json = data)
    print("--Worker is passing JSON to activity_log.py--\n")

amqp_setup.check_setup() # to make sure connection and channel are running


#Setting up activity_log exchange and queue
print('--Setting up exchange-- \n')
amqp_setup.channel.exchange_declare(exchange='activity_error_exchange', exchange_type='topic', durable=True)

print('--Setting up activity_log queue-- \n')
amqp_setup.channel.queue_declare(queue='activity_log_queue', durable=True)
amqp_setup.channel.queue_bind(exchange='activity_error_exchange', queue='activity_log_queue', routing_key='#')

print('--Initiate activity_log worker-- \n')
amqp_setup.channel.basic_consume(queue='activity_log_queue', on_message_callback=callback, auto_ack=True)
amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 


#Setting up error queue
# amqp_setup.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
# amqp_setup.channel.queue_declare(queue=queue_name, durable=True)
# amqp_setup.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)









    
