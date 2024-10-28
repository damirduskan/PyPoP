import requests
import random


# ------------------ Blackjack Game ------------------

class BlackjackGame:
    def __init__(self):
        """
        Initialize the Blackjack game with a shuffled deck and initial chips.
        """
        self.base_url = "https://deckofcardsapi.com/api/deck/"
        self.deck_id = self.shuffle_new_deck()  # Get a new shuffled deck ID from the API
        self.player_hand = []  # List to hold the player's cards
        self.dealer_hand = []  # List to hold the dealer's cards
        self.chips = 1000  # Starting chips for the player

    def shuffle_new_deck(self):
        """
        Shuffle a new deck with 6 decks combined and return the deck_id.
        """
        # Send a request to shuffle a deck with 6 combined decks using the API
        response = requests.get(f"{self.base_url}new/shuffle/?deck_count=6")
        deck_data = response.json()  # Convert response to JSON format
        return deck_data['deck_id']  # Return the unique deck ID

    def draw_card(self, count=1):
        """
        Draw a specified number of cards from the deck.
        """
        # Send a request to draw a specific number of cards from the current deck
        response = requests.get(f"{self.base_url}{self.deck_id}/draw/?count={count}")
        return response.json()['cards']  # Return the drawn cards as a list

    def card_value(self, card):
        """
        Calculate the value of a single card (handle face cards and Ace).
        """
        value = card['value']  # Get the card value (e.g., '5', 'KING', 'ACE')
        if value in ['JACK', 'QUEEN', 'KING']:
            return 10  # Face cards are worth 10 points
        elif value == 'ACE':
            return 11  # Treat ACE as 11 initially (can be adjusted later)
        else:
            return int(value)  # Convert number cards to their integer value

    def calculate_hand(self, hand):
        """
        Calculate the total value of a hand of cards, adjusting for Aces if necessary.
        """
        total = sum([self.card_value(card) for card in hand])  # Calculate the total value of the hand
        aces = sum(1 for card in hand if card['value'] == 'ACE')  # Count the number of Aces in the hand

        # Adjust the total if there are Aces and the total is greater than 21
        while total > 21 and aces:
            total -= 10  # Reduce the value of an Ace from 11 to 1
            aces -= 1  # Decrease the count of Aces

        return total  # Return the adjusted total value

    def show_hand(self, hand, owner="Player"):
        """
        Display the hand of a player or dealer.
        """
        # Create a string representation of the hand with card values and suits
        cards = ", ".join([f"{card['value']} of {card['suit']}" for card in hand])
        total = self.calculate_hand(hand)  # Calculate the total points of the hand
        print(f"{owner}'s hand: {cards} (Total: {total})")  # Print the hand

    def place_bet(self):
        """
        Allow the player to place a bet and validate the amount.
        """
        while True:
            print(f"You have {self.chips} chips.")  # Display the player's current chip count
            try:
                bet = int(input("Place your bet: "))  # Ask the player to enter a bet amount
                # Check if the bet is valid (greater than zero and within available chips)
                if bet > self.chips or bet <= 0:
                    print("Invalid bet amount. Try again.")
                else:
                    return bet  # Return the valid bet amount
            except ValueError:
                print("Please enter a valid number.")  # Handle non-numeric inputs

    def player_turn(self):
        """
        Handle the player's turn to either hit or stand.
        """
        while True:
            self.show_hand(self.player_hand, "Player")  # Display the player's current hand
            action = input("Do you want to 'hit' or 'stand'? ").lower()  # Ask for the player's action
            if action == 'hit':
                # Draw a card and add it to the player's hand
                self.player_hand += self.draw_card(1)
                if self.calculate_hand(self.player_hand) > 21:
                    self.show_hand(self.player_hand, "Player")  # Show the hand after hitting
                    print("Bust! You've gone over 21.")  # Inform player of the bust
                    return False  # End player's turn due to bust
            elif action == 'stand':
                return True  # Player decides to stand and end their turn
            else:
                print("Invalid action. Please choose 'hit' or 'stand'.")  # Handle invalid actions

    def dealer_turn(self):
        """
        Handle the dealer's turn, hitting until the total is at least 17.
        """
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand += self.draw_card(1)  # Draw a card for the dealer if under 17

    def determine_winner(self, bet):
        """
        Determine the winner between player and dealer and adjust chips.
        """
        player_total = self.calculate_hand(self.player_hand)  # Calculate player's total points
        dealer_total = self.calculate_hand(self.dealer_hand)  # Calculate dealer's total points

        self.show_hand(self.dealer_hand, "Dealer")  # Show the dealer's full hand

        # Determine the game outcome and adjust chips based on the result
        if dealer_total > 21:
            print("Dealer busts! You win!")  # Dealer busts, player wins
            self.chips += bet  # Add the bet amount to player's chips
        elif player_total > dealer_total:
            print("Congratulations, you win!")  # Player has a higher score, wins
            self.chips += bet  # Add the bet amount to player's chips
        elif player_total < dealer_total:
            print("Dealer wins. Better luck next time.")  # Dealer has a higher score, wins
            self.chips -= bet  # Subtract the bet amount from player's chips
        else:
            print("It's a tie!")  # Scores are equal, it's a tie

    def play(self):
        """
        Play the Blackjack game, allowing the player to bet and take turns.
        """
        print("Welcome to Blackjack!")  # Greet the player
        while self.chips > 0:  # Continue playing as long as the player has chips
            bet = self.place_bet()  # Place a bet for the round
            # Initial card draws for player and dealer
            self.player_hand = self.draw_card(2)  # Draw two cards for the player
            self.dealer_hand = self.draw_card(2)  # Draw two cards for the dealer
            # Show the dealer's first card (one card face up)
            print(f"Dealer's first card: {self.dealer_hand[0]['value']} of {self.dealer_hand[0]['suit']}")

            # Player's turn to hit or stand
            if self.player_turn():
                self.dealer_turn()  # Dealer's turn if the player didn't bust

            # Determine the winner of the round
            self.determine_winner(bet)

            # Check if the player wants to continue playing
            if self.chips <= 0:
                print("You're out of chips! Game over.")  # Player is out of chips
                break
            else:
                # Ask the player if they want to play another round
                play_again = input("Do you want to play another round? (yes/no): ").lower()
                if play_again != 'yes':
                    print(f"You left the game with {self.chips} chips. Goodbye!")  # End the game
                    break

