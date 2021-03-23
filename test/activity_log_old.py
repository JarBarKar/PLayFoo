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

class Activity_Log(db.Model):
    __tablename__ = 'activity_log'
    activity_id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.Integer(), nullable=False)
    data = db.Column(db.String(1000), nullable=False)
    message = db.Column(db.String(128), nullable=False)
    timestamp= db.Column(db.DateTime, server_default=db.func.now())

    

    def __init__(self, code, data, message):

        self.code = code
        self.data = data
        self.message = message



    def json(self):
        return {"activity_id": self.activity_id, "code": self.code, "data": self.data, "message": self.message, "timestamp": self.timestamp}



@app.route("/activity_log", methods=['POST'])
def activity_log_receive():
    print('\n--Receiving data...--')
    data = request.get_json()
    data = json.loads(data)
    activity_log = Activity_Log(code=data['code'],data=json.dumps(data['data']),message=data['message'])
    try:
        db.session.add(activity_log)
        db.session.commit()
        print("Recording an activity log:")
        print(activity_log)
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred creating the activity_log."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": data,
            "message": "Activity successfully logged in the database."
        }
    ), 201


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    app.run(port=5005, debug=True)
    print("\nThis is " + os.path.basename(__file__), end='')
    # print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    
