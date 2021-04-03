from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import datetime as dt



app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/playfoo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    """
    creates Message table with the following attributes:
    message_id: int(6), primary key, auto increment
    room_id: int(6), foreign key
    user_id: varchar(12), foreign key
    content: varchar(150)
    """
    __tablename__ = 'message'

    message_id = db.Column(db.Integer(), primary_key=True)
    room_id = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.String(12), nullable=False)
    content = db.Column(db.String(150), nullable=False)
    timestamp= db.Column(db.DateTime, default=dt.datetime.now())

    def __init__(self, room_id, user_id, content):
        self.room_id = room_id
        self.user_id = user_id
        self.content = content

    def json(self):
        return {"room_id":self.room_id, "user_id":self.user_id, "content":self.content}


# function to publish a sent message to the exchange of the room chat
@app.route('/message/send', methods=['POST'])
def publish_message():
    data = request.get_json()
    try:
        print('--Sending Message--\n\n')
        code = 200
        message_push = Message(room_id=data['room_id'],user_id=data['user_id'],content=data['content'])
        db.session.add(message_push)
        db.session.commit()
        message = "Message successfully sent"
    except Exception as e:
        code = 500
        message = "An error occurred while sending the message. " + str(e)

    return jsonify(
        {
            "code": code,
            "data": json.dumps(data),
            "message": message
        }
    ), code


if __name__ == "__main__":
    app.run(port=5007, debug=True)
    amqp_setup.check_setup() # to make sure connection and channel are running
