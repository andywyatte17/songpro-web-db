from flask import Flask
import flask
from collections import namedtuple
import os
from striprtf.striprtf import rtf_to_text
import json

# [START gae_python37_app]

HERE = os.path.dirname(os.path.realpath(__file__))
BASE_JSON = "Chorus.json" if (not "SONGPRO_CHORUS_JSON"  in os.environ) \
                          else os.environ["SONGPRO_CHORUS_JSON"]
app = Flask(__name__)

# ...

loaded_json = None
with open(os.path.join(HERE, "json", BASE_JSON), "rb") as f:
    loaded_json = json.load(f)

# ...

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
    global loaded_json
    js = loaded_json[:]
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

def InvertedDict(d):
    result = {}
    for key in d.keys():
        value = d[key]
        result[value] = key
    return result

SEQUENCE_LOOKUP = ( ('Chorus','C'), ('Verse1','1'), ('Verse2','2'), ('Verse3','3'), ('Verse4','4'), ('Verse5','5'), \
                    ('Verse6','6'), ('Verse7','7'), ('Verse8','8'), ('Bridge','B'), )

def ExtractSequence(chorus, SEQUENCE_LOOKUP):
    result = ""
    for key, seq in SEQUENCE_LOOKUP:
        v = chorus.get(key, "")
        if v!='':
            result.append(seq)
    return result

@app.route("/songs/<song_id>")
def song(song_id):
    global loaded_json
    js = loaded_json[:]
    js = sorted(js, key = lambda x: x.get("Title", ""))
    js = js[int(song_id)]
    KEYS = js.keys()
    KEYS_CUR = '''['Ref', 'Verse1', 'Verse2', 'Verse3', 'Verse4', 'Verse5', 'Verse6', 'Verse7', 'Verse8', 'Chorus', \
            'Bridge', 'PreChorus', 'Chorus2', 'MidSection', 'Intro', 'Title', 'TitleX', 'Sequence', 'Music', \
            'Font', 'Italic', 'Bold', 'FontSize', 'Outline', 'OneColour', 'Author', 'Copyright', 'BackColor', \
            'ForeColor', 'FooterColor', 'Category', 'Plus', 'Key', 'Notes', 'SongBook', 'Mod', 'SoundView', \
            'VideoView', 'View', 'BibleRef', 'BibleEndRef', 'BibleVersion', 'PowerPointFile', 'StartSlide', \
            'EndSlide', 'TimedSlides', 'Continuous', 'PPDate', 'Liturgy', 'TypeRef', 'HashPosition', \
            'HashSelected', 'Item', 'CCL', 'CCLSongID', 'DVDStartTime', 'DVDendtime', 'DVDid', 'Info', \
            'DVDTitle', 'AutoTextFade', 'Mute']'''
    print(KEYS)
    for key in KEYS:
        js[key] = rtf_to_text(js.get(key, ""))
    if js["Sequence"]=='':
        js["Sequence"] = ExtractSequence(js, SEQUENCE_LOOKUP)
    chorus_tuple = namedtuple("chorus_tuple", KEYS)
    chorus = chorus_tuple(**js)
    print(repr(chorus))

    section_tuple = namedtuple("section_tuple", ["name", "text"])
    sections = []
    for seqV in js["Sequence"]:
        for key, seq in SEQUENCE_LOOKUP:
            if seq==seqV:
                sections = sections + [ section_tuple(name=key, text=js[key]) ]
                continue

    return flask.render_template("chorus.template", chorus = chorus, sections = sections)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

# [END gae_python37_app]
