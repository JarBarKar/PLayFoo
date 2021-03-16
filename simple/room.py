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
    user_id = db.Column(db.String(12), primary_key=True)
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
    #json file sent here
    data = request.get_json()
    room = Room(**data)

    try:
        db.session.add(room)
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
@app.route("/book/<string:isbn13>", methods=['PUT'])
def update_book(isbn13):
    book = Book.query.filter_by(isbn13=isbn13).first()
    if book:
        data = request.get_json()
        if data['title']:
            book.title = data['title']
        if data['price']:
            book.price = data['price']
        if data['availability']:
            book.availability = data['availability'] 
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": book.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "isbn13": isbn13
            },
            "message": "Book not found."
        }
    ), 404

#Leave Room
@app.route("/book/<string:isbn13>", methods=['DELETE'])
def delete_book(isbn13):
    book = Book.query.filter_by(isbn13=isbn13).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "isbn13": isbn13
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "isbn13": isbn13
            },
            "message": "Book not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(port=5001, debug=True)
