from flask import Flask, request, send_from_directory
import flask
from collections import namedtuple
import os
from striprtf.striprtf import rtf_to_text
import json
import sys

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

# ...

def maybe_rtf_to_text(maybe_rtf):
    return maybe_rtf if not maybe_rtf.startswith("{\\rtf1") \
                else rtf_to_text(maybe_rtf).lstrip("\n").rstrip("\n")

def TokensFromJson(json_item):
    parts = set()
    for k in json_item.keys():
        text = maybe_rtf_to_text(json_item[k])
        text = text.replace(",", " ").replace(";", " ")
        text = text.replace(":", " ").replace("\n", " ")
        text = text.replace(".", " ").replace("!", " ")
        text = text.replace("\r", " ")
        for item in text.split(" "):
            parts.add(item.lower())
    return parts

# ...

@app.route("/")
def root():
    return flask.render_template("root.template", urls = get_urls())

def songs_n(songs_int_list):
    songs_int_list = set(songs_int_list)
    global loaded_json
    js = loaded_json[:]
    js = sorted(js, key = lambda x: x.get("Title", ""))
    songs = []
    songs_tuple = namedtuple("songs", ["name", "index"])
    n = -1
    for x in js:
        n += 1
        if not n in songs_int_list:
            continue
        songs.append( songs_tuple(name=x["Title"], index=n) )
    return flask.render_template("songs.template", songs = songs)

@app.route("/songs")
def songs():
    global loaded_json
    js = loaded_json[:]
    return songs_n([x for x in range(len(js))])

def GetChorusText(js, key):
    result = maybe_rtf_to_text(js.get(key, ""))
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

@app.route("/json/<song_id>")
def json_root(song_id):
    import pprint
    global loaded_json
    js = loaded_json[:]
    js = sorted(js, key = lambda x: x.get("Title", ""))
    js = js[int(song_id)]
    jst = json.dumps(js, indent=2)
    return flask.render_template("json.template", \
        json_text = jst, tokens = pprint.pformat(TokensFromJson(js)))

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
    #print(KEYS)
    for key in KEYS:
        js[key] = maybe_rtf_to_text(js.get(key, ""))
    if js["Sequence"]=='':
        js["Sequence"] = ExtractSequence(js, SEQUENCE_LOOKUP)
    chorus_tuple = namedtuple("chorus_tuple", KEYS)
    chorus = chorus_tuple(**js)
    #print(repr(chorus))

    section_tuple = namedtuple("section_tuple", ["name", "text"])
    sections = []
    for seqV in js["Sequence"]:
        for key, seq in SEQUENCE_LOOKUP:
            if seq==seqV:
                sections = sections + [ section_tuple(name=key, text=js[key]) ]
                continue

    return flask.render_template("chorus.template", chorus = chorus, sections = sections)

# ...

@app.route("/song_search")
def song_search():
    global loaded_json
    js = loaded_json[:]
    js = sorted(js, key = lambda x: x.get("Title", ""))
    c, n_max = -1, 200000
    my_parts = set([x.lower() for x in request.args.get('search').split(" ") if x != ""])
    songs_int_list = []
    for jsi in js:
        c += 1
        parts = TokensFromJson(jsi)
        if my_parts.intersection(parts)==my_parts:
            songs_int_list.append(c)
            n_max -= 1
            if n_max==0: break
    #print(songs_int_list)
    return songs_n(songs_int_list)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

# ...

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    if "--debug" in sys.argv[1:]:
        app.run(host='127.0.0.1', port=8080, debug=True)
    else:
        app.run(host='127.0.0.1', port=8080, debug=False)

# [END gae_python37_app]
