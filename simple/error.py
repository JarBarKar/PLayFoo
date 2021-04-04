import json
import os
import amqp_setup
from sqlalchemy import Table, Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

import datetime as dt

Base = declarative_base()

# engine = create_engine('mysql+mysqlconnector://root@localhost:3306/error')
engine = create_engine(environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/error')

Session = sessionmaker(bind=engine)
session = Session()

class Error(Base):
    __tablename__ = 'Error'
    error_id = Column(Integer(), primary_key=True)
    code = Column(Integer(), nullable=False)
    data = Column(String(1000), nullable=False)
    message = Column(String(128), nullable=False)
    timestamp= Column(DateTime, default=dt.datetime.now())

    def __init__(self, code, data, message):
        self.code = code
        self.data = data
        self.message = message

    def json(self):
        return {"activity_id": self.activity_id, "code": self.code, "data": self.data, "message": self.message, "timestamp": self.timestamp}



def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log by " + __file__)
    processErrorLog(body)
    print() # print a new line feed

def processErrorLog(data):
    print(json.loads(data)['code'])
    data = json.loads(data.decode('UTF-8'))
    #check if send to activity or error depending on code
    log = Error(code=data['code'],data=json.dumps(data['data']),message=data['message'])


    session.add(log)
    session.commit()
    print("Recording an error log:")
    print(log.json())


#Setting up activity_log and error exchange
print('\n --Setting up exchange-- \n')
amqp_setup.channel.exchange_declare(exchange='activity_error_exchange', exchange_type='topic', durable=True)

#Setting up error queue
print('--Setting up error queue-- \n')
amqp_setup.channel.queue_declare(queue='error_queue', durable=True)
amqp_setup.channel.queue_bind(exchange='activity_error_exchange', queue='error_queue', routing_key='error')

print('--Initiate error worker-- \n')
amqp_setup.channel.basic_consume(queue='error_queue', on_message_callback=callback, auto_ack=True)

print('\n--Start listening for messages....-- \n')
amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 




    
