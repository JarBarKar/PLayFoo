import json
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import amqp_setup

monitorBindingKey='#'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/activity_log'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Activity_Log(db.Model):
    __tablename__ = 'activity_log'
    activity_id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(128), nullable=False)
    code = db.Column(db.Integer(), nullable=False)
    timestamp= db.Column(db.DateTime, server_default=db.func.now())

    

    def __init__(self, activity_id, description, code, timestamp):
        self.activity_id = activity_id
        self.description = description
        self.code = code
        self.timestamp = timestamp


    def json(self):
        return {"activity_id": self.activity_id, "description": self.description, "code": self.code, "timestamp": self.timestamp}


@app.route("/activity_log", methods=['POST'])
def activity_log_receive():
    exchange_name= "activity_log_exchange"
    queue_name = "activity_log_queue"
    try:
        amqp_setup.create_queue(exchange_name, queue_name)
        code = 200
        message = "Queue successfully created."
        t = Thread(target=amqp_setup.receive_messages, args=(queue_name, callback))
        t.start()
    except Exception as e:
        code = 500
        message = "An error occurred while creating the queue. " + str(e)

    return jsonify(
        {
            "code": code,
            "data": {
                "exchange_name": exchange_name,
                "queue_name": queue_name
            },
            "message": message
        }
    ), code

# defines what to do when receiving message
def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a message from " + __file__)
    processMessage(body)
    print() # print a new line feed

# defines how exactly to process received message
def processMessage(body):
    print("Printing the message:")
    try:
        #Store in DB first, then convert to JSON string and print it out
        activity_log = Activity_Log(body)
        db.session.add(activity_log)
        db.session.commit()
        message_body = json.loads(body)
        print("--JSON:", message_body)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", body)
    print()
# def receiveOrderLog():
#     amqp_setup.check_setup()
#     queue_name = 'Activity_Log'
#     # set up a consumer and start to wait for coming messages
#     amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
#     amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
#     #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

# def callback(channel, method, properties, body): # required signature for the callback; no return
#     print("\nReceived an order log by " + __file__)
#     processOrderLog(json.loads(body))
#     print() # print a new line feed

# def processOrderLog(order):
#     print("Recording an order log:")
#     print(order)
#     try:
#         db.session.add(member)
#         db.session.commit()
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "user_id": member.user_id,
#                     "room": member.room_id
#                     },
#                 "message": "An error occurred joining the room."
#             }
#         ), 500



if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    app.run(port=5005, debug=True)
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    
