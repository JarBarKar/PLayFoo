import json
from invokes import invoke_http
import amqp_setup
from message import callback, processMessage

from threading import Thread

room_id = int(input("room_id: "))
user_id = input("user_id: ")

# y if creating room, n if just joining room
create_room = input("create_room? [y/n]:")
while create_room not in ["y", "n"]:
    print("Error: enter either 'y' or 'n'.")
    create_room = input("create_room? [y/n]:")

json_data = json.dumps(
    {
    "room_id": room_id,
    "user_id": user_id
    }
)
json_data = json.loads(json_data)
print(json_data)
print(type(json_data))

if create_room == 'y':
    create_response = invoke_http('http://localhost:5003/message/create/' + str(room_id), method="POST")
    print(create_response)
    
print('did this')
join_response = invoke_http('http://localhost:5003/message/join', method='POST', json=json_data)
print(join_response)

queue_name = join_response['data']['queue_name']

def go_consume():
    print('ok start liao')
    amqp_setup.channel.start_consuming()
    print('ok stop liao')

# client runs a loop to listen for chat messages
consumer_tag = amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
x = Thread(target=go_consume)
x.start()

stop = input('stop [y/n]')
while stop != 'y':
    stop = input('stop [y/n]')

amqp_setup.channel.basic_cancel(consumer_tag)
# think of a way to stop this

