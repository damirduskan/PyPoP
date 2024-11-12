import requests
import random


# ------------------ Blackjack Game ------------------

class BlackjackGame:
    def __init__(self):
        """
        Initialize the Blackjack game with a shuffled deck and initial chips.
        """
        self.base_url = "https://deckofcardsapi.com/api/deck/"
        self.deck_id = self.shuffle_new_deck()  # Get a new shuffled deck ID
        self.player_hand = []  # List to hold player's cards
        self.dealer_hand = []  # List to hold dealer's cards
        self.chips = 1000  # Starting chips for the player

    def shuffle_new_deck(self):
        """
        Shuffle a new deck with 6 decks combined and return the deck_id.
        """
        response = requests.get(f"{self.base_url}new/shuffle/?deck_count=6")
        deck_data = response.json()
        return deck_data['deck_id']

    def draw_card(self, count=1):
        """
        Draw a specified number of cards from the deck.
        """
        response = requests.get(f"{self.base_url}{self.deck_id}/draw/?count={count}")
        return response.json()['cards']

    def card_value(self, card):
        """
        Calculate the value of a single card (handle face cards and Ace).
        """
        value = card['value']
        if value in ['JACK', 'QUEEN', 'KING']:
            return 10
        elif value == 'ACE':
            return 11  # Treat ACE as 11 initially
        else:
            return int(value)

    def calculate_hand(self, hand):
        """
        Calculate the total value of a hand of cards, adjusting for Aces if necessary.
        """
        total = sum([self.card_value(card) for card in hand])
        aces = sum(1 for card in hand if card['value'] == 'ACE')

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def show_hand(self, hand, owner="Player"):
        """
        Display the hand of a player or dealer.
        """
        cards = ", ".join([f"{card['value']} of {card['suit']}" for card in hand])
        total = self.calculate_hand(hand)
        print(f"{owner}'s hand: {cards} (Total: {total})")

    def place_bet(self):
        """
        Allow the player to place a bet and validate the amount.
        """
        while True:
            print(f"You have {self.chips} chips.")
            try:
                bet = int(input("Place your bet: "))
                if bet > self.chips or bet <= 0:
                    print("Invalid bet amount. Try again.")
                else:
                    return bet
            except ValueError:
                print("Please enter a valid number.")

    def player_turn(self):
        """
        Handle the player's turn to either hit or stand.
        """
        while True:
            self.show_hand(self.player_hand, "Player")
            action = input("Do you want to 'hit' or 'stand'? ").lower()
            if action == 'hit':
                self.player_hand += self.draw_card(1)
                if self.calculate_hand(self.player_hand) > 21:
                    self.show_hand(self.player_hand, "Player")
                    print("Bust! You've gone over 21.")
                    return False
            elif action == 'stand':
                return True
            else:
                print("Invalid action. Please choose 'hit' or 'stand'.")

    def dealer_turn(self):
        """
        Handle the dealer's turn, hitting until the total is at least 17.
        """
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand += self.draw_card(1)

    def determine_winner(self, bet):
        """
        Determine the winner between player and dealer and adjust chips.
        """
        player_total = self.calculate_hand(self.player_hand)
        dealer_total = self.calculate_hand(self.dealer_hand)

        self.show_hand(self.dealer_hand, "Dealer")

        if dealer_total > 21:
            print("Dealer busts! You win!")
            self.chips += bet
        elif player_total > dealer_total:
            print("Congratulations, you win!")
            self.chips += bet
        elif player_total < dealer_total:
            print("Dealer wins. Better luck next time.")
            self.chips -= bet
        else:
            print("It's a tie!")

    def play(self):
        """
        Play the Blackjack game, allowing the player to bet and take turns.
        """
        print("Welcome to Blackjack!")
        while self.chips > 0:
            bet = self.place_bet()
            self.player_hand = self.draw_card(2)
            self.dealer_hand = self.draw_card(2)
            print(f"Dealer's first card: {self.dealer_hand[0]['value']} of {self.dealer_hand[0]['suit']}")

            if self.player_turn():
                self.dealer_turn()

            self.determine_winner(bet)

            if self.chips <= 0:
                print("You're out of chips! Game over.")
                break
            else:
                play_again = input("Do you want to play another round? (yes/no): ").lower()
                if play_again != 'yes':
                    print(f"You left the game with {self.chips} chips. Goodbye!")
                    break

# ------------------ Slot Machine Game ------------------

