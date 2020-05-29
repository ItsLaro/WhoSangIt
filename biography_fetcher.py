import requests
from bs4 import BeautifulSoup
import wikipedia

wikipedia.set_lang("en")

# class ArtistBio:
#     def __init__(self, year, location, genre, relation):
#         self.year = year
#         self.location = location 
#         self.genre = genre
#         self.relation = relation
#     def __str__(self):
#         return f'''They were born/formed in the {self.year} in {self.location}. 
#         They're known for playing {self.genre} and are related to artists like {self.relation}.'''

def fetch_bio(artist_name):
    '''
    Calls Wikipedia API to get artist. 
    TODO: Filter the information using regex to exclude explicit names and pronouns.
    '''

    Wiki_Page = wikipedia.page(artist_name)
    artistBio = Wiki_Page.summary
    
    return artistBio

if __name__ == '__main__':
    artist = input("Provide name of artist to fetch bio for: ")
    bio = fetch_bio(artist)
    print(bio)
