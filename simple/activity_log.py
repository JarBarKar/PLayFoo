import json
import os
import amqp_setup
from sqlalchemy import Table, Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

import datetime as dt

Base = declarative_base()

# engine = create_engine('mysql+mysqlconnector://root@localhost:3306/activity_log')
engine = create_engine(environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/activity_log')

Session = sessionmaker(bind=engine)
session = Session()

class Activity_Log(Base):
    __tablename__ = 'activity_log'
    activity_id = Column(Integer(), primary_key=True)
    code = Column(Integer(), nullable=False)
    data = Column(String(1000), nullable=False)
    message = Column(String(128), nullable=False)
    timestamp= Column(DateTime, default=dt.datetime.now())

    def __init__(self, code, data, message):
        self.code = code
        self.data = data
        self.message = message

    def json(self):
        return {"activity_id": self.activity_id, "data": self.data, "code": self.code, "timestamp": self.timestamp}


# @app.route("/activity_log", methods=['POST'])
# def activity_log_receive():
#     exchange_name = 'activity_log_exchange'
#     queue_name = 'activity_log_queue'
#     routing_key = '#'
#     #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
#     amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
#     amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log file by " + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed



def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log by " + __file__)
    processOrderLog(body)
    print() # print a new line feed

def processOrderLog(data):
    data = json.loads(data.decode('UTF-8'))
    #check if send to activity or error depending on code
    log = Activity_Log(code=data['code'],data=json.dumps(data['data']),message=data['message'])

    session.add(log)
    session.commit()
    print("Recording an activity log:")
    print(log.json())



#Setting up activity_log and error exchange
print('\n --Setting up exchange-- \n')
amqp_setup.channel.exchange_declare(exchange='activity_error_exchange', exchange_type='topic', durable=True)

print('--Setting up activity_log queue-- \n')
amqp_setup.channel.queue_declare(queue='activity_log_queue', durable=True)
amqp_setup.channel.queue_bind(exchange='activity_error_exchange', queue='activity_log_queue', routing_key='info')

print('--Initiate activity_log worker-- \n')
amqp_setup.channel.basic_consume(queue='activity_log_queue', on_message_callback=callback, auto_ack=True)


print('\n--Start listening for messages....-- \n')
amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 


    