# ------------------ Slot Machine ------------------

class SlotMachine:
    def __init__(self):
        """
        Initialize the slot machine with symbols, their values, and starting chips.
        """
        # Define the list of emoji symbols that represent the slot machine symbols
        self.emojis = ["🍒", "🍋", "🍊", "🍉", "🍇", "⭐", "🔔", "🍀", "💎", "👑"]

        # Define the payout values for each emoji symbol when three match in a row
        self.values = {
            "🍒": 10,  # Payout for three Cherries
            "🍋": 20,  # Payout for three Lemons
            "🍊": 30,  # Payout for three Oranges
            "🍉": 50,  # Payout for three Watermelons
            "🍇": 75,  # Payout for three Grapes
            "⭐": 100,  # Payout for three Stars
            "🔔": 150, # Payout for three Bells
            "🍀": 200, # Payout for three Four-leaf Clovers
            "💎": 300, # Payout for three Diamonds
            "👑": 500  # Payout for three Crowns
        }

        # Starting chips for the player
        self.chips = 500

    def spin(self):
        """
        Simulate a spin of the slot machine by randomly selecting three emojis.
        """
        # Randomly select three symbols from the emoji list (with replacement)
        result = random.choices(self.emojis, k=3)
        return result  # Return the result of the spin as a list of three emojis

    def calculate_payout(self, result, bet):
        """
        Calculate the payout based on the result of the spin.
        """
        # Check if all three symbols in the result are the same
        if result[0] == result[1] == result[2]:
            # Calculate the payout by multiplying the value of the matching symbol by the bet amount
            payout = self.values[result[0]] * bet
            return payout  # Return the calculated payout amount
        else:
            return 0  # Return zero if symbols do not match

    def place_bet(self):
        """
        Allow the player to place a bet and validate the amount.
        """
        while True:
            print(f"You have {self.chips} chips.")  # Display the player's current chip count
            try:
                # Prompt the player to enter a bet amount
                bet = int(input("Place your bet: "))
                # Check if the bet amount is valid (greater than zero and within available chips)
                if bet > self.chips or bet <= 0:
                    print("Invalid bet amount. Try again.")
                else:
                    return bet  # Return the valid bet amount
            except ValueError:
                print("Please enter a valid number.")  # Handle non-numeric inputs

    def play(self):
        """
        Play the slot machine game, allowing the player to bet and spin.
        """
        print("Welcome to the Slot Machine!")  # Greet the player
        while self.chips > 0:  # Continue playing as long as the player has chips
            # Place a bet for the spin
            bet = self.place_bet()

            # Spin the slot machine to get a random result
            result = self.spin()
            # Display the result of the spin
            print(f"Result: {' | '.join(result)}")

            # Calculate the payout based on the result of the spin
            payout = self.calculate_payout(result, bet)
            if payout > 0:
                # If there is a payout, inform the player and add the payout to their chips
                print(f"Congratulations! You won {payout} chips!")
                self.chips += payout
            else:
                # If there is no payout, inform the player and subtract the bet from their chips
                print("Sorry, you didn't win this time.")
                self.chips -= bet

            # Check if the player still has chips to continue playing
            if self.chips <= 0:
                print("You're out of chips! Game over.")  # End the game if chips run out
                break
            else:
                # Ask the player if they want to play another spin
                play_again = input("Do you want to play another spin? (yes/no): ").lower()
                if play_again != 'yes':
                    # If the player chooses not to play, display their final chip count and exit the game
                    print(f"You left the game with {self.chips} chips. Goodbye!")
                    break

