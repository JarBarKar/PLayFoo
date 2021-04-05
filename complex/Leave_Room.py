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

room_URL = environ.get('room_URL') or "http://localhost:5001/room"

@app.route('/leave', methods=['DELETE'])
def leave_room():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # we expect room_id & user_id to be in request
            request_info = request.get_json()
            print("\nReceived a leave request in JSON:", request_info)

            # do the actual work
            # 1. send room and user info
            result = processLeaveRoom(request_info)
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
                "message": "Leave_Room.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processLeaveRoom(request_info):
    # Invoke the room microservice
    print('\n-----Invoking room microservice-----')
    print(request_info,'juju')
    room_result = invoke_http(room_URL, method='DELETE', json=request_info)
    exchange_name = 'activity_error_exchange'
    print('leave_room_result:', room_result)

    #for activity_log routing key
    if room_result['code'] in range(200, 300):
        print('\n\n-----Invoking activity_log microservice for successfully leaving room-----')
        routing_key = 'info'
        code = 201
        message = 'Leave Room successful'
        try:
            amqp_setup.channel.basic_publish(exchange=exchange_name, body=json.dumps(room_result), properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
        except Exception as e:
            code=500
            message = "An error occurred while sending the message. " + str(e)

        print(f"\nOrder status {code} published to the RabbitMQ Exchange: {json.dumps(room_result)}")

    else:
        print('\n\n-----Invoking error microservice as room creation fails-----')
        routing_key = 'error'
        code = 500
        message = 'Leave Room failed'
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5102, debug=True)
    amqp_setup.check_setup()