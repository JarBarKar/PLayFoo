from flask import Flask, request, jsonify
from flask_cors import CORS

import json
import amqp_setup

app = Flask(__name__)
CORS(app)

# function to create a queue for a user in an exchange of the room chat they joined
@app.route('/message/join/<int:room_id>&<string:user_id>', methods=['POST'])
def join_room_chat(room_id, user_id):
    exchange_name= str(room_id) + "_roomchat"
    queue_name = user_id + "_queue"
    try:
        amqp_setup.create_queue(exchange_name, queue_name)
        code = 200
        message = "Queue successfully created."
        amqp_setup.receive_messages(queue_name, callback)
    except Exception as e:
        code = 500
        message = "An error occurred while creating the queue. " + str(e)

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
        print("--DATA:", body)
    print()


if __name__ == "__main__":
    app.run(port=5004, debug=True)