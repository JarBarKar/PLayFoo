from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json
import amqp_setup
from os import environ

import datetime as dt

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/message'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
@app.route('/message/listen')
def listen_room():
    data = request.get_json()
    room_id = data['room_id']
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
    app.run(host='0.0.0.0', port=5003, debug=True)