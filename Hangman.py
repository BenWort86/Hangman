'''
Hangman game with score tracking, rounds, and persistent player storage
in JSON.
'''

import json
import os
import random

# JSON file for storing player data
FILENAME = 'player.json'

# ANSI color codes for terminal output
BROWN = '\033[33m'
GREEN = '\033[32m'
RESET = '\033[0m'


class Player:
    '''
    Represents a player with name, score, and number of rounds played.
    Player data is saved persistently in a JSON file.
    '''

    def __init__(self, player_name='', score=0, rounds=0):
        self.player_name = player_name
        self.score = score
        self.rounds = rounds

    @classmethod
    def load_players(cls):
        '''Load all players from the JSON file, if it exists.'''
        if os.path.exists(FILENAME):
            with open(FILENAME) as f:
                return json.load(f)
        else:
            return {}

    @classmethod
    def create_player(cls, name):
        '''Create a new player entry and save it to the JSON file.'''
        p = cls(name)
        players = cls.load_players()
        players[name] = {'Score': p.score, 'Rounds': p.rounds}

        with open(FILENAME, 'w') as f:
            json.dump(players, f, indent=4)
        return p

    @classmethod
    def player_exists(cls, name):
        '''Check whether a player name already exists in the database.'''
        players = cls.load_players()
        return name in players

    @classmethod
    def clear_player(cls):
        '''Erase all player data (used when clearing the highscore list).'''
        with open(FILENAME, 'w') as f:
            json.dump({}, f)

    def update_player(self):
        '''Update this player's score and round count in the JSON file.'''
        players = Player.load_players()
        players[self.player_name] = {
            'Score': self.score,
            'Rounds': self.rounds
        }
        with open(FILENAME, 'w') as f:
            json.dump(players, f, indent=4)


class Game:
    '''
    Core Hangman game logic.
    Stores a reference to the Player object so score and rounds can be updated.
    '''

    def __init__(self, player):
        self.player = player

    def get_random_word(self):
        '''Return a random word from a predefined list.'''
        words = [
            'apple', 'banana', 'orange', 'grape', 'pear', 'peach', 'cherry', 
            'lemon', 'lime', 'mango', 'book', 'pen', 'paper', 'notebook', 'pencil', 
            'eraser', 'ruler', 'desk', 'chair', 'lamp', 'dog', 'cat', 'bird', 'fish', 
            'horse', 'cow', 'sheep', 'goat', 'pig', 'rabbit', 'run', 'jump', 'swim', 
            'fly', 'write', 'read', 'draw', 'sing', 'dance', 'play','happy', 'sad', 
            'angry', 'tired', 'excited', 'scared', 'brave', 'funny', 'kind', 'smart',
            'house', 'school', 'office', 'shop', 'park', 'garden', 'street', 'city', 
            'village', 'country', 'car', 'bike', 'bus', 'train', 'plane', 'boat', 
            'truck', 'scooter', 'taxi', 'subway', 'red', 'blue', 'green', 'yellow', 
            'orange', 'purple', 'black', 'white', 'pink', 'brown', 'day', 'night', 
            'morning', 'evening', 'week', 'month', 'year', 'hour', 'minute', 'second',
            'food', 'water', 'milk', 'bread', 'cheese', 'meat', 'rice', 'soup', 
            'fruit', 'vegetable', 'light', 'dark', 'hot', 'cold', 'warm', 'cool', 
            'strong', 'weak', 'big', 'small'
        ]

        return random.choice(words)

    def display_items(self, items, kind='correct'):
        '''
        Display either correct or wrong guessed items using different colors.
        `kind` can be 'correct' or 'wrong'.
        '''

        if kind == 'correct':
            print(GREEN + 'Correct Guesses: ' + ' '.join(items) + RESET + '\n')

        elif kind == 'wrong':
            print(BROWN + 'Wrong Guesses: ' + ' '.join(items) + RESET + '\n')

    def guessed_word(self, word, guessed_letters):
        '''Returns True if the player has guessed all letters of the word.'''
        return all(letter in guessed_letters for letter in word)

    def hangman_stage(self, attempt):
        '''Print the ASCII-art hangman stage depending on the number of
           attempts.'''
        stage = [
            '''
               -----
               |   |
                   |
                   |
                   |
                   |
            =========
            ''',
            '''
               -----
               |   |
               O   |
                   |
                   |
                   |
            =========
            ''',
            '''
               -----
               |   |
               O   |
               |   |
                   |
                   |
            =========
            ''',
            '''
               -----
               |   |
               O   |
              /|   |
                   |
                   |
            =========
            ''',
            '''
               -----
               |   |
               O   |
              /|\\  |
                   |
                   |
            =========
            ''',
            '''
               -----
               |   |
               O   |
              /|\\  |
              /    |
                   |
            =========
            ''',
            '''
               -----
               |   |
               O   |
              /|\\  |
              / \\  |
                   |
            =========
            '''
        ]
        print(stage[attempt])

    def play_game(self):
        '''
        Main game loop.
        Handles guessing, scoring, stages, and ending conditions.
        Returns (True, None) when won, and (False, word) when lost.
        '''

        word = self.get_random_word()
        guessed_letters = ['_'] * len(word)
        wrong_letters = []
        attempt = 0

        while True:

            # Player successfully guessed all letters
            if self.guessed_word(word, guessed_letters):
                self.player.rounds += 1
                self.player.update_player()
                return True, None

            # Player lost after full hangman is drawn
            if attempt == 7:
                self.hangman_stage(attempt-1)
                self.player.update_player()
                return False, word

            guess = input('Enter a letter to guess: ').strip()

            # Duplicate wrong letter
            if guess in wrong_letters:
                print(BROWN + '\nYou have already guessed that letter!\n' + RESET)
                continue

            # Input validation: must be a single alphabetic character
            if len(guess) != 1 or not guess.isalpha():
                print(BROWN + '\nPlease enter exactly one alphabetic character!\n' + RESET)
                continue

            # Correct guess
            if guess in word:
                for i, l in enumerate(word):
                    if l == guess:
                        guessed_letters[i] = guess

                self.player.score += 10
                self.display_items(wrong_letters, 'wrong')
                self.display_items(guessed_letters, 'correct')

            # Wrong guess
            else:
                wrong_letters.append(guess)
                self.hangman_stage(attempt)
                attempt += 1
                self.display_items(wrong_letters, 'wrong')
                self.display_items(guessed_letters, 'correct')


