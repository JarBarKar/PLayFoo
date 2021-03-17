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
    exchange_name= str(room_id) + "_roomchat"

    try:
        amqp_setup.create_exchange(exchange_name)
        code = 200
        message = "Exchange successfully created."
    except Exception as e:
        code = 500
        message = "An error occurred while creating the exchange. " + str(e)

    return jsonify(
        {
            "code": code,
            "data": {
                "exchange_name": exchange_name
            },
            "message": message
        }
    ), code


# function to create a queue for a user in an exchange of the room chat they joined
@app.route('/message/join/<int:room_id>&<string:user_id>', methods=['POST'])
def join_room_chat(room_id, user_id):
    exchange_name= str(room_id) + "_roomchat"
    queue_name = user_id + "_queue"
    try:
        amqp_setup.create_queue(exchange_name, queue_name)
        amqp_setup.receive_messages(queue_name, callback)
        code = 200
        message = "Queue and consumer successfully created."
    except Exception as e:
        code = 500
        message = "An error occurred while creating the queue and consumer. " + str(e)

    return jsonify(
        {
            "code": code,
            "data": {
                "exchange_name": exchange_name,
                "queue_name": queue_name
            },
            "message": message
        }
    ), code

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a message from " + __file__)
    processMessage(body)
    print() # print a new line feed

def processMessage(body):
    print("Printing the message:")
    try:
        message_body = json.loads(body)
        print("--JSON:", message_body)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", message_body)
    print()


# function to publish a sent message to the exchange
@app.route('/message/send/<int:room_id>&<string:user_id>&<string:content>', methods=['POST'])
def send_message(room_id, user_id, content):
    # NOTE: currently we are treating queue_name as the routing key (see amqp_setup), might want to modify later
    exchange_name = str(room_id) + "_roomchat"
    queue_name = user_id + "_queue"
    try:
        amqp_setup.send_message(exchange_name, queue_name, content)
        code = 200
        message = "Message successfully sent."
    except Exception as e:
        code = 500
        message = "An error occurred while sending the message. " + str(e)

    return jsonify(
        {
            "code": code,
            "data": {
                "exchange_name": exchange_name,
                "queue_name": queue_name,
                "content": content
            },
            "message": message
        }
    ), code



if __name__ == "__main__":
    app.run(port=5003, debug=True)
    amqp_setup.check_setup() # to make sure connection and channel are running
