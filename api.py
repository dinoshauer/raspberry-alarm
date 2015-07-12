from datetime import datetime

from flask import abort, Flask, jsonify, request
from mpd import MPDClient

from utils import get_db, write_db

app = Flask(__name__)
client = MPDClient()


@app.route('/', methods=['POST'])
def create_alarms():
    data = request.get_json()
    db = get_db()

    try:
        db['playlist'] = data.get('playlist')
        for entry in data['days']:
            day = entry['day']
            time_str = entry['time']
            db['days'][day] = time_str

        if write_db(db):
            return 'ok\n'

    except KeyError as exc_info:
        abort(400, exc_info)


@app.route('/', methods=['GET'])
def get_alarms():
    return jsonify(get_db())


@app.route('/playlists', methods=['GET'])
def get_playlists():    
    client.connect('localhost', 6600)
    playlists = [item['playlist'] for item in client.listplaylists()]
    client.disconnect()
    return jsonify({'playlists': playlists})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
