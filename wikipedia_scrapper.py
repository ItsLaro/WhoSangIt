import requests
from bs4 import BeautifulSoup

class ArtistBio:
    def __init__(self, year, location, genre, relation):
        self.year = year
        self.location = location 
        self.genre = genre
        self.relation = relation
    def __str__(self):
        return f'''They were born/formed in the {self.year} in {self.location}. 
        They're known for playing {self.genre} and are related to artists like {self.relation}.'''

def fetch_bio(artist_name):
    '''
    Fetches information about an artist from www.allmusic.com.
    Returns them inside a ArtistBio object.
    '''

    #
    artist_words = artist_name.split()
    song_searchterm = '_'.join(artist_words)
    
    search_url = 'https://www.allmusic.com/search/artists/' + song_searchterm
    search_response = requests.get(search_url, 
        headers = {"Accept":"text/html"})
    print(search_url)
    #Parses HTML string from allmusic.com with bs4
    html_search_string = search_response.text
    print(html_search_string)
    parsed_search_html = BeautifulSoup(html_search_string, 'html.parser')
    print('PARSED')
    #
    search_result = parsed_search_html.find(class_='artist')
    print(search_result)
    
    return 'Function Ends.'

fetch_bio('John Lennon')