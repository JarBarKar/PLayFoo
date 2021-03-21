from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json
import amqp_setup
import pika

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
    exchange_type= "fanout"
    try:
        amqp_setup.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
        code = 200
        message = "Exchange successfully created."
    except Exception as e:
        code = 500
        message = "An error occurred while creating the exchange. " + str(e)

    return jsonify(
        {
            "code": code,
            "data": {
                "exchange_name": exchange_name,
            },
            "message": message
        }
    ), code

# function to create a queue for a user in an exchange of the room chat they joined
@app.route('/message/join', methods=['POST'])
def join_room_chat():
    request_info = request.get_json()

    user_id = request_info['user_id']
    room_id = request_info['room_id']
    
    exchange_name= str(room_id) + "_roomchat"
    queue_name = user_id + "_queue"
    routing_key = str(room_id) + "." + user_id
    try:
        amqp_setup.channel.queue_declare(queue=queue_name, durable=True)
        amqp_setup.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
        code = 200
        message = "Queue successfully created."

    except Exception as e:
        code = 500
        message = "An error occurred while creating the queue. " + str(e)

    return jsonify(
        {
            "code": code,
            "data": {
                "exchange_name": exchange_name,
                "queue_name": queue_name,
                "routing_key": routing_key
            },
            "message": message
        }
    ), code

# defines what to do when receiving a message
def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a message from " + __file__)
    processMessage(json.loads(body))
    print() # print a new line feed

# defines how exactly to process received message
def processMessage(body):
    print("Printing the message:")
    try:
        message_body = json.loads(body)
        print("--JSON:", message_body)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", body)
    print()

# function to publish a sent message to the exchange of the room chat
@app.route('/message/send/<int:room_id>&<string:user_id>', methods=['POST'])
def publish_message(room_id, user_id):
    # NOTE: currently we are treating queue_name as the routing key (see amqp_setup), might want to modify later
    exchange_name = str(room_id) + "_roomchat"
    routing_key = str(room_id) + ".*"
    content = json.dumps(request.get_json())
    try:
        amqp_setup.channel.basic_publish(exchange=exchange_name, body=content, properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
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
                "routing_key": routing_key,
                "content": content
            },
            "message": message
        }
    ), code

# function to close queue of user when leaving room chat
@app.route('/message', methods=['DELETE'])
def leave_room_chat():

    request_info = request.get_json()

    user_id = request_info['user_id']
    room_info = request_info['room_info']
    room_id = room_info['room_id']
    is_host = request_info['is_host']

    exchange_name= str(room_id) + "_roomchat"

    if is_host: # user is the host, we need to remove everyone from the room by deleting their queues
        member_ids = request_info['member_ids']
        try:
            for member_id in member_ids:
                queue_name = member_id + "_queue"
                amqp_setup.channel.queue_delete(queue=queue_name)
            amqp_setup.channel.exchange_delete(exchange=exchange_name)
            code = 200
            message = "Queues and exchange successfully deleted."
        except Exception as e:
            code = 500
            message = "An error occurred while deleting the queue. " + str(e)
    else: # user is not the host, only have to delete user's queue
        try:
            queue_name = user_id + "_queue"
            amqp_setup.channel.queue_delete(queue=queue_name)
            code = 200
            message = "Queue successfully deleted."

        except Exception as e:
            code = 500
            message = "An error occurred while deleting the queue. " + str(e)


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

if __name__ == "__main__":
    app.run(port=5003, debug=True)
    amqp_setup.check_setup() # to make sure connection and channel are running
