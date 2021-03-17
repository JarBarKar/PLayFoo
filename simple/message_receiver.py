from flask import Flask, request, jsonify
from flask_cors import CORS

import json
import amqp_setup

app = Flask(__name__)
CORS(app)

# function to start consuming messages to exchange
def receive_messages():
    # NOTE: currently we are treating queue_name as the routing key (see amqp_setup), might want to modify later
    print('started receiving')
    amqp_setup.channel.start_consuming()
    print('stopped receiving')

if __name__ == "__main__":
    receive_messages()