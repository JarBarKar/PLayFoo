from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/room'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer(), primary_key=True)
    room_name = db.Column(db.String(64), nullable=False)
    game_id= db.Column(db.Integer(), nullable=False)
    capacity = db.Column(db.Integer(), nullable=False)
    host_id = db.Column(db.String(12), nullable=False)


    def __init__(self, room_name, game_id, capacity, host_id):
        self.room_name = room_name
        self.game_id = game_id
        self.capacity = capacity
        self.host_id = host_id

    def json(self):
        return {"room_id": self.room_id, "room_name": self.room_name, "capacity": self.capacity, "game_id":self.game_id, "host_id": self.host_id}


class Member(db.Model):
    __tablename__ = 'member'
    user_id = db.Column(db.String(100), primary_key=True)
    room_name = db.Column(db.String(64), primary_key=True)
    room_id = db.Column(db.Integer(), nullable=False)


    def __init__(self, user_id, room_name, room_id):
        self.user_id = user_id
        self.room_name = room_name
        self.room_id = room_id


    def json(self):
        return {"user_id": self.user_id, "room_name":self.room_name, "room_id": self.room_id}


#Get room based on game_id
@app.route("/game_id_room_detail", methods=['POST'])
def get_room():
    data = request.get_json()
    game_id = data['game_id']
    roomlist = Room.query.filter_by(game_id=game_id)
    rooms = [room.json() for room in roomlist]
    room_name_list = [room['room_name'] for room in rooms]
    if roomlist:
        return jsonify(
            {
                "code": 200,
                "data": {
                    'rooms': rooms,
                    'capacity': [Member.query.filter_by(room_name=single_room_name).count() for single_room_name in room_name_list]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no rooms."
        }
    ), 404

#Get room detail based on room_id
@app.route("/room_id_room_detail", methods=['POST'])
def get_room_detail():
    data = request.get_json()
    room_id = data['room_id']
    selected_room = Room.query.filter_by(room_id=room_id).first()
    members = Member.query.filter_by(room_id=room_id)
    no_of_members = Member.query.filter_by(room_id=room_id).count()
    try:
        return jsonify(
            {
                "code" : 201,
                "data": {
                    "room_name": selected_room.room_name,
                    "members":[member.user_id for member in members],
                    "capacity": no_of_members
                },
                "message" : "Retrieved room detail."
            }
        ), 201

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "room_id": room_id
                    },
                "message": "An error retrieving the room detail."
            }
        ), 500

#Create Room
#For this section, some changes r made. When room is created. Both room and member tables will be updated. 
@app.route("/room", methods=['POST'])
def create_room():
    data = request.get_json()
    try:
        print(f'\n\n---Creating Room: {data["room_name"]}...---')
        print(data)
        room = Room(room_name=data['room_name'],game_id=int(data['game_id']),capacity=int(data['capacity']),host_id=data['host_id'])
        db.session.add(room)
        db.session.commit()
        room_id = Room.query.filter_by(host_id=data['host_id'], room_name=data['room_name']).first().room_id
        member = Member(user_id=data['host_id'],room_name=data['room_name'], room_id=room_id)
        db.session.add(member)
        db.session.commit()

    except:
        print(f'\n\n---Cannot create Room: {data["room_name"]}...---')
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred creating the room."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": {
                "room_id": room.room_id,
                "room_info": room.json(),
                "room_name": room.room_name,
                "members" : [member.user_id for member in Member.query.filter_by(room_name=room.room_name).all()]
            },
            "message": "Room has successfully been created"
        },
    ), 201


#Join Room
@app.route("/room/join", methods=['POST'])
def join_room():
    data = request.get_json()
    room_id = data['room_id']
    selected_room = Room.query.filter_by(room_id=room_id).first()
    no_of_members = Member.query.filter_by(room_id=room_id).count()
    if no_of_members==selected_room.capacity:
        return jsonify(
            {
                "code" : 401,
                "data": {
                    "user_id": member.user_id,
                    "room_id": member.room_id
                },
                "message" : "Room is full."
            }
        ), 401
    #Get user id via request
    else:
        member = Member(user_id=data['user_id'],room_id=data['room_id'], room_name=data['room_name'])
    try:
        db.session.add(member)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "user_id": member.user_id,
                    "room_id": member.room_id
                    },
                "message": "An error occurred joining the room."
            }
        ), 500

    print(member.json())

    return jsonify(
        {
            "code": 201,
            "data": {
                "user_id": member.user_id,
                "room_id": member.room_id
            },
            "message":"Successfully joined room."
        }
    ), 201


#Leave Room
@app.route("/room", methods=['DELETE'])
def leave_room():
    request_info = request.get_json()
    room_id = request_info['room_id']
    user_id = request_info['user_id']

    selected_room = Room.query.filter_by(room_id=room_id).first()

    room_info = selected_room.json()
    host_id = room_info['host_id']

    data = {"user_id": user_id, "room_info": room_info} # to store room_info which will be returned later in response

    if host_id != user_id: # user is not the host, regular procedures 
        try:
            data["is_host"] = False
            deleted_user = Member.query.filter_by(user_id=user_id).first()
            db.session.delete(deleted_user)
            db.session.commit()

            code = 201
            message = "Successfully left room."
        except Exception as e:
            code = 500
            message = "An error occurred leaving the room: " + str(e)
    else: # user is the host, need to close entire room
        try:
            data["is_host"] = True
            room_members = Member.query.filter_by(room_id=room_id).all() # filter for all members of the room
            member_ids = []

            for room_member in room_members: # delete all members from room
                member_ids.append(room_member.user_id)
                db.session.delete(room_member)

            db.session.delete(selected_room) # delete room itself
            db.session.commit()

            code = 201
            message = "Successfully left room."
            data["member_ids"] = member_ids # return room_members in json response as well

        except Exception as e:
            code = 500
            message = "An error occurred leaving the room: " + str(e)

        
    return jsonify(
        {
            "code": code,
            "data": data,
            "message": message
        }
    ), code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
