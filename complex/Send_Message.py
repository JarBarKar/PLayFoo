from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import requests
from invokes import invoke_http
import pika

import json

app = Flask(__name__)
CORS(app)

# user_URL = "http://localhost:5000/user"
room_URL = "http://localhost:5001/room"
# game_URL = "http://localhost:5002/game"
message_URL = "http://localhost:5003/message"

@app.route('/send', methods=['POST'])
def send_message():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # we expect room_id & user_id to be in request
            request_info = request.get_json()
            print("\nReceived a send message request in JSON:", request_info)

            # do the actual work
            # 1. send room and user info
            result = processSendMessage(request_info)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "Send_Message.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processSendMessage(request_info):
    print('\n\n-----Invoking message microservice-----')    
    
    message_result = invoke_http(
        message_URL + "/send", method="POST", json=request_info)
    print("message_result:", message_result, '\n')

    return {
        "code": 201,
        "data": {
            "message_result": message_result
        }
    }

if __name__ == "__main__":
    app.run(port=5103, debug=True)