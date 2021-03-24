import amqp_setup
import json
import pika

info = {
    "code": 201,
    "data": "testing nia",
    "message": "testing message nia"
}

json_data = json.dumps(info)
print(json_data)
print(type(json_data))

amqp_setup.channel.basic_publish(exchange='activity_error_exchange', body=json_data,
    properties=pika.BasicProperties(delivery_mode = 2), routing_key="info")

