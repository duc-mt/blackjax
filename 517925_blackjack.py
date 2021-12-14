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
    """Display the author's details."""
    print(f'File   : {filename}',
          f'Author : {author}',
          f'ID     : {student_id}',
          f'This is my own work as defined by the',
          f'Eynesbury Academic Integrity Policy.',
          sep='\n',
          end='\n\n')


def input_name():
    """Prompt for, read, and validate the player's name.

    Returns
    -------
    str
        The valid user's input name.
    """
    username = None

    while username is None or ' ' in username or len(username) >= 12:
        username = input('Enter your name: ')
        if ' ' in username or len(username) >= 12:
            print('ERROR: Must be 1 word and less than 12 characters.')
        print()

    return username


def display_hand(player_name, hand):
    """Displays the hand and its total to the screen.

    Parameters
    ----------
    player_name : str
        It is either the user's name or "Dealer".
    hand : list
        The list of cards, either the dealer_hand or player_hand list.

    Returns
    -------
    None
    """
    # Output the hand.
    print(f'{player_name}\'s hand', end=': ')
    i = 0
    for card in hand:
        i += 1
        if i < len(hand):
            print(f'{card[0]} of {card[1]}', end=', ')
        else:
            print(f'{card[0]} of {card[1]}')

    # Output the total value.
    print(f'Hand Total: ({get_hand_total(hand)})', end='\n\n')


def get_hand_total(hand):
    """Take a list of cards and returns the total point value of them.

    Parameters
    ----------
    str
        The cards drawn.

    Returns
    -------
    int
        The total point value of all card values in the 'hand'.
    """
    # Variable initialisation.
    point = 0
    count_ace = 0

    # Add the value of cards.
    for card in hand:
        if card[0] == 'Ace':
            count_ace += 1
        elif card[0] in ['Jack', 'Queen', 'King']:
            point += 10
        else:
            point += int(card[0])

    # Determine the value of Ace cards.
    if (point + 11*count_ace) <= 21:
        point += 11*count_ace
    else:
        point += 1*count_ace

    return point


def input_hit_choice():
    """Prompt for, read, and validate the user's choice.

    Returns
    -------
    str
        The valid user choice which is either 'h' (hit) or 's' (stand).
    """
    choice = None
    valid_choices = ['h', 's']

    while choice is None or choice not in valid_choices:
        choice = input('Do you want to hit or stand (h/s): ')
        if choice not in valid_choices:
            print("ERROR: Must be 'h' or 's'.")
    print()

    return choice


def player_play(name, hand):
    """
      Continue to draw cards until the user responds
      's' (stand) or their cards' total exceeds 21.

    Parameters
    ----------
    name : str
        The player's name.
    hand : list
        The list of cards drawn by the player.

    Returns
    -------
    None
    """
    user_hit = None

    while user_hit is None or (user_hit == 'h' and get_hand_total(hand) < 21):
        user_hit = input_hit_choice()

        if user_hit == 'h':
            # Draw another card.
            hand.append(card_deck.draw_card())
            # Output the total value.
            display_hand(name, hand)

    return get_hand_total(hand)


def dealer_play(hand):
    """Continue to draw cards until the dealer's cards' total reaches 17.

    Parameters
    ----------
    list
        The list of cards drawn by the dealer.

    Returns
    -------
    None
    """
    dealer_hit = None

    while dealer_hit is None or (dealer_hit == '' and get_hand_total(hand) < 17):
        # Draw another card.
        hand.append(card_deck.draw_card())
        # Output the total value.
        display_hand('Dealer', hand)

        dealer_hit = input('Press "Enter" to continue...')
        print()

    return get_hand_total(hand)


