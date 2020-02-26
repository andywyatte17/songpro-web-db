from flask import Flask
import flask
from collections import namedtuple
import os
from striprtf.striprtf import rtf_to_text

HERE = os.path.dirname(os.path.realpath(__file__))
BASE_JSON = "Chorus.json" if (not "SONGPRO_CHORUS_JSON"  in os.environ) \
                          else os.environ["SONGPRO_CHORUS_JSON"]
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
    with open(os.path.join(HERE, "..", "json", BASE_JSON), "rb") as f:
        js = json.load(f)
        js = sorted(js, key = lambda x: x.get("Title", ""))
    songs = []
    songs_tuple = namedtuple("songs", ["name", "index"])
    n = -1
    for x in js:
        n += 1
        songs.append( songs_tuple(name=x["Title"], index=n) )
    return flask.render_template("songs.template", songs = songs)

def GetChorusText(js, key):
    result = rtf_to_text(js.get(key, ""))
    result = result.rstrip("\n")
    result = result.lstrip("\n")
    return result

@app.route("/songs/<song_id>")
def song(song_id):
    import json
    with open(os.path.join(HERE, "..", "json", BASE_JSON), "rb") as f:
        js = json.load(f)
        js = sorted(js, key = lambda x: x.get("Title", ""))
    js = js[int(song_id)]
    chorus_tuple = namedtuple("chorus_tuple", ["Title", "Verse1", "Chorus"])
    chorus = chorus_tuple(Title = GetChorusText(js, "Title"),
                          Verse1 = GetChorusText(js, "Verse1"),
                          Chorus = GetChorusText(js, "Chorus"))
    print(repr(chorus))
    return flask.render_template("chorus.template", chorus = chorus)
