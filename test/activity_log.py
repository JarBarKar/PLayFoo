import json
import os

import amqp_setup
from sqlalchemy import Table, Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime as dt

Base = declarative_base()

engine = create_engine('mysql+mysqlconnector://root@localhost:3306/playfoo')

Session = sessionmaker(bind=engine)
session = Session()

class Activity_Log(Base):
    __tablename__ = 'activity_log'
    activity_id = Column(Integer(), primary_key=True)
    code = Column(Integer(), nullable=False)
    data = Column(String(1000), nullable=False)
    message = Column(String(128), nullable=False)
    timestamp= Column(DateTime, default=dt.datetime.now())

    def __init__(self, code, data, message):
        self.code = code
        self.data = data
        self.message = message

    def json(self):
        return {"activity_id": self.activity_id, "code": self.code, "data": self.data, "message": self.message, "timestamp": self.timestamp}

log1 = Activity_Log(201, "test nia", "test message nia")
session.add(log1)
session.commit()


# @app.route("/activity_log", methods=['POST'])
# def activity_log_receive():
#     print('\n--Receiving data...--')
#     data = request.get_json()
#     data = json.loads(data)
#     activity_log = Activity_Log(code=data['code'],data=json.dumps(data['data']),message=data['message'])
#     try:
#         db.session.add(activity_log)
#         db.session.commit()
#         print("Recording an activity log:")
#         print(activity_log)
#     except:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": data,
#                 "message": "An error occurred creating the activity_log."
#             }
#         ), 500
#     return jsonify(
#         {
#             "code": 201,
#             "data": data,
#             "message": "Activity successfully logged in the database."
#         }
#     ), 201


# if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')

#     print("\nThis is " + os.path.basename(__file__), end='')
    # print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    
