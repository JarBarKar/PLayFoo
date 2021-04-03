from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
sys.path.insert(0, '../simple')
import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

#user_URL = "http://localhost:5000/user"
room_URL = "http://localhost:5001/room"
# game_URL = "http://localhost:5002/game"
message_URL = "http://localhost:5003/message"
activity_log_URL = "http://localhost:5004/activity_log"


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


def processCreateRoom(room):
    # 2. Setting up amqp between publisher and subscriber for create_room and activity_log
    print('\n-----Sending request to room.py to create room-----')
    room_result = invoke_http(room_URL, method='POST', json=room)

    # 3. Setting up amqp between publisher and subscriber for create_room and activity_log
    # print('\n-----Setting up subscriber queue for activity_log microservice-----')
    # room_result = invoke_http(activity_log_URL, method='POST')

    print('\n-----Setting up exchange broker to publish messages-----')
    exchange_name = 'activity_log_exchange'
    queue_name = 'activity_log_queue'
    routing_key = '#'

    amqp_setup.create_exchange(exchange_name=exchange_name, exchange_type='topic')
    amqp_setup.send_message(exchange_name=exchange_name, routing_key=routing_key, content=room)

    print('room_result:', room_result)

    try:
        amqp_setup.channel.exchange_declare(exchange_name=exchange_name, exchange_type='topic', durable=True)
        amqp_setup.channel.basic_publish(exchange=exchange_name, body=content, properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
        code = 200
    except Exception as e:
        code=500
        message = "An error occurred while sending the message. " + str(e)

    return 
    {
        "code": 201,
        "data": 
            {
                "room_result": room_result
            },
        "message": "Room creation successful."
    }
  

    # # Check the result; if a failure, send it to the error microservice.
    # code = room_result["code"]
    # message = json.dumps(room_result)

    # if code not in range(200, 300):
    #     # Inform the error microservice
    #     #print('\n\n-----Invoking error microservice as order fails-----')
    #     print('\n\n-----Publishing the (order error) message with routing_key=room.error-----')

    #     # invoke_http(error_URL, method="POST", json=order_result)
    #     amqp_setup.basic_publish(exchange=amqp_setup.exchangename, routing_key="room.error", 
    #         body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    #     # make message persistent within the matching queues until it is received by some receiver 
    #     # (the matching queues have to exist and be durable and bound to the exchange)

    #     # - reply from the invocation is not used;
    #     # continue even if this invocation fails        
    #     print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), room_result)

    #     # Return error when room creation failed
    #     return {
    #         "code": 500,
    #         "data": {"room_result": room_result},
    #         "message": "Room creation failed."
    #     }

    # # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # # In http version, we first invoked "Activity Log" and then checked for error.
    # # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # # and a message sent to “Error” queue can be received by “Activity Log” too.

    # else:
    #     # 4. Record new order
    #     # record the activity log anyway
    #     #print('\n\n-----Invoking activity_log microservice-----')
    #     print('\n\n-----Publishing the (room info) message with routing_key=room.info-----')        

    #     # invoke_http(activity_log_URL, method="POST", json=order_result)            
    #     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="room.info", 
    #         body=message)

def processCreateRoom(request_info):
    # 2. POST a request to create a room.
    print('\n-----Sending request to room.py to create room-----')
    room_result = invoke_http(room_URL, method='POST', json=request_info)
    exchange_name = 'activity_error_exchange'
    print('create_room_result:', room_result)

    #Setting up activity_log and error exchange
    print('\n --Setting up exchange-- \n')
    amqp_setup.channel.exchange_declare(exchange='activity_error_exchange', exchange_type='topic', durable=True)

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


    
    room_result_data = room_result['data']
    message_result = invoke_http(
        message_URL + "/create", method="POST", json=room_result_data)
    print("message_result:", message_result, '\n')


    # return {
    #     "code": 201,
    #     "data": {
    #         "room_result": room_result,
    #         "message_result": message_result
    #     }
    # }

    # print('\n\n-----Sending request to message.py to create exchange and queue-----')    
    
    # room_result_data = room_result['data']
    # message_result = invoke_http(
    #     message_URL + "/create", method="POST", json=room_result_data)
    # print("message_result:", message_result, '\n')

    # return {
    #     "code": 201,
    #     "data": {
    #         "room_result": room_result,
    #         "message_result": message_result
    #     }
    # }




# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for creating a room...")
    app.run(port=5100, debug=True)
    amqp_setup.check_setup() # to make sure connection and channel are running

    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
