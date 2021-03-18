from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/room'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer(), primary_key=True)
    room_name = db.Column(db.String(64), nullable=False)
    game_id= db.Column(db.Integer(), nullable=False)
    capacity = db.Column(db.Integer(), nullable=False)
    host_id = db.Column(db.String(12), nullable=False)
    

    def __init__(self, room_id, room_name, game_id, capacity, host_id):
        self.room_id = room_id
        self.room_name = room_name
        self.game_id = game_id
        self.capacity = capacity
        self.host_id = host_id

    def json(self):
        return {"room_id": self.room_id, "room_name": self.room_name, "capacity": self.capacity, "game_id":self.game_id, "host_id": self.host_id}


class Member(db.Model):
    __tablename__ = 'member'
    user_id = db.Column(db.String(100), primary_key=True)
    room_id = db.Column(db.Integer(), primary_key=True)


    def __init__(self, user_id, room_id):
        self.user_id = user_id
        self.room_id = room_id


    def json(self):
        return {"user_id": self.user_id, "room_id": self.room_id}


#Get room based on game_id
@app.route("/room/<string:game_id>")
def get_room(game_id):
    roomlist = Room.query.filter_by(game_id=game_id)
    if roomlist:
        return jsonify(
            {
                "code": 200,
                "data": [room.json() for room in roomlist]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no rooms."
        }
    ), 404

#Create Room
@app.route("/room", methods=['POST'])
def create_room():
    data = request.get_json()
    room = Room(**data)
    member = Member(room.host_id,room.room_id)
    try:
        db.session.add(room)
        db.session.add(member)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "room": room
                },
                "message": "An error occurred creating the room."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": room.json()
        }
    ), 201

#Join Room
@app.route("/room/<string:room_id>", methods=['POST'])
def join_room(room_id):
    selected_room = Room.query.filter_by(room_id=room_id).first()
    no_of_members = Member.query.filter_by(room_id=room_id).count()
    if no_of_members==selected_room.capacity:
        return jsonify(
            {
                "code" : 500,
                "message" : "Room is full"
            }
        )
    #Get user id via request
    else:
        data = request.get_json()
        member = Member(**data)

    try:
        db.session.add(member)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "user_id": member.user_id,
                    "room": member.room_id
                    },
                "message": "An error occurred joining the room."
            }
        ), 500

    #did not return valid response but code is loaded in DB
    return jsonify(
        {
            "code": 201,
            "data": member.json()
        }
    ), 201


#Leave Room
@app.route("/room/<string:user_id>&<string:room_id>", methods=['DELETE'])
def leave_room(user_id,room_id):
    selected_room = Room.query.filter_by(room_id=room_id).first()
    try:
        deleted_user = Member.query.filter_by(user_id=user_id).first()
        db.session.delete(deleted_user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "room": selected_room.json()
                    },
                "message": "An error occurred leaving the room. Please try again."
            }
        ), 500
    return jsonify(
    {
        "code": 204,
        "data": selected_room.json(),
        "message": "Successfully leave room"
        }
    ), 201


if __name__ == '__main__':
    app.run(port=5001, debug=True)
