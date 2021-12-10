# ----------------------------------------------------------------------------
# |
# | File:         517925_blackjack.py
# | Author:       Tan Duc Mai
# | Student ID:   517925
# | Description:  Assignment 2 - Implement a card game called Blackjack (21)
# | This is my own work as defined by Eynesbury
# | Academic Misconduct policy.
# |
# ----------------------------------------------------------------------------


# ------------------------------- Module Import -------------------------------
import card_deck


# ---------------------------- Function Definitions ---------------------------
def display_details(filename, author, student_id):
    print(f'File   : {filename}',
          f'Author : {author}',
          f'ID     : {student_id}',
          f'This is my own work as defined by the',
          f'Eynesbury Academic Integrity Policy.',
          sep='\n',
          end='\n\n',
    )



def play_game():
    print("--------- Welcome to Blackjack ---------\n")
    # TODO: Write your game code here


# --------------------------- Call the Main Function --------------------------
if __name__ == '__main__':
    # Start the game.
    play_game()

    # Display the author's details.
    display_details('517925_blackjack.py', 'Tan Duc Mai', '517925')
    print("---------- See you again soon ----------")