# ------------------ Roulette Game ------------------

class RouletteGame:
    def __init__(self):
        """
        Initialize the Roulette game with starting chips and sets of red/black numbers.
        """
        # Set the starting chips for the player
        self.chips = 1000

        # Define the sets of numbers that are considered red and black
        self.red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        self.black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

    def spin_wheel(self):
        """
        Simulate a spin of the roulette wheel.
        """
        # Return a random number between 0 and 36, inclusive, to simulate the wheel spin
        return random.randint(0, 36)

    def place_bet(self):
        """
        Allow the player to place a bet and validate the amount.
        """
        while True:
            print(f"You have {self.chips} chips.")  # Display the player's current chip count
            try:
                # Prompt the player to enter a bet amount
                bet = int(input("Place your bet amount: "))
                # Check if the bet amount is valid (greater than zero and within available chips)
                if bet > self.chips or bet <= 0:
                    print("Invalid bet amount. Try again.")
                else:
                    return bet  # Return the valid bet amount
            except ValueError:
                print("Please enter a valid number.")  # Handle non-numeric inputs

    def choose_bet_type(self):
        """
        Display the list of bet types and allow the player to choose one.
        """
        # Display the available types of bets in Roulette
        print("\nBet Types:")
        print("1: Straight Bet (bet on a single number, 35:1 payout)")
        print("2: Color Bet (bet on Red or Black, 1:1 payout)")
        print("3: Odd/Even Bet (bet on Odd or Even numbers, 1:1 payout)")
        print("4: Low/High Bet (bet on Low 1-18 or High 19-36, 1:1 payout)")

        # Loop until the player selects a valid bet type
        while True:
            try:
                # Prompt the player to choose a bet type by entering a number (1-4)
                choice = int(input("Choose a bet type (1-4): "))
                if choice in [1, 2, 3, 4]:
                    return choice  # Return the valid bet type choice
                else:
                    print("Invalid choice. Please choose a valid bet type.")
            except ValueError:
                print("Please enter a number between 1 and 4.")  # Handle non-numeric inputs

    def get_bet_details(self, choice):
        """
        Get the specific details for the selected bet type.
        """
        if choice == 1:
            # Straight Bet: Choose a single number between 0 and 36
            while True:
                try:
                    # Prompt the player to enter a number to bet on
                    number = int(input("Enter a number to bet on (0-36): "))
                    if 0 <= number <= 36:
                        return {"type": "straight", "number": number}  # Return the bet details
                    else:
                        print("Invalid number. Please choose a number between 0 and 36.")
                except ValueError:
                    print("Please enter a valid number.")  # Handle non-numeric inputs

        elif choice == 2:
            # Color Bet: Choose Red or Black
            color = input("Enter 'red' or 'black': ").lower()  # Prompt for color choice
            if color in ["red", "black"]:
                return {"type": "color", "color": color}  # Return the bet details
            else:
                print("Invalid color. Please choose 'red' or 'black'.")
                return self.get_bet_details(choice)  # Retry if invalid input

        elif choice == 3:
            # Odd/Even Bet: Choose Odd or Even
            odd_even = input("Enter 'odd' or 'even': ").lower()  # Prompt for odd/even choice
            if odd_even in ["odd", "even"]:
                return {"type": "odd_even", "odd_even": odd_even}  # Return the bet details
            else:
                print("Invalid choice. Please choose 'odd' or 'even'.")
                return self.get_bet_details(choice)  # Retry if invalid input

        elif choice == 4:
            # Low/High Bet: Choose Low (1-18) or High (19-36)
            low_high = input("Enter 'low' (1-18) or 'high' (19-36): ").lower()  # Prompt for low/high choice
            if low_high in ["low", "high"]:
                return {"type": "low_high", "low_high": low_high}  # Return the bet details
            else:
                print("Invalid choice. Please choose 'low' or 'high'.")
                return self.get_bet_details(choice)  # Retry if invalid input

    def determine_payout(self, result, bet_details, bet_amount):
        """
        Determine the payout based on the result and the bet placed.
        """
        # Check if the bet is a straight bet and if the number matches the result
        if bet_details["type"] == "straight":
            if result == bet_details["number"]:
                return bet_amount * 35  # Payout for straight bet (35:1)

        # Check if the bet is a color bet and if the result matches the chosen color
        elif bet_details["type"] == "color":
            if (bet_details["color"] == "red" and result in self.red_numbers) or \
               (bet_details["color"] == "black" and result in self.black_numbers):
                return bet_amount  # Payout for color bet (1:1)

        # Check if the bet is an odd/even bet and if the result matches the choice
        elif bet_details["type"] == "odd_even":
            if (bet_details["odd_even"] == "odd" and result % 2 != 0 and result != 0) or \
               (bet_details["odd_even"] == "even" and result % 2 == 0 and result != 0):
                return bet_amount  # Payout for odd/even bet (1:1)

        # Check if the bet is a low/high bet and if the result falls within the chosen range
        elif bet_details["type"] == "low_high":
            if (bet_details["low_high"] == "low" and 1 <= result <= 18) or \
               (bet_details["low_high"] == "high" and 19 <= result <= 36):
                return bet_amount  # Payout for low/high bet (1:1)

        # If no winning condition is met, return a negative payout equal to the bet amount
        return -bet_amount

    def play(self):
        """
        Play the Roulette game, allowing the player to place and resolve bets.
        """
        print("Welcome to the Roulette Game!")  # Greet the player
        while self.chips > 0:  # Continue playing as long as the player has chips
            # Place a bet for the round
            bet_amount = self.place_bet()

            # Choose the type of bet and get the bet details
            bet_type = self.choose_bet_type()
            bet_details = self.get_bet_details(bet_type)

            # Spin the roulette wheel to get the result
            result = self.spin_wheel()
            print(f"\nThe ball landed on: {result}")  # Display the result of the spin

            # Determine the payout based on the result and bet details
            payout = self.determine_payout(result, bet_details, bet_amount)

            # Adjust the player's chips based on the payout
            if payout > 0:
                print(f"Congratulations! You won {payout} chips!")
                self.chips += payout  # Add the payout to the player's chips
            else:
                print("Sorry, you lost.")
                self.chips += payout  # Subtract the bet amount from the player's chips (payout is negative)

            # Show the player's current chip balance
            print(f"You have {self.chips} chips remaining.")

            # Ask if the player wants to continue playing
            if self.chips <= 0:
                print("You're out of chips! Game over.")  # End the game if chips run out
                break
            else:
                # Prompt the player to continue or quit the game
                play_again = input("Do you want to play another round? (yes/no): ").lower()
                if play_again != 'yes':
                    print(f"You left the game with {self.chips} chips. Goodbye!")  # Display final chips and exit
                    break

