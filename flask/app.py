from flask import Flask
import flask
from collections import namedtuple
import os

HERE = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)

def get_urls():
    url_tuple = namedtuple("urls", ["url", "text"])
    return (
        url_tuple(url = "/songs", text = "Songs")
        ,
    )

@app.route("/")
def root():
    return flask.render_template_string("""<!doctype html>
    <title>SongProDB</title>
    <body>
    <div>
    <h1>SongProDB</h1>
    <div>
    {% for url in get_urls() %}
        <a href="{{ url.url }}">{{ url.text }}</a>
    {% endfor %}
    </div>
    </body>""", get_urls = get_urls)

@app.route("/songs")
def songs():
    import json
    with open(os.path.join(HERE, "..", "json", "Chorus.json"), "rb") as f:
        js = json.load(f)
    songs = []
    songs_tuple = namedtuple("songs", ["name", "index"])
    n = -1
    for x in js:
        n += 1
        songs.append( songs_tuple(name=x["Title"], index=n) )
    return flask.render_template_string("""<!doctype html>
    <title>Songs</title>
    <body>
    <div>
    <h1>Songs</h1>
    <div>
    {% for song in songs %}
        <a href="/songs/{{ song.index }}">{{ song.name }}</div>
    {% endfor %}
    </div>
    </body>""", songs = songs)
