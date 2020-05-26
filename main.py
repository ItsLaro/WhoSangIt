import lyrics_scrapper 
import billboard_scrapper
from random import randint, shuffle, choice
import pyfiglet

class Player:
    '''
    A Player class for this quiz. Contains strikes (up to 3),
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

    #While-loop ensures no exit from round_setup until lyrics have succesfully being fetched.
    while True:

        #Randomly picks 5 entries (no repeating artists) from billboard by shuffling it and stores object & artist inside previously defined lists
        shuffle(billboard_entries)
        index = 0
        while len(artist_options) < 5:
            entry_option = billboard_entries[index]
            artist_option = billboard_entries[index].artist
            if artist_option not in artist_options:
                entry_options.append(entry_option)
                artist_options.append(artist_option)
            index += 1

        try:
            #Selects on of the 5 entries & artist to have their lyrics displayed
            correct_entry = choice(entry_options)    
            correct_artist = correct_entry.artist

            #Fetches the random verse from the lyrics from the selected entry
            song_query = correct_entry.pretty_print()
            verse = lyrics_scrapper.fetch_lyrics(song_query).rand_verse()
        except AttributeError:
            #Happens when song lyrics were not available.
            pass
        else:
            #When lyrics have been obtained and round set up is succesful. Breaks out of while-loop.
            break

    return entry_options, artist_options, correct_artist, correct_entry, verse

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

def quiz_opening():
    '''
    Bubble prints opening.
    '''

    opening = pyfiglet.figlet_format("WHO  SANG  IT?")

    print(opening)
    input ('Press <Enter> to Start ')

def quiz_mode():
    '''
    Requests user for song selection (Billboard chart to be fetched for quiz). 
    '''
    #Labels all the options to be given to the player
    mode_options = {'Current Hot 100 Singles':'hot-100', 
                    'Greatest Hot 100 Singles of All Times':'greatest-hot-100-singles',  
                    "Top Songs from the 80's":'greatest-billboards-top-songs-80s', 
                    'Greatest Hot Latin Songs':'greatest-hot-latin-songs',
                    'Hot EDM Songs':'dance-electronic-songs'}
    enumerated_mode_options = list(enumerate(mode_options, start=1))

    for option in enumerated_mode_options:
        print(f'[{option[0]}] {option[1]}')

    while True:
        try:
            selection = int(input("Select song collection: "))
            if selection > len(enumerated_mode_options):
                raise IndexError
        except IndexError:
            print("Invalid Input. Please select song collection by inputting their associated number.")
            continue
        except ValueError:
            print("Invalid Input. Please select song collection by inputting their associated number.")
            continue
        else:
            break
    
    mode_option = enumerated_mode_options[selection-1]
    mode_key = mode_option[1]
    mode_value = mode_options[mode_key]

    return mode_value
    

def run_quiz():

        #Instantiates a player
        P1 = Player()

        playing = True
        round_number = 1

        #Bubble prints winning and losing screen
        winning_screen = pyfiglet.figlet_format("CONGRATULATIONS!") 
        losing_screen = pyfiglet.figlet_format("GAME OVER...")

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
                quiz_round(P1)

def quiz_round(player):
    
    #Sets up a new round
    entry_options, artist_options, correct_artist, correct_entry, verse = round_setup()
    
    #Determines number pertaining to the correct answer
    correct_selection = artist_options.index(correct_artist) + 1
    
    print('"' + verse + '"')
    print('\nWho sang it?')

    #Labels all the options to be given to the player
    selection_number = 1
    for item in entry_options:
        print(f'[{selection_number}] {item.artist}')
        selection_number += 1
    print(f'---Input {selection_number} for a hint---')

    #Request for input
    player_selection = select_artist()

    #Adds points or strike for result of player selection
    if player_selection  == correct_selection:
        print('Correct! +10 pts')
        player.add_points(10)
        input('\nPress <Enter> to continue...')
    else:
        print("That's not right...Strike!")
        player.add_strike()
        print(f'This is billboard entry {correct_entry}. The correct answer was: [{correct_selection}] ')
        input('\nPress <Enter> to continue...')


if __name__ == "__main__": 

    while True:
        quiz_opening()
        chart = quiz_mode()
        billboard_entries = billboard_scrapper.fetch_billboard(chart)
        run_quiz()
        replay = input("Play again? <yes/no>")
        try:
            if replay.lower()[0] == 'y':
                pass
            else:
                break
        except IndexError:
            break