# ------------------ Texas Hold'em Poker ------------------

class TexasHoldemPoker:
    def __init__(self):
        """
        Initialize the Texas Hold'em Poker game with a shuffled deck and initial chips.
        """
        self.base_url = "https://deckofcardsapi.com/api/deck/"
        self.deck_id = self.get_new_deck()  # Get a new shuffled deck ID
        self.community_cards = []  # Cards on the table
        self.players = {
            "Player 1": {"hand": [], "chips": 1000, "current_bet": 0, "folded": False},
            "Player 2": {"hand": [], "chips": 1000, "current_bet": 0, "folded": False}
        }
        self.pot = 0  # Initialize the pot

    def get_new_deck(self):
        """Get a new shuffled deck using the API."""
        response = requests.get(f"{self.base_url}new/shuffle/?deck_count=1")
        deck_data = response.json()
        return deck_data['deck_id']

    def draw_cards(self, count=1):
        """Draw a specified number of cards from the deck."""
        response = requests.get(f"{self.base_url}{self.deck_id}/draw/?count={count}")
        return response.json()['cards']

    def deal_hole_cards(self):
        """Deal two cards to each player."""
        for player in self.players:
            self.players[player]["hand"] = self.draw_cards(2)

    def deal_flop(self):
        """Deal the Flop (3 community cards)."""
        self.community_cards = self.draw_cards(3)

    def deal_turn(self):
        """Deal the Turn (1 additional community card)."""
        self.community_cards += self.draw_cards(1)

    def deal_river(self):
        """Deal the River (1 additional community card)."""
        self.community_cards += self.draw_cards(1)

    def display_cards(self):
        """Display the players' hands and community cards."""
        for player, details in self.players.items():
            if not details["folded"]:
                hand = details["hand"]
                print(f"{player} hand: {', '.join([f'{card['value']} of {card['suit']}' for card in hand])}")
        print(f"Community cards: {', '.join([f'{card['value']} of {card['suit']}' for card in self.community_cards])}")

    def get_card_value(self, card):
        """Convert card values to numeric values for comparison."""
        if card['value'] in ['JACK', 'QUEEN', 'KING']:
            return 10
        elif card['value'] == 'ACE':
            return 11
        else:
            return int(card['value'])

    def compare_hands(self):
        """A simplified comparison of hands based on the highest card value."""
        best_hands = {}

        # Calculate the best hand for each player who has not folded
        for player, details in self.players.items():
            if details["folded"]:
                continue
            combined_hand = details["hand"] + self.community_cards
            hand_values = [self.get_card_value(card) for card in combined_hand]
            best_hand_value = max(hand_values)
            best_hands[player] = best_hand_value

        # Determine the winner from the best hands
        if not best_hands:
            print("All players folded. No winner.")
            return

        winner = max(best_hands, key=best_hands.get)
        print(f"{winner} wins the pot of {self.pot} chips!")
        self.players[winner]["chips"] += self.pot
        self.pot = 0  # Reset the pot after determining the winner

    def betting_round(self):
        """Conduct a betting round where both players can bet, call, raise, or fold."""
        # Reset current bets for both players and initialize highest bet
        for player in self.players:
            self.players[player]["current_bet"] = 0

        highest_bet = 0  # Track the highest bet placed in this round

        # Loop through each player to take betting actions
        for player, details in self.players.items():
            if details["chips"] <= 0:
                print(f"{player} is out of chips and cannot bet.")
                continue

            if details["folded"]:
                continue

            print(f"\n{player}'s turn. You have {details['chips']} chips.")
            while True:
                action = input("Do you want to 'call', 'raise', or 'fold'? ").lower()
                if action == "call":
                    call_amount = highest_bet - details["current_bet"]
                    if details["chips"] >= call_amount:
                        # Player calls the current highest bet
                        self.pot += call_amount
                        details["chips"] -= call_amount
                        details["current_bet"] += call_amount
                        print(f"{player} calls {call_amount}.")
                    else:
                        # Player goes all in if they cannot match the full call amount
                        self.pot += details["chips"]
                        details["current_bet"] += details["chips"]
                        details["chips"] = 0
                        print(f"{player} goes all in with {details['current_bet']}.")
                    break

                elif action == "raise":
                    # Player raises; prompt for raise amount
                    raise_amount = int(input("Enter the amount you want to raise: "))
                    if raise_amount + highest_bet > details["chips"]:
                        print("You do not have enough chips to raise that amount.")
                    else:
                        self.pot += (raise_amount + highest_bet - details["current_bet"])
                        details["chips"] -= (raise_amount + highest_bet - details["current_bet"])
                        details["current_bet"] = raise_amount + highest_bet
                        highest_bet = details["current_bet"]
                        print(f"{player} raises to {highest_bet}.")
                        break

                elif action == "fold":
                    # Player folds and forfeits the round
                    print(f"{player} folds.")
                    details["folded"] = True
                    break

                else:
                    print("Invalid action. Please choose 'call', 'raise', or 'fold'.")

    def play(self):
        """Play a simplified game of Texas Hold'em Poker with betting."""
        print("Welcome to Texas Hold'em Poker!")

        # Deal hole cards to players
        self.deal_hole_cards()
        print("\nDealing hole cards...")
        self.display_cards()

        # Pre-flop betting round
        print("\nPre-flop betting round:")
        self.betting_round()

        # Deal the Flop if players are still in the game
        if not all(player["folded"] for player in self.players.values()):
            print("\nDealing the Flop...")
            self.deal_flop()
            self.display_cards()

            # Post-flop betting round
            print("\nPost-flop betting round:")
            self.betting_round()

        # Deal the Turn if players are still in the game
        if not all(player["folded"] for player in self.players.values()):
            print("\nDealing the Turn...")
            self.deal_turn()
            self.display_cards()

            # Post-turn betting round
            print("\nPost-turn betting round:")
            self.betting_round()

        # Deal the River if players are still in the game
        if not all(player["folded"] for player in self.players.values()):
            print("\nDealing the River...")
            self.deal_river()
            self.display_cards()

            # Post-river betting round
            print("\nPost-river betting round:")
            self.betting_round()

        # Determine the winner after all community cards are dealt and betting is complete
        if not all(player["folded"] for player in self.players.values()):
            print("\nComparing hands...")
            self.compare_hands()

        # Display the final chip counts for each player after the round ends
        for player, details in self.players.items():
            print(f"{player} has {details['chips']} chips remaining.")
        print(f"The pot is now empty.")


