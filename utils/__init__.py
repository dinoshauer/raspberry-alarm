import json
import os


def get_db(path='db.json'):
    if os.path.exists(path):
        with open(path, 'r') as fd:
            db = json.load(fd)
    else:
        db = {
            'playlist': None,
            'days': {
                'mon': None,
                'tue': None,
                'wed': None,
                'thu': None,
                'fri': None,
                'sat': None,
                'sun': None,
            }
        }
        with open(path, 'w') as fd:
            json.dump(db, fd)
    return db


def write_db(db, path='db.json'):
    with open(path, 'w') as fd:
        json.dump(db, fd)
    return db
