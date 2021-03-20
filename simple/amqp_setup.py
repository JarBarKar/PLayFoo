import pika

# These module-level variables are initialized whenever a new instance of python interpreter imports the module;
# In each instance of python interpreter (i.e., a program run), the same module is only imported once (guaranteed by the interpreter).

hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600, # these parameters to prolong the expiration time (in seconds) of the connection
))

channel = connection.channel()


def create_exchange(exchange_name, exchange_type):
    # Set up the exchange if the exchange doesn't exist
    # - use a 'fanout' exchange to enable interaction
    #exchange_type="fanout"
    return channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
        # 'durable' makes the exchange survive broker restarts

def create_queue(exchange_name, queue_name, routing_key):
    ############   Message queue   #############
    #delcare Message queue
    channel.queue_declare(queue=queue_name, durable=True)
        # 'durable' makes the queue survive broker restarts

    #bind Message queue
    return channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key) 
        # bind the queue to the exchange via the key

def send_message(exchange_name, routing_key, content):
    return channel.basic_publish(exchange=exchange_name, body=content, properties=pika.BasicProperties(delivery_mode = 2), routing_key=queue_name)

def receive_messages(queue_name, callback):
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    return channel.start_consuming()




"""
This function in this module sets up a connection and a channel to a local AMQP broker,
and declares a 'fanout' exchange to be used by the microservices in the solution.
"""
def check_setup():
    # The shared connection and channel created when the module is imported may be expired, 
    # timed out, disconnected by the broker or a client;
    # - re-establish the connection/channel is they have been closed
    global connection, channel, hostname, port

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    if channel.is_closed:
        channel = connection.channel()

def is_connection_open(connection):
    # For a BlockingConnection in AMQP clients,
    # when an exception happens when an action is performed,
    # it likely indicates a broken connection.
    # So, the code below actively calls a method in the 'connection' to check if an exception happens
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False