class SlotMachine:
    def __init__(self):
        """
        Initialize the slot machine with symbols, their values, and starting chips.
        """
        self.emojis = ["🍒", "🍋", "🍊", "🍉", "🍇", "⭐", "🔔", "🍀", "💎", "👑"]
        self.values = {
            "🍒": 10, "🍋": 20, "🍊": 30, "🍉": 50,
            "🍇": 75, "⭐": 100, "🔔": 150, "🍀": 200,
            "💎": 300, "👑": 500
        }
        self.chips = 500  # Starting chips for the player

    def spin(self):
        """
        Simulate a spin of the slot machine by requesting three random numbers via the Random.org API.
        """
        base_url = "https://www.random.org/integers/"
        params = {
            "num": 3, "min": 0, "max": 9, "col": 1,
            "base": 10, "format": "plain", "rnd": "new"
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            random_numbers = list(map(int, response.text.strip().split()))
            return [self.emojis[number] for number in random_numbers]
        else:
            print("Could not retrieve random values. Please try again later.")
            return ["❌", "❌", "❌"]  # Fallback in case of error

    def calculate_payout(self, result, bet):
        """
        Calculate the payout based on the spin result.
        """
        if result[0] == result[1] == result[2]:
            return self.values[result[0]] * bet
        else:
            return 0

    def place_bet(self):
        """
        Allow the player to place a bet and validate the amount.
        """
        while True:
            print(f"You have {self.chips} chips.")
            try:
                bet = int(input("Place your bet: "))
                if bet > self.chips or bet <= 0:
                    print("Invalid bet amount. Please try again.")
                else:
                    return bet
            except ValueError:
                print("Please enter a valid number.")

    def play(self):
        """
        Play the slot machine, allowing the player to place bets and spin.
        """
        print("Welcome to the Slot Machine!")
        while self.chips > 0:
            bet = self.place_bet()
            result = self.spin()
            print(f"Result: {' | '.join(result)}")

            payout = self.calculate_payout(result, bet)
            if payout > 0:
                print(f"Congratulations! You won {payout} chips!")
                self.chips += payout
            else:
                print("Sorry, you did not win this time.")
                self.chips -= bet

            if self.chips <= 0:
                print("You have no chips left! Game over.")
                break
            else:
                play_again = input("Do you want to spin again? (yes/no): ").lower()
                if play_again != 'yes':
                    print(f"You left the game with {self.chips} chips. Goodbye!")
                    break

# ------------------ Roulette Game ------------------

def choose_bet_type():
    """
    Display the list of bet types and allow the player to choose one.
    """
    print("\nBet Types:")
    print("1: Straight Bet (bet on a single number, 35:1 payout)")
    print("2: Color Bet (bet on Red or Black, 1:1 payout)")
    print("3: Odd/Even Bet (bet on Odd or Even numbers, 1:1 payout)")
    print("4: Low/High Bet (bet on Low 1-18 or High 19-36, 1:1 payout)")

    while True:
        try:
            choice = int(input("Choose a bet type (1-4): "))
            if choice in [1, 2, 3, 4]:
                return choice
            else:
                print("Invalid choice. Please choose a valid bet type.")
        except ValueError:
            print("Please enter a number between 1 and 4.")


class RouletteGame:
    def __init__(self):
        """
        Initialize the Roulette game with starting chips and red/black numbers.
        """
        self.chips = 1000
        self.red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        self.black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

    def spin_wheel(self):
        """
        Simulate a spin of the roulette wheel.
        """
        return random.randint(0, 36)

    def place_bet(self):
        """
        Allow the player to place a bet and validate the amount.
        """
        while True:
            print(f"You have {self.chips} chips.")
            try:
                bet = int(input("Place your bet amount: "))
                if bet > self.chips or bet <= 0:
                    print("Invalid bet amount. Try again.")
                else:
                    return bet
            except ValueError:
                print("Please enter a valid number.")

    def get_bet_details(self, choice):
        """
        Get the specific details for the selected bet type.
        """
        if choice == 1:
            while True:
                try:
                    number = int(input("Enter a number to bet on (0-36): "))
                    if 0 <= number <= 36:
                        return {"type": "straight", "number": number}
                    else:
                        print("Invalid number. Please choose a number between 0 and 36.")
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == 2:
            color = input("Enter 'red' or 'black': ").lower()
            if color in ["red", "black"]:
                return {"type": "color", "color": color}
            else:
                print("Invalid color. Please choose 'red' or 'black'.")
                return self.get_bet_details(choice)
        elif choice == 3:
            odd_even = input("Enter 'odd' or 'even': ").lower()
            if odd_even in ["odd", "even"]:
                return {"type": "odd_even", "odd_even": odd_even}
            else:
                print("Invalid choice. Please choose 'odd' or 'even'.")
                return self.get_bet_details(choice)
        elif choice == 4:
            low_high = input("Enter 'low' (1-18) or 'high' (19-36): ").lower()
            if low_high in ["low", "high"]:
                return {"type": "low_high", "low_high": low_high}
            else:
                print("Invalid choice. Please choose 'low' or 'high'.")
                return self.get_bet_details(choice)

    def determine_payout(self, result, bet_details, bet_amount):
        """
        Determine the payout based on the result and the bet placed.
        """
        if bet_details["type"] == "straight":
            if result == bet_details["number"]:
                return bet_amount * 35
        elif bet_details["type"] == "color":
            if (bet_details["color"] == "red" and result in self.red_numbers) or \
                    (bet_details["color"] == "black" and result in self.black_numbers):
                return bet_amount
        elif bet_details["type"] == "odd_even":
            if (bet_details["odd_even"] == "odd" and result % 2 != 0 and result != 0) or \
                    (bet_details["odd_even"] == "even" and result % 2 == 0 and result != 0):
                return bet_amount
        elif bet_details["type"] == "low_high":
            if (bet_details["low_high"] == "low" and 1 <= result <= 18) or \
                    (bet_details["low_high"] == "high" and 19 <= result <= 36):
                return bet_amount

        return -bet_amount

    def play(self):
        """
        Play the Roulette game, allowing the player to place and resolve bets.
        """
        print("Welcome to the Roulette Game!")
        while self.chips > 0:
            bet_amount = self.place_bet()
            bet_type = choose_bet_type()
            bet_details = self.get_bet_details(bet_type)
            result = self.spin_wheel()
            print(f"\nThe ball landed on: {result}")

            payout = self.determine_payout(result, bet_details, bet_amount)
            if payout > 0:
                print(f"Congratulations! You won {payout} chips!")
                self.chips += payout
            else:
                print("Sorry, you lost.")
                self.chips += payout

            print(f"You have {self.chips} chips remaining.")
            if self.chips <= 0:
                print("You're out of chips! Game over.")
                break
            else:
                play_again = input("Do you want to play another round? (yes/no): ").lower()
                if play_again != 'yes':
                    print(f"You left the game with {self.chips} chips. Goodbye!")
                    break

# ------------------ Texas Hold'em Poker Game ------------------

def get_card_value(card):
    """
    Convert card values to numeric values for comparison.
    """
    if card['value'] in ['JACK', 'QUEEN', 'KING']:
        return 10
    elif card['value'] == 'ACE':
        return 11
    else:
        return int(card['value'])


class TexasHoldemPoker:
    def __init__(self):
        """
        Initialize the Texas Hold'em Poker game with a shuffled deck and initial chips.
        """
        self.base_url = "https://deckofcardsapi.com/api/deck/"
        self.deck_id = self.get_new_deck()  # Get a new shuffled deck ID
        self.community_cards = []  # Cards on the table
        self.players = {
            "Player 1": {"hand": [], "chips": 1000, "current_bet": 0},
            "Player 2": {"hand": [], "chips": 1000, "current_bet": 0}
        }
        self.pot = 0  # Initialize the pot

    def get_new_deck(self):
        """
        Get a new shuffled deck using the API.
        """
        response = requests.get(f"{self.base_url}new/shuffle/?deck_count=1")
        deck_data = response.json()
        return deck_data['deck_id']

    def draw_cards(self, count=1):
        """
        Draw a specified number of cards from the deck.
        """
        response = requests.get(f"{self.base_url}{self.deck_id}/draw/?count={count}")
        return response.json()['cards']

    def deal_hole_cards(self):
        """
        Deal two cards to each player.
        """
        for player in self.players:
            self.players[player]["hand"] = self.draw_cards(2)

    def deal_flop(self):
        """
        Deal the Flop (3 community cards).
        """
        self.community_cards = self.draw_cards(3)

    def deal_turn(self):
        """
        Deal the Turn (1 additional community card).
        """
        self.community_cards += self.draw_cards(1)

    def deal_river(self):
        """
        Deal the River (1 additional community card).
        """
        self.community_cards += self.draw_cards(1)

    def display_cards(self):
        """
        Display the players' hands and community cards.
        """
        for player, details in self.players.items():
            hand = details["hand"]
            print(f"{player} hand: {', '.join([f'{card['value']} of {card['suit']}' for card in hand])}")
        print(f"Community cards: {', '.join([f'{card['value']} of {card['suit']}' for card in self.community_cards])}")

    def compare_hands(self):
        """
        A simplified comparison of hands based on the highest card value.
        """
        for player, details in self.players.items():
            combined_hand = details["hand"] + self.community_cards
            hand_values = [get_card_value(card) for card in combined_hand]
            best_hand_value = max(hand_values)
            self.players[player]["best_hand"] = best_hand_value  # Store the best hand value

        # Compare hands and determine the winner
        player1_value = self.players["Player 1"]["best_hand"]
        player2_value = self.players["Player 2"]["best_hand"]

        if player1_value > player2_value:
            print("Player 1 wins!")
            self.players["Player 1"]["chips"] += self.pot
        elif player2_value > player1_value:
            print("Player 2 wins!")
            self.players["Player 2"]["chips"] += self.pot
        else:
            print("It's a tie!")
            # Split the pot if it's a tie
            self.players["Player 1"]["chips"] += self.pot // 2
            self.players["Player 2"]["chips"] += self.pot // 2

        self.pot = 0  # Reset the pot after determining the winner

    def betting_round(self):
        """
        Conduct a betting round where both players can bet, call, raise, or fold.
        """
        # Reset current bets for both players
        for player in self.players:
            self.players[player]["current_bet"] = 0

        highest_bet = 0  # Track the highest bet placed in this round

        for player, details in self.players.items():
            if details["chips"] <= 0:
                print(f"{player} is out of chips and cannot bet.")
                continue

            print(f"\n{player}'s turn. You have {details['chips']} chips.")
            while True:
                action = input("Do you want to 'call', 'raise', or 'fold'? ").lower()
                if action == "call":
                    call_amount = highest_bet - details["current_bet"]
                    if details["chips"] >= call_amount:
                        self.pot += call_amount
                        details["chips"] -= call_amount
                        details["current_bet"] += call_amount
                        print(f"{player} calls {call_amount}.")
                    else:
                        self.pot += details["chips"]
                        details["chips"] = 0
                        details["current_bet"] += call_amount
                        print(f"{player} goes all in with {call_amount}.")
                    break

                elif action == "raise":
                    raise_amount = int(input("Enter the amount you want to raise: "))
                    if raise_amount > details["chips"]:
                        print("You do not have enough chips to raise that amount.")
                    elif raise_amount + highest_bet > details["chips"]:
                        print("You cannot raise more than your total chips.")
                    else:
                        self.pot += raise_amount + highest_bet - details["current_bet"]
                        details["chips"] -= (raise_amount + highest_bet - details["current_bet"])
                        details["current_bet"] = raise_amount + highest_bet
                        highest_bet = details["current_bet"]
                        print(f"{player} raises to {highest_bet}.")
                        break

                elif action == "fold":
                    print(f"{player} folds.")
                    details["folded"] = True
                    return

                else:
                    print("Invalid action. Please choose 'call', 'raise', or 'fold'.")

    def play(self):
        """
        Play a simplified game of Texas Hold'em Poker with betting.
        """
        print("Welcome to Texas Hold'em Poker!")

        # Deal hole cards to players
        self.deal_hole_cards()
        print("\nDealing hole cards...")
        self.display_cards()

        # Pre-flop betting round
        print("\nPre-flop betting round:")
        self.betting_round()

        # Deal the Flop
        print("\nDealing the Flop...")
        self.deal_flop()
        self.display_cards()

        # Post-flop betting round
        print("\nPost-flop betting round:")
        self.betting_round()

        # Deal the Turn
        print("\nDealing the Turn...")
        self.deal_turn()
        self.display_cards()

        # Post-turn betting round
        print("\nPost-turn betting round:")
        self.betting_round()

        # Deal the River
        print("\nDealing the River...")
        self.deal_river()
        self.display_cards()

        # Post-river betting round
        print("\nPost-river betting round:")
        self.betting_round()

        # Determine the winner after all community cards are dealt and betting is complete
        print("\nComparing hands...")
        self.compare_hands()

        # Display the final chip counts for both players
        print("\nFinal chip counts:")
        for player, details in self.players.items():
            print(f"{player}: {details['chips']} chips")

        # Reset the deck and community cards for the next game
        self.deck_id = self.get_new_deck()
        self.community_cards = []

# ------------------ Casino Main Menu ------------------

def casino_main():
    """
    Provide the main menu for the Casino app, allowing users to select games or get weather updates.
    """
    while True:
        print("\nWelcome to the PyPop Casino!")
        print("1. Play Blackjack")
        print("2. Play Slot Machine")
        print("3. Play Roulette")
        print("4. Play Texas Hold'em Poker")
        print("5. Leave the Casino (Quit)")

        choice = input("Please choose an option (1-5): ")

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
            print("Thank you for visiting the PyPop Casino! Goodbye!")
            break

        else:
            print("Invalid choice. Please choose a number between 1 and 6.")


# ------------------ Run the Casino App ------------------

if __name__ == "__main__":
    casino_main()
