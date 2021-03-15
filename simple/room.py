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
    room_id = db.Column(db.Integer(6), primary_key=True)
    room_name = db.Column(db.String(64), nullable=False)
    game_id= db.Column(db.Integer(3), nullable=False)
    capacity = db.Column(db.Integer(2), nullable=False)
    host = db.Column(db.String(12), nullable=False)
    

    def __init__(self, room_id, room_name, game_name, capacity, host):
        self.room_id = room_id
        self.room_name = room_name
        self.game_name = game_name
        self.capacity = capacity
        self.host = host

    def json(self):
        return {"room_id": self.room_id, "room_name": self.room_name, "capacity": self.capacity, "game_name":self.game_name, "host": self.host}


#get room based on game_id
@app.route("/room/<string:game_id>")
def get_room():
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
@app.route("/room/<string:user_id>", methods=['POST'])
def create_room(user_id):
    if (Book.query.filter_by(isbn13=isbn13).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "isbn13": isbn13
                },
                "message": "Book already exists."
            }
        ), 400

    data = request.get_json()
    book = Book(isbn13, **data)

    try:
        db.session.add(book)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "isbn13": isbn13
                },
                "message": "An error occurred creating the book."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": book.json()
        }
    ), 201


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
    app.run(port=5000, debug=True)
