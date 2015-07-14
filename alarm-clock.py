import datetime
import logging
import sys
import time

from mpd import MPDClient, CommandError, ConnectionError

from utils import get_db


_handler = logging.StreamHandler(sys.stdout)
_format = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s')
_handler.setFormatter(_format)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(_handler)

CACHE = {}


def trim_cache(cache, threshold=1):
    now = datetime.datetime.now()
    threshold = now - datetime.timedelta(days=threshold)
    marked_deleted = []

    for key, _ in cache.items():
        if key < threshold:
            marked_deleted.append(key)

    for key in marked_deleted:
        del cache[key]

    return cache


def play(playlist):
    client = MPDClient()
    client.connect('localhost', 6600)

    if playlist:
        try:
            client.listplaylistinfo(playlist)
            client.clear()
            client.load(playlist)
            client.play()
        except CommandError as exc_info:
            LOGGER.error('Could not load playlist', exc_info)
            client.disconnect()
            return False
    else:
        LOGGER.warn('No playlist specified, using current playlist')
        client.play()
    client.disconnect()
    return True


def main():
    global CACHE
    LOGGER.info('Starting alarm-clock')

    while True:
        now = datetime.datetime.now()
        today = now.strftime('%a').lower()

        db = get_db()
        playlist = db['playlist']
        alarm_str = db['days'][today]
        
        if alarm_str is not None:
            hour, minute = alarm_str.split(':')

            alarm_hour = datetime.time(int(hour), int(minute))

            dt = datetime.datetime.combine(now, alarm_hour)

            if not CACHE.get(dt, False):
                if dt <= now:
                    res = play(playlist)
                    if res:
                        CACHE[dt] = True

        CACHE = trim_cache(CACHE)
        time.sleep(60)


if __name__ == '__main__':
    main()
