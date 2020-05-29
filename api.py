import flask
from flask import request, jsonify
from time import sleep
from billboard_scrapper import fetch_billboard
from lyrics_scrapper import fetch_lyrics
from biography_fetcher import fetch_bio


app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=['GET'])
def home():
    return '''<h1>Sing It! API</h1>
<p>A prototype API that crawls the web for music.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>That music chat could not be found.</p>", 404

@app.route('/api/v1/chart', defaults={'name' : 'hot-100'},  methods=['GET'])
def api_filter():
    print("Request made, acquiring billboard with lyrics.\n")
    
    query_parameters = request.args
    chart_name = query_parameters.get('name')
    # Some Popular Charts & corresponding chart_name path:
    #
    # Current Hot 100 Singles (Default):      'hot-100', 
    # Greatest Hot 100 Singles of All Times:  'greatest-hot-100-singles'
    # Top Songs from the 80's:                'greatest-billboards-top-songs-80s'
    # Greatest Hot Latin Songs:               'greatest-hot-latin-songs'
    # Hot EDM Songs:                          'dance-electronic-songs'

    result = {}
    billboard_entries = fetch_billboard(chart_name)
    for i in range(len(billboard_entries)):
        result[i] = {"rank" : billboard_entries[i].rank,
                    "title": billboard_entries[i].title,
                    "artist": billboard_entries[i].artist,
                    "lyrics": fetch_lyrics(billboard_entries[i].pretty_print()).verses()
                    }
        sleep(3) #throttles the crawling speed to avoid getting IP-blocked 
    return jsonify(result)

app.run()