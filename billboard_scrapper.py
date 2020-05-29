import requests
from bs4 import BeautifulSoup

class Billboard_Entry:
    '''
    Entry fetched from the billboard.
    Contains current rank, title and artist of the song.
    Prints in the following format: "[##] Song by Artist"
    '''
    def __init__(self,rank,title,artist):
        self.rank = rank
        self.title = title
        self.artist = artist
    def __str__(self):
        return f'[{self.rank}] {self.title} by {self.artist}'
    def pretty_print(self):
        '''
        Returns in a simplified format the title of song accompanied 
        by first name of artist for several uses(e.i. to input as query on a webpage).
        '''
        pretty_artist = self.artist.split(' ')[0]
        return f'{self.title} by {pretty_artist}'

class Billboard:
    '''
    Billboard object containing all the billboard entries
    '''

    def __init__(self, entries):
        self.entries = entries
        self.chart_name = entries[0]
    def __str__(self):
        string = ""
        for entry in self.entries:
            string += (str(entry) + "\n" )
        return string

class Billboard_Error(Exception):
    '''
    Custom exception for failure to properly parse an entry 
    '''
    pass

def fetch_billboard(chart='hot-100'):
    '''
    Fetches billboard from https://www.billboard.com.
    Defaults to The Top Hot 100 Billboard, but takes in a string of any Billboard
    chart in the form of '/chart_x'.
    Returns list with chart tile at index [0] and Billboard_Entry objects.
    TODO: 
    The Hot-100 page seems to have changed and therefore turned 'unscrapable'. Needs to be updated.
    '''
    url = 'https://www.billboard.com/charts/' + chart
    response = requests.get(url, 
        headers = {"Accept":"text/html"})

    #Parses HTML string from billboard.com with bs4
    html_string = response.text 
    parsed_html = BeautifulSoup(html_string, 'html.parser') 

    #fetches the chart's title
    chart_title = parsed_html.find('title').text

    #empty list to allocate all entry objects created from the info fetched
    entries = [] 

    #Line below is able to append chart title to index position 0 on resulting array
    #entries.append(chart_title)

    #Iterates over each entry on the billboard, creating a Entry Object and appending it to entries list
    if chart =='hot-100': 
        #Main 100-Billboard chart has a different DOM structure than the rest.

        ranks = parsed_html.find_all(class_='chart-element__rank__number')
        titles = parsed_html.find_all(class_='chart-element__information__song')
        artists = parsed_html.find_all(class_='chart-element__information__artist')

        for i in range(len(parsed_html.find_all(class_='chart-list__element'))):
            try:
                rank = int(ranks[i].get_text().strip())
                title = titles[i].get_text().strip()
                artist = artists[i].get_text().strip() or ''
                if artist == '':
                    artist = 'Unknown'
            except:
                message = "Failed to parse entry: " + str(item)
                raise Billboard_Error(message)
            
            entry = Billboard_Entry(rank, title, artist)
            entries.append(entry)  

    else: 
        #All other charts are seemingly structured the same.
       
        for item in parsed_html.find_all(class_='chart-list-item'):
            try:
                rank = int(item['data-rank'].strip())
                title = item['data-title'].strip()
                artist = item['data-artist'].strip() or ''
                if artist == '':
                    artist = 'Unknown'
            except:
                message = "Failed to parse entry"
                raise Billboard_Error(message)
            
            entry = Billboard_Entry(rank, title, artist)
            entries.append(entry)

    return entries

if __name__ == '__main__':
    entries = fetch_billboard()
    billboard = Billboard(entries)
    print(billboard)


