from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route("/gamedetails")
def get_gamesdetails():
    game_id = request.args.get("id")
    games = []
    gamelist = requests.get(
        'https://api.rawg.io/api/games/' + str(game_id) + '?key=d64ef8b888564641b6a7b34f3e2e763c').json()

    game = {}

    game['background_image'] = gamelist['background_image']

    temp = []
    for g in gamelist['genres']:
        temp.append(g['name'])
    game['genre'] = temp

    game['description'] = gamelist['description_raw']
    game['name'] = gamelist['name']
    game['rating'] = gamelist['rating']
    game['released'] = gamelist['released']

    games.append(game)

    return jsonify(games), 200


@app.route("/banner")
def get_banner():
    gamesid = [10213, 3498, 19369]
    games = []
    for gid in gamesid:
        gamelist = requests.get('https://api.rawg.io/api/games/' +
                                str(gid) + '?key=d64ef8b888564641b6a7b34f3e2e763c').json()

        game = {}
        game['background_image'] = gamelist['background_image']

        temp = []
        for g in gamelist['genres']:
            temp.append(g['name'])

        game['genre'] = temp
        game['id'] = gid
        game['description'] = gamelist['description_raw']
        game['name'] = gamelist['name']
        game['rating'] = gamelist['rating']
        game['released'] = gamelist['released']

        games.append(game)

    return jsonify(games), 200


@app.route("/toprated")
def get_toprated():
    games = []
    gamelist = requests.get(
        'https://api.rawg.io/api/games?apikey=d64ef8b888564641b6a7b34f3e2e763c').json()
    for i in range(len(gamelist['results'])):
        if gamelist['results'][i]['rating'] > 4:
            game = {}

            game['background_image'] = gamelist['results'][i]['background_image']
            temp = []
            for g in gamelist['results'][i]['genres']:
                temp.append(g['name'])
            game['genre'] = temp
            game['id'] = gamelist['results'][i]['id']

            # game_id = gamelist['results'][i]['id']
            # desc_api = requests.get(
            #     'https://api.rawg.io/api/games/' + str(game_id) + '?key=d64ef8b888564641b6a7b34f3e2e763c').json()
            # game['description'] = desc_api['description_raw']

            game['name'] = gamelist['results'][i]['name']
            game['rating'] = gamelist['results'][i]['rating']
            game['released'] = gamelist['results'][i]['released']

            games.append(game)

    return jsonify(games), 200


@app.route("/games", methods=["GET"])
def get_games():
    genre = request.args.get("genre")
    page = request.args.get('page', default=1)
    games = []
    gamelist = requests.get(
        'https://api.rawg.io/api/games?key=d64ef8b888564641b6a7b34f3e2e763c&genres=' + genre + '&page=' + str(page) + '&page_size=10').json()

    for i in range(len(gamelist['results'])):
        game = {}

        game['background_image'] = gamelist['results'][i]['background_image']

        temp = []
        for g in gamelist['results'][i]['genres']:
            temp.append(g['name'])
        game['genre'] = temp
        game['id'] = gamelist['results'][i]['id']
        game['name'] = gamelist['results'][i]['name']
        game['rating'] = gamelist['results'][i]['rating']
        game['released'] = gamelist['results'][i]['released']

        games.append(game)

    return jsonify(games), 200


# @app.route("/room", methods=["POST"])
# def create_room():
#     data = request.get_json()
#     print(data)
#     return(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
