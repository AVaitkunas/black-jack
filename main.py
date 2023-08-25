from random import shuffle
from typing import List

DEALER = "dealer"

value_points_mapping = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}

suits = ("Spades", "Hearts", "Clubs", "Diamonds")


class Card:
    def __init__(self, suit, value):
        if suit not in suits:
            raise ValueError("Incorrect card suit value received")
        if value not in value_points_mapping:
            raise ValueError("Incorrect value of card received")
        self.suit = suit
        self.value = value
        self.points = value_points_mapping[value]

    def __str__(self):
        return f"Card {self.value} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        for suit in suits:
            for value in value_points_mapping:
                card = Card(suit, value)
                self.cards.append(card)

        self.shuffle()

    def __str__(self):
        return f"Deck of {len(self.cards)} cards: {[str(card) for card in self.cards]}"

    def shuffle(self):
        shuffle(self.cards)

    def deal(self) -> Card:
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.name = name
        self.hand: List[Card] = []

    def __str__(self):
        if self.name == DEALER:
            return f"Dealer shows one card: {self.hand[0]}. Points {self.hand[0].points}"
        return f"Player {self.name} has cards: {[str(card) for card in self.hand]}. value: {self.get_points()}"

    def add_card(self, card):
        print(f"Player {self.name} got new card: {str(card) if self.name != DEALER else ''}")
        self.hand.append(card)

    def get_points(self):
        value = 0
        num_aces = 0
        for card in self.hand:
            if card.value == "A":
                num_aces += 1
            value += value_points_mapping[card.value]

        # adjust for aces
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value


if __name__ == '__main__':
    deck = Deck()

    player = Player("Tom")
    dealer = Player(DEALER)

    # Deal initial cards
    for _ in range(2):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())

    # Game loop
    game_over = False
    while not game_over:
        print(player)
        print(dealer)

        action = input("Deal a new card? (y/n)").lower()
        if action not in ("y", "n"):
            print("wrong input. Expected y or n.")
            continue

        if action == "y":
            new_card = deck.deal()
            player.add_card(card=new_card)

            if player.get_points() > 21:
                print(f"{player.name} failed with {player.get_points()} points! Dealer wins.")
                game_over = True
        elif action == "n":
            while dealer.get_points() < 15:
                new_card = deck.deal()
                dealer.add_card(new_card)

            if dealer.get_points() > 21 or dealer.get_points() < player.get_points():
                print(f"{player.name} wins!")
            elif dealer.get_points() > player.get_points():
                print("Dealer wins!")
            else:
                print("It's a tie!")

            game_over = True
