from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from invokes import invoke_http

import amqp_setup
import pika
import json
from os import environ

app = Flask(__name__)
CORS(app)

room_URL = environ.get('room_URL')


#Create Room (must send via JSON REQUEST)

#{"room_id": room_id, "room_name": room_name, "capacity": capacity,
#  "game_id":game_id, "host_id": host_id}

@app.route("/create_room", methods=['POST'])
def create_room():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            request_info = request.get_json()
            print("\nReceived room details in JSON:", request_info)
            # do the actual work
            # 1. Send room info
            result = processCreateRoom(request_info)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "Create_Room.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify(
        {
            "code": 400,
            "message": "Invalid JSON input: " + str(request.get_data())
        }
    ), 400

def processCreateRoom(request_info):
    # 2. POST a request to create a room.
    print('\n-----Sending request to room.py to create room-----')
    room_result = invoke_http(room_URL, method='POST', json=request_info)
    exchange_name = 'activity_error_exchange'
    print('create_room_result:', room_result)

    #for activity_log routing key
    if room_result['code'] in range(200, 300):
        print('\n\n-----Invoking activity_log microservice as room creation successful-----')
        routing_key = 'info'
        code = 201
        message = 'Room creation successful'
        try:
            amqp_setup.channel.basic_publish(exchange=exchange_name, body=json.dumps(room_result), properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
        except Exception as e:
            code=500
            message = "An error occurred while sending the message. " + str(e)

        print(f"\nOrder status {code} published to the RabbitMQ Exchange: {json.dumps(room_result)}")

    #for error_log routing key
    else:
        print('\n\n-----Invoking error microservice as room creation fails-----')
        routing_key = 'error'
        code = 500
        message = 'Room creation failed'
        try:
            amqp_setup.channel.basic_publish(exchange=exchange_name, body=json.dumps(room_result), properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
            code = 500
        except Exception as e:
            code=500
            message = "An error occurred while sending the message. " + str(e)

        print(message)
        print(f"\nOrder status {code} published to the RabbitMQ Exchange: {json.dumps(room_result)}")


    return {
        "code": code,
        "data": {
            "room_result": room_result
        },
        "message": message
    }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5100, debug=True)
    amqp_setup.check_setup() # to make sure connection and channel are running

    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