def add_score(name, score, filename):
    """Read the file to check if (score) is greater than the others in the file.

    Parameters
    ----------
    name : str
        The player's name
    score : int
        The player's score, calculated by [won/(games-tied)*100].
    filename : str
        The name of the text file containing two players' names and their scores.

    Returns
    -------
    None
    """
    """This program removes any blank line present in the file (if any)."""
    with open('highscores.txt') as check_blank_infile:
        # ----- Reading ----- #
        line_list = check_blank_infile.readlines()

        # ----- Writing ----- #
        if '' in line_list or '\n' in line_list:
            with open('highscores.txt', 'w') as removed_blank_outfile:
                for line in line_list:
                    if line and line != '\n':
                        removed_blank_outfile.write(line)

    """This program adds/appends the new score to highscores.txt file."""
    with open('highscores.txt') as infile:
        # This checks if player's score is greater than those of other.
        is_new_highscore = True

        # Read the contents of the file into a list.
        line_list = infile.readlines()

        """Change {line_list}'s format to [['Tiffany', 37.500], ['Mike', 0.667]]."""
        for index in range(len(line_list)):
            # Strip \n from each element.
            # Split the name and the score into two sub-lists.
            line_list[index] = line_list[index].rstrip().split()
            # Convert the score part into a float.
            line_list[index][1] = float(line_list[index][1])

        """Compare player's score with those of the others in highscores.txt file."""
        for line in line_list:
            if line[1] > score:
                is_new_highscore = False

        # Adjust the score to 3 decimal points.
        score = f'{score:.3f}'

        if is_new_highscore:
            """This program adds the new high score to the first line."""
            with open('highscores.txt', 'w') as write_outfile:
                # This serves as a flag indicating whether to continue printing.
                # Become False when hitting the line of Mike.
                continue_print = True

                # Adjust the high score to 3 decimal points and write it to file.
                write_outfile.write(f'{name} {score}\n')

                # Display the first three lines, the third one is the high score.
                print(f'New High Score!' + '\n',
                      f'NAME\tSCORE',
                      f'{name}\t{score}',
                      sep='\n')

                # As for the rest scores.
                for current_index, current_line in enumerate(line_list):
                    # Adjust them to 3 decimal points and write them to file.
                    score = f'{current_line[1]:.3f}'
                    write_outfile.write(f'{current_line[0]} {score}\n')
                    # Do not display names that are below Mike.
                    # Indicated by continue_print = False.
                    if continue_print:
                        print(f'{current_line[0]}\t{score}')
                    if current_line == ['Mike', 0.667]:
                        continue_print = False

        else:
            """This program appends the score (not a high score) to the file."""
            with open('highscores.txt', 'a') as append_outfile:
                append_outfile.write(f'{name} {score}\n')


def play_game():
    print("--------- Welcome to Blackjack ---------\n")

    # Display the author's details.
    display_details('517925_blackjack.py', 'Tan Duc Mai', '517925')

    # Variable initialisation.
    valid_answers = ['y', 'n']
    games = 0
    dealer_hand = []
    player_hand = []
    won = 0
    lost = 0
    tied = 0

    # Ask to play.
    play = None
    while play is None or play not in valid_answers:
        play = input('Do you want to play blackjack (y/n): ')
        if play not in valid_answers:
            print("ERROR: Only enter 'y' or 'n'")

    # Start the game once the user responds 'y'.
    if play == valid_answers[0]:
        name = input_name()

        while play == valid_answers[0]:
            games += 1

            # Draw cards.
            dealer_hand.append(card_deck.draw_card())

            for _ in range(2):
                player_hand.append(card_deck.draw_card())

            # Display hands.
            display_hand('Dealer', dealer_hand)
            display_hand(name, player_hand)

            # Check for Blackjack.
            dealer_point = get_hand_total(dealer_hand)
            player_point = get_hand_total(player_hand)
            count_21 = [dealer_point, player_point].count(21)

            if count_21 == 0:
                # Determine the winner.
                player_point = player_play(name, player_hand)
                dealer_point = dealer_play(dealer_hand)

                if dealer_point == player_point:
                    print(f'Dealer: {dealer_point}\t{name}: {player_point}',
                          f'Push!',
                          sep='  ->  ')
                    tied += 1
                elif (dealer_point > player_point and dealer_point <= 21) or player_point > 21:
                    if player_point > 21:
                        print(f'{name} bust!')
                    print(f'Dealer: {dealer_point}\t{name}: {player_point}',
                          f'Dealer wins!',
                          sep='  ->  ')
                    lost += 1
                elif (player_point > dealer_point and player_point <= 21) or dealer_point > 21:
                    if dealer_point > 21:
                        print(f'Dealer bust!')
                    print(f'Dealer: {dealer_point}\t{name}: {player_point}',
                          f'{name} wins!',
                          sep='  ->  ')
                    won += 1

            elif count_21 == 2:
                print('Two player blackjack!-> Push!')
                tied += 1

            else:
                print('Blackjack', end='! ')
                if dealer_point == 21:
                    print('Dealer wins!')
                    lost += 1
                else:
                    print(f'{name} wins!')
                    won += 1

            # A line separating each game.
            print(f"\n{'-' * 40}\n")

            # Reset the card once a game is complete.
            dealer_hand = []
            player_hand = []

            # Ask to play again.
            again = None
            while again is None or again not in valid_answers:
                again = input('Do you want to play again (y/n): ')
                if again not in valid_answers:
                    print("ERROR: Only enter 'y' or 'n'")
            play = again
            print()

        # Summary.
        print(f'You played {games} games.',
              f' -> Won:    {won}',
              f' -> Lost:   {lost}',
              f' -> Tied:   {tied}',
              sep='\n',
              end='\n\n')

        # Check for high scores.
        try:
            player_score = (won / (games - tied)) * 100
            if player_score:
                add_score(name, player_score, 'highscores.txt')
        except ZeroDivisionError as err:
            print(f'ERROR: {err} because the number of games ({games}) ',
                  f'is equal to to the number of tied ({tied}).')

        print('\nThanks for playing!', end='\n\n')

    else:
        print('Maybe next time...', end='\n\n')


# --------------------------- Call the Main Function --------------------------
if __name__ == '__main__':
    play_game()
    print("---------- See you again soon ----------")
