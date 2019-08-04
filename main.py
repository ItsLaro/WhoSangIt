from lyrics_scrapper import fetch_lyrics
from billboard_scrapper import Billboard_Entry, billboard
from random import randint, shuffle, choice
import pyfiglet

class Player:
    '''
    A Player class for this game. Contains strikes (up to 3),
    points (up to 100), and tracks allowance of the 2 hints.
    '''
    def __init__(self, strikes=0, points=0, hints='---'):
        self.strikes = strikes
        self.points = points
        self.hints = hints
    def __str__(self):
        strike_marks = ['__ __ __', 'X __ __', 'X X __']
        return f"Points: {self.points}/50 | Strikes: {strike_marks[self.strikes]} | Hints Available: {self.hints} "
    def add_strike(self):
        self.strikes += 1
    def add_points(self, amount):
        self.points += amount
    def use_hint(self):
        self.hints -= 1
    

def round_setup():
    '''
    Make preparations for a new round.
    Selects 5 random entries as options with 1 as the right answer. 
    '''
    #Allocates entries and corresponding artists to match with user entry.
    entry_options = []
    artist_options = []

    #Randomly picks 5 entries from billboard by shuffling it and stores object & artist inside previously defined lists
    shuffle(billboard_entries)
    for index in range(1,6):
        entry_option = billboard_entries[index]
        artist_option = billboard_entries[index].artist
        entry_options.append(entry_option)
        artist_options.append(artist_option)

    #Selects on of the 5 entries & artist to have their lyrics displayed
    correct_entry = choice(entry_options)    
    correct_artist = correct_entry.artist

    #Fetches the random verse from the lyrics from the selected entry
    song_query = correct_entry.pretty_print()
    verse = fetch_lyrics(song_query).rand_verse()

    return entry_options, artist_options, correct_artist, verse

def select_artist():
    '''
    Allows the user to make their selection based on the 5 options displayed
    while handling errors.
    '''
    while True:
        try:
            selection = int(input("Select from the following numbered artists: "))
            if selection > 6:
                raise IndexError
        except IndexError:
            print("Invalid Input. Please select an artist by inputting their associated number.")
            continue
        except ValueError:
            print("Invalid Input. Please select an artist by inputting their associated number.")
            continue
        else:
            return selection

def run_game():

        #Bubble prints opening, winning screen and losing screen.
        opening = pyfiglet.figlet_format("WHO  SANG  IT?")
        winning_screen = pyfiglet.figlet_format("CONGRATULATIONS!") 
        losing_screen = pyfiglet.figlet_format("GAME OVER...")

        print(opening)
        input ('Press <Enter> to Start ')

        #Instantiates a player
        P1 = Player()

        playing = True
        round_number = 1

        #Progresses through rounds, checking if end-game conditions have been met
        while playing:
            if P1.strikes == 3:
                print(losing_screen)
                playing = False
            elif P1.points == 50:
                print(winning_screen)
                playing = False
            else:
                print(f'\nROUND-{round_number}')
                print(P1, end='\n\n')
                round_number += 1
                game_round(P1)

def game_round(player):
    
    #Sets up a new round
    entry_options, artist_options, correct_artist, verse = round_setup()
    
    #Determines number pertaining to the correct answer
    correct_selection = artist_options.index(correct_artist) + 1
    
    print('"' + verse + '"')
    print('\nWho sang it?')

    #Labels all the options to be given to the player
    selection_number = 1
    for item in entry_options:
        print(f'[{selection_number}] {item.artist}')
        selection_number += 1
    print('---Input [6] for a hint---')

    #Request for input
    player_selection = select_artist()

    #Adds points or strike for result of player selection
    if player_selection  == correct_selection:
        print('Correct!')
        player.add_points(10)
        input('\nPress <Enter> to continue...')
    else:
        print("That's not right...")
        player.add_strike()
        input('\nPress <Enter> to continue...')

if __name__ == "__main__": 

    while True:
        billboard_entries = billboard('greatest-hot-100-singles')
        #dance-electronic-songs'
        #'greatest-hot-100-singles'
        #'greatest-billboards-top-songs-80s'
        #'greatest-hot-latin-songs'
        #'pop-songs'
        run_game()
        replay = input("Play again? <yes/no>")
        try:
            if replay.lower()[0] == 'y':
                pass
            else:
                break
        except IndexError:
            break