def game_menu():
    '''Print the main menu with ASCII-art design.'''
    print('\n')
    print('<=================== Welcome to Hangman ===================>')
    print(BROWN + r'''
                       _______
                      |       |
                      |       O
                      |      /|\
                      |      / \
                      | ''' + RESET)
    print(BROWN + '         =====================' + RESET + '            \\o/  \\o/  \\o/')
    print(BROWN + '        / | 1. Start Game   | \\' + RESET + '            |    |    |')
    print(BROWN + '       /  | 2. Quit Game    |  \\' + RESET + '          / \\  / \\  / \\')
    print(BROWN + '      /   | 3. Highscores   |   \\' + RESET)
    print(BROWN + '     /   ======================  \\' + RESET + '         \\o/  \\o/  \\o/')
    print('                                            |    |    |')
    print('                                           / \\  / \\  / \\')
    print('\n')
    print('          (Press C to Clear the Highscore List)')
    print('<==========================================================>')


def create_player_ui():
    '''
    Ask the user for a player name.
    Ensures max length and checks if the player already exists.
    '''

    while True:
        name = input('\nEnter Your Name (Max. 15 Letters): ')

        if len(name) > 15:
            print(BROWN + '\nYour name is too long! Try again!\n' + RESET)
            continue

        if Player.player_exists(name):
            print(BROWN + '\nPlayer Already Exists!\n' + RESET)
        else:
            return Player.create_player(name)


def start_game_ui():
    '''Handle the flow for starting and replaying the Hangman game.'''
    player = create_player_ui()
    while True:
        game = Game(player)
        won, word = game.play_game()

        if won:
            print(GREEN + '=================================' + RESET)
            print(GREEN + '=== Congratulations, You won! ===' + RESET)
            print(GREEN + '=================================' + RESET)
        else:
            print(BROWN + '==================' + RESET)
            print(BROWN + '=== Game Over! ===' + RESET)
            print(BROWN + '==================' + RESET)
            print(BROWN + '\nThe Word was: ' + word + RESET)
            break

        again = input('\nPlay Again? (y/n):\n ').lower()
        if again != 'y':
            break


def show_highscores_ui():
    '''Display all saved players with their score and number of rounds.'''
    players = Player.load_players()

    if players == {}:
        print('\n')
        print(BROWN + '========================' + RESET)
        print(BROWN + '===  No Entries Yet  ===' + RESET)
        print(BROWN + '========================' + RESET)
    else:
        print('========== Highscore List =========\n')
        print(BROWN + f'{'Name':<15}{'Score':<10}{'Rounds':<10}' + RESET)
        print(BROWN + '-' * 35 + RESET)

        for name, stats in players.items():
            print(f'{name:<15}{stats['Score']:<10}{stats['Rounds']:<10}')

        print('\n===================================')


def main():
    '''Main application loop for the menu system.'''
    while True:
        game_menu()
        option = input('\nSelect Your Option: ')
        if option == '1':
            start_game_ui()
        elif option == '2':
            break
        elif option == '3':
            show_highscores_ui()
        elif option == 'c':  # Clear highscores
            Player.clear_player()


if __name__ == '__main__':
    main()
