import json
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import amqp_setup


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/playfoo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)  

class Error(db.Model):
    __tablename__ = 'Error'
    error_id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.Integer(), nullable=False)
    data = db.Column(db.String(1000), nullable=False)
    message = db.Column(db.String(128), nullable=False)
    timestamp= db.Column(db.DateTime, server_default=db.func.now())

    

    def __init__(self, code, data, message):
        self.code = code
        self.data = data
        self.message = message



    def json(self):
        return {"error_id": self.activity_id, "code": self.code, "data": self.data, "message": self.message, "timestamp": self.timestamp}



@app.route("/error", methods=['POST'])
def error_receive():
    print('\n--Receiving data...--')
    data = request.get_json()
    data = json.loads(data)
    print(data)
    error = Error(code=data['code'],data=json.dumps(data['data']),message=data['message'])
    try:
        db.session.add(error)
        db.session.commit()
        print("Recording an error log:")
        print(data)
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred creating an error log."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": data,
            "message": "Error successfully logged in the database."
        }
    ), 201


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    app.run(port=5006, debug=True)
    print("\nThis is " + os.path.basename(__file__), end='')
    # print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    
