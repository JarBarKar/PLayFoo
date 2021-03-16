from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json
import amqp_setup


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/message'
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

    def __init__(self, message_id, room_id, user_id, content):
        self.message_id = message_id
        self.room_id = room_id
        self.user_id = user_id
        self.content = content

    def json(self):
        return {"message_id":self.message_id, "room_id":self.room_id, "user_id":self.user_id, "content":self.content}

# function to create an exchange for a specific room's chat whenever a room is created
@app.route('/message/create/<int:room_id>', methods=['POST'])
def create_room_chat(room_id):
    # note: add error handling and HTTP response here later
    exchangename= str(room_id) + "_roomchat"
    amqp_setup.create_exchange(exchangename)
    print('exchange created')

# function to create a queue for a user in an exchange of the room chat they joined
@app.route('/message/join/<int:room_id>&<string:user_id>', methods=['POST'])
def join_room_chat(room_id, user_id):
    # note: add error handling and HTTP response here later
    exchangename= str(room_id) + "_roomchat"
    amqp_setup.create_queue(exchangename, user_id)
    print('queue_created')

# function to publish a sent message to the exchange
@app.route('/message/send/<int:room_id>&<string:user_id>&<string:content>', methods=['POST'])
def send_message(room_id, user_id, content):
    # note: add error handling and HTTP response here later
    exchangename = str(room_id) + "_roomchat"
    amqp_setup.channel.basic_publish(exchange=exchangename, body=content, properties=pika.BasicProperties(delivery_mode = 2))

if __name__ == "__main__":
    app.run(port=5003, debug=True)
    amqp_setup.check_setup() # to make sure connection and channel are running
