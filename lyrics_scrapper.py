import requests
from bs4 import BeautifulSoup
from random import randint

class Lyrics:
    def __init__(self, lyrics):
        self.lyrics = lyrics

    def __str__(self):
        '''
        String represantion of the lyrics. 
        Takes away any extra spaces or new lines.
        '''
        return self.lyrics.strip()

    def verses(self):
        '''
        Returns the lyrics in a list containing each verse as a
        separate string. 
        '''
        verse_list = self.lyrics.split('\n\n')
        return verse_list

    def rand_verse(self):
        '''
        Returns a random verse from the entire lyrics.
        '''
        
        verse_list = self.lyrics.split('\n\n')
        #Makes a shallow copy of verse list to use in scenario of really short verses
        verse_list_copy = verse_list.copy()

        #Removes short verses from the list (Only 120+ chars remain)
        for verse in verse_list:
            if len(verse) < 120:
                verse_list.remove(verse)
                 
        #Scenario with short verses (less than 120 chars), just takes the longest
        if len(verse_list) == 1:
            return max(verse_list_copy, key=len)
   
        verse_num = randint(0,len(verse_list)-1)    
        return verse_list[verse_num].strip()

def fetch_lyrics(song):
    '''
    Fetches lyrics from https://www.azlyrics.com.
    Returns them inside a Lyrics object.
    TODO: 
        Better selection methodology to increase accuracy. Currently, we pick the first result out of the AZLyrics search result. 
        Regex could be implemented and take into account the actual artist as a separate element.
    '''

    #Take the song input and substitutes spaces with '+' to concatenate to url
    song_words = song.split()
    song_searchterm = '+'.join(song_words)
    
    search_url = 'https://search.azlyrics.com/search.php?q=' + song_searchterm
    search_response = requests.get(search_url, 
        headers = {"Accept":"text/html"})

    #Parses HTML string from AZlyrics.com with bs4
    html_search_string = search_response.text
    parsed_search_html = BeautifulSoup(html_search_string, 'html.parser')

    try:
        #Navigates parsed HTML to extract first result from our query in the webpage's search
        search_result = parsed_search_html.findChild(class_='text-left visitedlyr').find('a')['href']
        lyrics_response = requests.get(search_result, 
            headers = {"Accept":"text/html"})

        #Parses HTML string from AZlyrics.com containing the lyrics with bs4    
        html_lyrics_string = lyrics_response.text
        parsed_lyrics_html = BeautifulSoup(html_lyrics_string, 'html.parser')

        #Extracts the lyrics as a string
        fetched_lyrics = parsed_lyrics_html.find(class_='ringtone').findNext('div').get_text()
    
        return Lyrics(fetched_lyrics)

    except:
        return Lyrics("")

if __name__ == '__main__':
    song_name = input("\nEnter song name to fetch lyrics for:")
    lyrics = fetch_lyrics(song_name)
    print(lyrics)