from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from invokes import invoke_http
import pika

import json

app = Flask(__name__)
CORS(app)

user_url = "http://localhost:5000/user"
room_url = "http://localhost:5001/room"
game_url = "http://localhost:5002/game"
message_url = "http://localhost:5003/message"

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
    # 2. Send the room and user info
    # Invoke the room microservice
    print('\n-----Invoking room microservice-----')
    room_result = invoke_http(room_url, method='DELETE', json=request_info)
    print('leave_room_result:', room_result)

    # Check the order result; if a failure, send it to the error microservice.
    code = room_result["code"]
    message = json.dumps(room_result)

    # if code not in range(200, 300):
    #     # Inform the error microservice
    #     #print('\n\n-----Invoking error microservice as order fails-----')
    #     # print('\n\n-----Publishing the (room error) message with routing_key=room.error-----')

    #     # invoke_http(error_URL, method="POST", json=order_result)
    #     # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="room.error", 
    #     #     body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    #     # make message persistent within the matching queues until it is received by some receiver 
    #     # (the matching queues have to exist and be durable and bound to the exchange)

    #     # - reply from the invocation is not used;
    #     # continue even if this invocation fails        
    #     print("\Room status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), room_result)

    #     # 7. Return error
    #     return {
    #         "code": 500,
    #         "data": {"room_result": room_result},
    #         "message": "Order creation failure sent for error handling."
    #     }

    # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # In http version, we first invoked "Activity Log" and then checked for error.
    # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # and a message sent to “Error” queue can be received by “Activity Log” too.

    # else:
    #     # 4. Record new order
    #     # record the activity log anyway
    #     # print('\n\n-----Invoking activity_log microservice-----')
    #     print('\n\n-----Publishing the (room info) message with routing_key=room.info-----')        

    #     # invoke_http(activity_log_URL, method="POST", json=room_result)            
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="room.info", 
    #         body=message)
    
    # print("\nRoom status published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails
    
    # 5. Send new room chat info to message
    # Invoke the message microservice

    print('\n\n-----Invoking message microservice-----')    
    
    room_result_data = room_result['data']
    message_result = invoke_http(
        message_url, method="DELETE", json=room_result_data)
    print("message_result:", message_result, '\n')

    # Check the shipping result;
    # if a failure, send it to the error microservice.
    code = message_result["code"]
    # if code not in range(200, 300):
    #     # Inform the error microservice
    #     #print('\n\n-----Invoking error microservice as message fails-----')
    #     # print('\n\n-----Publishing the (message error) message with routing_key=message.error-----')

    #     # invoke_http(error_URL, method="POST", json=message_result)
    #     message = json.dumps(message_result)
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="message.error", 
    #         body=message, properties=pika.BasicProperties(delivery_mode = 2))

    #     print("\nMessage status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), message_result)

    #     # 7. Return error
    #     return {
    #         "code": 400,
    #         "data": {
    #             "room_result": room_result,
    #             "message_result": message_result
    #         },
    #         "message": "Message error sent for error handling."
    #     }

    # 7. Return created room, message
    return {
        "code": 201,
        "data": {
            "room_result": room_result,
            "message_result": message_result
        }
    }

if __name__ == "__main__":
    app.run(port=5102, debug=True)