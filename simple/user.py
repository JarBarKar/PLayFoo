from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    """
    creates User table with the following attributes:
    user_id: varchar(12), primary key
    name: varchar(16)
    """
    __tablename__ = 'user'

    user_id = db.Column(db.String(12), primary_key=True)
    name = db.Column(db.String(16), nullable=False)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def json(self):
        return {"user_id":self.user_id, "name":self.name}

@app.route("/user/<string:user_id>")
def find_by_user_id(user_id):
    """
    to retrieve user information by user_id
    """
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Book not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)