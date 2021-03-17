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
    timestamp= db.Column(db.DateTime, server_default=db.func.now())

    

    def __init__(self, activity_id, description, timestamp):
        self.activity_id = activity_id
        self.description = description
        self.timestamp = timestamp


    def json(self):
        return {"activity_id": self.activity_id, "description": self.description, "timestamp": self.timestamp}


@app.route("/activity_log", methods=['POST'])

def receiveOrderLog():
    amqp_setup.check_setup()
    queue_name = 'Activity_Log'    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(order):
    print("Recording an order log:")
    print(order)


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
