import random

SUITS = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

SHORTSUITS = ['s', 'c', 'd', 'h']

CARDRANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
#This is so the suits will be in order when the hand is sorted
RANKCONVERT = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
               'K': 13}

SUITABBREV = {'Spades': 's', 'Clubs': 'c', 'Diamonds': 'd', 'Hearts': 'h'}


class Deck:
    def __init__(self, pack):
        self.pack = pack
        self.cards = []
        # This creates all of the card inside of the deck
        for i in range(pack):
            for s in SUITS:
                for c in CARDRANKS:
                    self.cards.append(Card(c, s))

    def pick_up_card(self):
        # This will draw a card from the deck as the first card on the discard pile
        a = self.cards[0]
        self.cards.pop(0)
        return a

    def shuffle(self):
        # This shuffles the deck
        random.shuffle(self.cards)


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + SUITABBREV[self.suit]


class Player:
    def __init__(self, name, deck, game):
        self.playerhand = []
        self.playername = name
        self.deck = deck
        self.game = game

    def deal_card(self, card):
        try:
            self.playerhand.append(card)
            if len(self.playerhand) > 8:
                raise ValueError('You currently have 8 cards. Please discard a card to continue.')
        except ValueError as error:
            print(error.args)

    def discard_card(self, card):
        card = get_object(self.playerhand, card)

        # Prevents player from discarding a card if it is is not in their hand
        if card not in self.playerhand:
            return False

        # Removes the card from hand
        self.playerhand.remove(card)

        # Puts the discarded card on the top of the discard pile
        self.game.add_discardpile(card)

        return True

    def declare_rummy(self):
        # This separates the player's hand into 2 separate groups, a group of 3-cards and a group of 4-cards
        rummy_hand = [self.playerhand[:3], self.playerhand[3:7]]
        count = 0
        for s in rummy_hand:
            if matching_run(s):
                count += 1
        if count == 0:
            return False

        # This checks if the groups of cards are sets or runs
        for s in rummy_hand:
            if matching_run(s) is False and matching_set(s) is False:
                return False

        return True

    def play(self):
        while True:
            print("\n Your hand is:\n")
            print(printhand(self.playerhand))
            self.game.display_discardpile()

            # Asks player to choose one of 5 options
            action = input(
                "\n" + self.playername + ", What would you like to do? \n\n(1)Take from pile \n(2)Take from deck \n(3)Discard a card \n(4)Sort hand \n(5)Declare Rummy: ")

            # Pick up a card from the discard pile
            if action == '1':
                if len(self.playerhand) < 8:
                    c = self.game.draw_discardpile()
                    self.playerhand.append(c)
                else:
                    input("You have " + str(len(self.playerhand)) + " cards in your hand and can not pick up any more. Please press enter to choose again")

            # Pick up a card from the deck
            if action == '2':
                if len(self.playerhand) < 8:
                    c = self.deck.pick_up_card()
                    self.playerhand.append(c)
                else:
                    input("You have " + str(len(self.playerhand)) + " cards in your hand and can not pick up any more. Please press enter to choose again")

            # Discard card on to the discard pile
            if action == '3':
                if len(self.playerhand) == 8:
                    discard = input("\nWhich card would you like to discard?")
                    discard = discard.strip()
                    discard = discard.upper()
                    if self.discard_card(discard):
                        # As it is not game over
                        return False
                    else:
                        input("You do not have this card in your hand. Please press enter to choose again")
                else:
                    input("You currently have 7 cards and can not discard more. Please press enter to choose again")

            # Sort the cards in the playerhand
            if action == '4':
                sort_sequence(self.playerhand)

            # Declare Rummy
            if action == '5':

                if len(self.playerhand) == 8:
                    discard = input("\nWhich card would you like to discard?")
                    discard = discard.strip()
                    discard = discard.upper()
                    if self.discard_card(discard):
                        if self.declare_rummy():
                            print(printhand(self.playerhand))
                            # This will be Game Over
                            return True
                        else:
                            input("You do not yet have the cards to declare rummy. Please press enter to choose again.")
                            self.playerhand.append(self.game.draw_discardpile())
                    else:
                        input(
                            "The card you have chosen is not currently in your hand. Please press enter to choose again.")
                else:
                    input(
                        "You can only declare Rummy when you have 8 cards in your hand. Please press enter and pick up a card.")


class Game:
    def __init__(self, hands, deck):
        self.discardpile = []
        self.players = []

        for i in range(hands):
            name = input("Player " + str(i + 1) + ", please enter your name: ")
            self.players.append(Player(name, deck, self))

    def display_discardpile(self):
        if len(self.discardpile) == 0:
            print("\nThe discard pile is currently empty.")
        else:
            print("\nThe card at the top of the pile is: ", self.discardpile[0])

    def add_discardpile(self, card):
        self.discardpile.insert(0, card)

    def draw_discardpile(self):
        if len(self.discardpile) != 0:
            return self.discardpile.pop(0)
        else:
            return None

    def play(self):
        i = 0
        while self.players[i].play() is False:
            i += 1
            if i == len(self.players):
                i = 0
            # This creates blank lines which will clear the screen so player 2 is unable to see player 1's moves
            input("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" + self.players[
                i].playername + ", It's your turn to play. Please press enter when you're ready")

        # This will print when someone wins
        print("Game Over")
        print(self.players[i].playername, " is the winner!")


def matching_set(sequence):
    for card in sequence:
        if card.rank != sequence[0].rank:
            return False

    return True


def matching_run(sequence):
# checks if there is a matching run within the sequence

    # Cards are sorted in order of their rank
    sort_sequence(sequence)

    # This checks that the suit is the same fo all of the cards within this run
    for card in sequence:
        if card.suit != sequence[0].suit:
            return False

    # This is how the ranks are compared
    for i in range(1, len(sequence)):
        if RANKCONVERT[sequence[i].rank] != RANKCONVERT[sequence[i - 1].rank] + 1:
            return False

    return True


def get_object(arr, strcard):
    # This makes sure there are only 2 places - 1 for the rank and 1 for the suit
    if len(strcard) != 2:
        return None

    for item in arr:
        if item.rank == strcard[0] and item.suit[0] == strcard[1]:
            return item

    return None


def printhand(arr):
    s = ""
    for card in arr:
        s = s + " " + str(card)
    return s


def sort_sequence(sequence):
    hand_is_sorted = False

    while hand_is_sorted is False:
        hand_is_sorted = True
        for i in range(0, len(sequence) - 1):
            if RANKCONVERT[sequence[i].rank] > RANKCONVERT[sequence[i + 1].rank]:
                a = sequence[i + 1]
                sequence[i + 1] = sequence[i]
                sequence[i] = a
                hand_is_sorted = False
    return sequence


def main():
    # This creates the deck
    deck = Deck(1)
    deck.shuffle()

    # Starts a new game with 2 players
    g = Game(2, deck)

    # This deals 7 cards to each player
    for i in range(7):
        for hand in g.players:
            card = deck.pick_up_card()
            hand.deal_card(card)

    # This will create the discard pile
    first_card = deck.pick_up_card()
    g.add_discardpile(first_card)

    # Begins the game!
    g.play()


if __name__ == "__main__":
    main()
