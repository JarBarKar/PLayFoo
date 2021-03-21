import requests
import amqp_setup
from message import callback, processMessage

room_id = int(input("room_id: "))
user_id = input("user_id: ")

# y if creating room, n if just joining room
create_room = input("create_room? [y/n]:")
while create_room not in ["y", "n"]:
    print("Error: enter either 'y' or 'n'.")
    create_room = input("create_room? [y/n]:")

# request to join room chat
def post_request(url, *args):
    
    count = 0
    for arg in args:
        if count == 0:
            url += str(arg)
        else:
            url += "&" + str(arg)
        count += 1

    r = requests.post(url)

    response = r.json()
    
    return response

if create_room == 'y':
    create_response = post_request('http://localhost:5003/message/create/', room_id)
    print(create_response)
    
join_response = post_request('http://localhost:5003/message/join/', room_id, user_id)
print(join_response)

queue_name = join_response['data']['queue_name']

# client runs a loop to listen for chat messages
amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
amqp_setup.channel.start_consuming()

# think of a way to stop this