def get_weather(city, api_key):
    """
    Get weather updates for the input city using OpenWeather API.
    """
    # Define the base URL for the OpenWeather API request
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Define the parameters for the request, including the city name, API key, and units
    params = {
        "q": city,             # City for which the weather is to be fetched
        "appid": api_key,      # API key for authentication with OpenWeather API
        "units": "metric"      # Use metric units for temperature (Celsius)
    }

    # Make a GET request to the OpenWeather API with the specified parameters
    response = requests.get(base_url, params=params)

    # Check if the response status code indicates a successful request (status code 200)
    if response.status_code == 200:
        data = response.json()  # Parse the response data as JSON format

        # Extract the weather description and temperature from the JSON data
        weather = data['weather'][0]['description']  # Extract the weather description (e.g., "clear sky")
        temperature = data['main']['temp']           # Extract the temperature in Celsius

        # Print the weather information to the user
        print(f"Weather in {city}: {weather}")
        print(f"Temperature: {temperature}°C")
    else:
        # If the response is not successful, inform the user that the city was not found or the API key was invalid
        print("City not found or invalid API key.")


# ------------------ Casino Main Menu ------------------

def casino_main():
    """Provide the main menu for the Casino app, allowing users to select games or get weather updates."""
    api_key = "3ec4b3e19cbdab67be6758473d061f41"  # OpenWeather API key
    while True:
        print("\nWelcome to the Casino!")
        print("1. Play Blackjack")
        print("2. Play Slot Machine")
        print("3. Play Roulette")
        print("4. Play Texas Hold'em Poker")
        print("5. Get Weather Updates")
        print("6. Leave the Casino (Quit)")

        choice = input("Please choose an option (1-6): ")

        if choice == "1":
            print("\nStarting Blackjack...")
            game = BlackjackGame()
            game.play()

        elif choice == "2":
            print("\nStarting Slot Machine...")
            game = SlotMachine()
            game.play()

        elif choice == "3":
            print("\nStarting Roulette...")
            game = RouletteGame()
            game.play()

        elif choice == "4":
            print("\nStarting Texas Hold'em Poker...")
            game = TexasHoldemPoker()
            game.play()

        elif choice == "5":
            city = input("Enter the city name: ")
            get_weather(city, api_key)

        elif choice == "6":
            print("Thank you for visiting the Casino! Goodbye!")
            break

        else:
            print("Invalid choice. Please choose a number between 1 and 6.")


# ------------------ Run the Casino App ------------------

if __name__ == "__main__":
    casino_main()
