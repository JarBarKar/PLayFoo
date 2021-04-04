import json
import os
import amqp_setup
from sqlalchemy import Table, Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime as dt
from os import environ

Base = declarative_base()

engine = create_engine(environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/message')

Session = sessionmaker(bind=engine)
session = Session()

class Message(Base):
    __tablename__ = 'message'
    message_id = Column(Integer(), primary_key=True)
    room_id = Column(Integer(), nullable=False)
    user_id = Column(String(12), nullable=False)
    content = Column(String(150), nullable=False)
    timestamp= Column(DateTime, default=dt.datetime.now())

    def __init__(self, room_id, user_id, content):
        self.room_id = room_id
        self.user_id = user_id
        self.content = content

    def json(self):
        return {"message_id":self.message_id, "room_id":self.room_id, "user_id":self.user_id, "content":self.content, "timestamp":self.timestamp}


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a log by " + __file__)
    processOrderLog(body)
    print() # print a new line feed

def processOrderLog(data):
    data = json.loads(data.decode('UTF-8'))
    log = Message(room_id=data['room_id'],user_id=data['user_id'],content=data['content'])
    session.add(log)
    session.commit()
    print("Recording an message sent:")
    print(log.json())


print('--Setting up exchange-- \n')
amqp_setup.channel.exchange_declare(exchange='roomchat', exchange_type='fanout', durable=True)

print('--Setting up message queue-- \n')
amqp_setup.channel.queue_declare(queue='message_queue', durable=True)
amqp_setup.channel.queue_bind(exchange='roomchat', queue='message_queue', routing_key='message')

print('--Initiate message worker-- \n')
amqp_setup.channel.basic_consume(queue='message_queue', on_message_callback=callback, auto_ack=True)


print('\n--Start listening for messages....-- \n')
amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 


    
