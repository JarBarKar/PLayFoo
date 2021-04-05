import sys
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import amqp_setup
import pika
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# function to publish a sent message to the exchange of the room chat
@app.route('/send_message', methods=['POST'])
def publish_message():
    request_info = request.get_json()
    exchange_name = "roomchat"
    routing_key = "message"
    try:
        user_id = request_info['user_id']
        room_id = request_info['room_id']
        content = request_info['content']
        amqp_setup.channel.basic_publish(exchange=exchange_name, body=json.dumps(request_info), properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
        code = 200
        message = "Message sent."
    except Exception as e:
        code = 500
        message = "An error occurred while sending the message. " + str(e)

    if code in range(200, 300):
        print('\n\n-----Invoking activity_log microservice as message sent successful-----')
        exchange_name = 'activity_error_exchange'
        routing_key = 'info'
        code = 201
        message = 'Message sent successfully'
        message_result = {
            "code": code,
            "message": message,
            "data" : request_info
        }
        try:
            amqp_setup.channel.basic_publish(exchange=exchange_name, body=json.dumps(message_result), properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
        except Exception as e:
            code=500
            message = "An error occurred while sending the message. " + str(e)

        print(f"\nOrder status {code} published to the RabbitMQ Exchange: {json.dumps(message_result)}")

    #for error_log routing key
    else:
        print('\n\n-----Invoking error microservice as message fails to send-----')
        exchange_name = 'activity_error_exchange'
        routing_key = 'error'
        code = 500
        message = 'Message sent failed'
        message_result = {
            "code": code,
            "message": message,
            "data" : request_info
        }
        try:
            amqp_setup.channel.basic_publish(exchange=exchange_name, body=json.dumps(message_result), properties=pika.BasicProperties(delivery_mode = 2), routing_key=routing_key)
            code = 500
        except Exception as e:
            code=500
            message = "An error occurred while sending the message. " + str(e)

        print(message)
        print(f"\nOrder status {code} published to the RabbitMQ Exchange: {json.dumps(message_result)}")

    return jsonify(
        {
            "code": code,
            "data": {
                "exchange_name": exchange_name,
                "routing_key": routing_key,
                "content": request_info
            },
            "message": message
        }
    ), code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5103, debug=True)
    amqp_setup.check_setup() # to make sure connection and channel are running
