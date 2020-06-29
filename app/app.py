from flask import Flask, render_template, request
from searchapp.app.search import do_general_search, do_advanced_search, do_general_range_search

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
    )

#basic search
@app.route('/search', methods=['GET', 'POST'])
def general_search():
    query = request.args.get('search')
    boost_array = [1,1,1,1,1,1,1,1]
    num_results = 0
    isRange = False

    tokens = query.split()

    for word in tokens:

        #check whether the phrase include a number
        if word.isdigit():
            isRange = True
            num_results = int(word)

        #check mappings for synonyms related to differnet fields
        for i in range(2, 8):
            if word in terms_list[i]:
                boost_array[i] = 5

        if word in terms_popular:
           if(not isRange):
            isRange = True
            num_results = 450

    if len(tokens) > 5:
        boost_array[1] = 5

    fields = boost(boost_array)
    results = []
    if(isRange):
        #if phrase has a number do a sorted query
        results = do_general_range_search(query,num_results, fields)
        return render_template(
            'index.html',
            hit=results['hits']['hits'],
            search_term=query,
        )
    else:
        results = do_general_search(query,fields)

        return render_template(
            'index.html',
            hit=results['hits']['hits'],
            aggs=results['aggregations'],
            search_term=query,
        )

#advanced search
@app.route('/advanced_search', methods=['GET', 'POST'])
def advanced_search():

    Body = request.args.get('Body')
    Artist = request.args.get('Artist')
    Lyrics = request.args.get('Lyrics')
    Music = request.args.get('Music')
    Genre = request.args.get('Genre')
    num_results = 50
    results = do_advanced_search(Body, Artist, Lyrics, Music, Genre, num_results)
    return render_template(
        'index.html',
        artist_term=Artist,
        lyrics_term=Lyrics,
        music_term=Music,
        genre_term=Genre,
        body_term=Body,
        hit=results['hits']['hits'],
        aggs=results['aggregations']
    )

#function to boost fields according to the terms included in search phrase
def boost(boost_array):
    term0 = "Title^{}".format(boost_array[0])
    term1 = "Body^{}".format(boost_array[1])
    term2 = "Artist^{}".format(boost_array[2])
    term3 = "Lyrics^{}".format(boost_array[3])
    term4 = "Music^{}".format(boost_array[4])
    term5 = "Genre^{}".format(boost_array[5])
    term6 = "Key^{}".format(boost_array[6])
    term7 = "Beat^{}".format(boost_array[7])

    return [term0, term1, term2, term3, term4, term5, term6, term7]

#synonyms list to map token in the search pharses to their corresponding fields
terms_artist = ['ගායකයා','ගයන','ගයපු','ගයනවා','ගායනා','ගායනය','ගැයු','ගැයූ','කිව්ව','කීව','කියපු','කී','කියන','කියු','කියූ']
terms_lyrics = ['රචකයා','රචිත','රචනා','රචක','ලියන්නා','ලියන','ලියපු','ලියව්‌ව','ලිව්‌ව','ලියු','ලියූ','ලීවා','ලීව']
terms_music = ['සංගීත', 'සංගීතවත්','සංගීතය']
terms_genre = ['කැලිප්සෝ','පොප්ස්', 'පොප්', 'සම්භාව්ය','කණ්ඩායම්','යුගල','චිත්‍රපට','වත්මන්','අලුත්','නව','පැරණි']
terms_key = ['Minor','Major','minor','major']
terms_beat = ["6/8",'4/4', '3/4','2/4','7/8']
terms_popular=['හොඳම','හොදම','හොද','හොඳ','ප්‍රචලිත','ප්‍රසිද්ධ','ජනප්‍රිය','ජනප්‍රියම','සුපිරි', 'සුපිරිම']

terms_list = [None, None, terms_artist, terms_lyrics, terms_music, terms_genre, terms_key, terms_beat]