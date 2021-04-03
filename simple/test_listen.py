import json
import os
import amqp_setup
from sqlalchemy import Table, Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime as dt



def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log file by " + __file__)
    print(body)
    # processOrderLog(json.loads(body))
    print() # print a new line feed


def processOrderLog(data):
    print(json.loads(data)['code'])
    data = json.loads(data.decode('UTF-8'))
    #check if send to activity or error depending on code
    log = Activity_Log(code=data['code'],data=json.dumps(data['data']),message=data['message'])

    session.add(log)
    session.commit()
    print("Recording an activity log:")
    print(log)



print('--Setting up activity_log queue-- \n')
amqp_setup.channel.queue_declare(queue='aaron_queue', durable=True)
amqp_setup.channel.queue_bind(exchange='1_roomchat', queue='aaron_queue', routing_key='1.aaron')

print('--Initiate activity_log worker-- \n')
amqp_setup.channel.basic_consume(queue='aaron_queue', on_message_callback=callback, auto_ack=True)


print('\n--Start listening for messages....-- \n')
amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 


    
