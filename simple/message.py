from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json

import '../amqp_setup'


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/message'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    """
    creates Message table with the following attributes:
    message_id: int(6), primary key, auto increment
    user_id: varchar(12), foreign key
    content: varchar(150)
    """
    __tablename__ = 'message'

    message_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(12), nullable=False)
    content = db.Column(db.String(150), nullable=False)

    def __init__(self, message_id, user_id):
        self.message_id = message_id
        self.user_id = user_id
        self.content = content

    def json(self):
        return {"message_id":self.message_id, "user_id":self.user_id, "content":self.content}

@app.route('/message/<string:room_id>', methods=['POST'])
def create_room_chat(room_id):
    create_exchange(room_id)
    print('exchange created')

@app.route('/message/<string:user_id>', methods=['POST'])
