Raspberry Alarm
===============

A little script and an API to create an alarm clock that plays music from an
MPD server.

Read more here: http://mackwerk.dk/posts/weekend-project-spotify-alarm-clock-part-2/

# Installation

Clone this repo, create a virtualenv and `pip install -r requirements.txt`

# Documentation

## api.py

Add entries to the database:

    curl -XPOST http://0.0.0.0:5000/ -H "Content-Type:application/json" -d '
    {
      "playlist": "foo",
      "timeout": 120,
      "days": [
         {"day": "mon", "time": "06:00"},
         {"day": "sun", "time": "20:00"}
      ]
    }'

Get current entries from database:

    curl http://0.0.0.0:5000/
    {
      "days": {
        "fri": null,
        "mon": "06:00",
        "sat": null,
        "sun": "19:30",
        "thu": null,
        "tue": null,
        "wed": null
      },
      "timeout": 120
      "playlist": "foo"
    }

Get a list of available playlists:

    curl localhost:5000/playlists
    {
      "playlists": [
        "foo",
        "bar",
        "baz"
      ]
    }

## alarm-clock.py

Just run `alarm-clock.py` and it'll read from the database file `db.json` in 
the same directory. Hopefully you'll get woken up!
