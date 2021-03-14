from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    """
    creates User table with the following attributes:
    userid: varchar(12), primary key
    name: varchar(16)
    """
    __tablename__ = 'user'

    userid = db.Column(db.String(12), primary_key=True)
    name = db.Column(db.String(16), nullable=False)

    def __init__(self, userid, name):
        self.userid = userid
        self.name = name

    def json(self):
        return {"userid":self.userid, "name":self.name}

@app.route("/user/<string:userid>")
def find_by_userid(userid):
    """
    to retrieve user information by userid
    """
    user = User.query.filter_by(userid=userid).first()
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