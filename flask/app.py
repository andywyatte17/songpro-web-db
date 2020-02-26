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
    return flask.render_template("root.template", urls = get_urls())

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
    return flask.render_template("songs.template", songs = songs)
