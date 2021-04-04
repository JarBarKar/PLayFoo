from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json
import amqp_setup
from sqlalchemy import Table, Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

import datetime as dt

app = Flask(__name__)
CORS(app)

# engine = create_engine('mysql+mysqlconnector://root@localhost:3306/message')
engine = create_engine(environ.get('dbURL'))

db = SQLAlchemy(app)

class Message(db.Model):
    """
    creates Message table with the following attributes:
    message_id: int(6), primary key, auto increment
    room_id: int(6), foreign key
    user_id: varchar(12), foreign key
    content: varchar(150)
    """
    __tablename__ = 'message'

    message_id = db.Column(db.Integer(), primary_key=True)
    room_id = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.String(12), nullable=False)
    content = db.Column(db.String(150), nullable=False)
    timestamp= db.Column(db.DateTime, default=dt.datetime.now())

    def __init__(self, message_id, room_id, user_id, content, timestamp):
        self.message_id = message_id
        self.room_id = room_id
        self.user_id = user_id
        self.content = content
        self.timestamp = timestamp


    def json(self):
        return {"message_id":self.message_id, "room_id":self.room_id, "user_id":self.user_id, "content":self.content, "timestamp":self.timestamp}

# keep pinging for new messages (room_id)
@app.route('/message/listen/<string:room_id>')
def listen_room(room_id):
    messagelist = Message.query.filter_by(room_id=room_id)
    if messagelist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    'messages': [message.json() for message in messagelist]
                }
            }
        ), 200

if __name__ == "__main__":
    app.run(port=5003, debug=True)