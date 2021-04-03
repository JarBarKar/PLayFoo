from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from invokes import invoke_http
import pika

import json

app = Flask(__name__)
CORS(app)

# user_URL = "http://localhost:5000/user"
room_URL = "http://localhost:5001/room"
# game_URL = "http://localhost:5002/game"
message_URL = "http://localhost:5003/message"

@app.route('/send', methods=['POST'])
def send_message():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # we expect room_id & user_id to be in request
            request_info = request.get_json()
            print("\nReceived a send message request in JSON:", request_info)

            # do the actual work
            # 1. send room and user info
            result = processSendMessage(request_info)
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
                "message": "Send_Message.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processSendMessage(request_info):
    # 2. Send the room and user info
    # Invoke the room microservice
    # print('\n-----Invoking room microservice-----')
    # room_id = request_info['room_id']
    # room_result = invoke_http(room_URL + '/' + str(room_id), method='POST', json=request_info)
    # print('join_room_result:', room_result)

    #Setting up activity_log and error exchange
    # print('\n --Setting up exchange-- \n')
    # amqp_setup.channel.exchange_declare(exchange='activity_error_exchange', exchange_type='topic', durable=True)

    #for activity_log routing key
    # if room_result['code'] in range(200, 300):
    #     print('\n\n-----Invoking activity_log microservice as successfully joined room-----')
    #     routing_key = 'info'
    #     code = 201
    #     message = 'Room successfully joined'
    #     try:
    #         amqp_setup.channel.basic_publish(exchange=exchange_name, body=json.dumps(room_result), properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
    #     except Exception as e:
    #         code=500
    #         message = "An error occurred while sending the message. " + str(e)

    #     print(f"\nOrder status {code} published to the RabbitMQ Exchange: {json.dumps(room_result)}")

    #for error_log routing key
    # else:
    #     print('\n\n-----Invoking error microservice as failed to join room-----')
    #     routing_key = 'error'
    #     code = 500
    #     message = 'Failed to join room'
    #     try:
    #         amqp_setup.channel.basic_publish(exchange=exchange_name, body=json.dumps(room_result), properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
    #         code = 500
    #     except Exception as e:
    #         code=500
    #         message = "An error occurred while sending the message. " + str(e)

    #     print(message)
    #     print(f"\nOrder status {code} published to the RabbitMQ Exchange: {json.dumps(room_result)}")

    print('\n\n-----Invoking message microservice-----')    
    
    message_result = invoke_http(
        message_URL + "/send", method="POST", json=request_info)
    print("message_result:", message_result, '\n')

    return {
        "code": 201,
        "data": {
            "message_result": message_result
        }
    }

if __name__ == "__main__":
    app.run(port=5103, debug=True)