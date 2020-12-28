import random
import os

#card class
class Card():
    suits = ['Clubs', 'Hearts', 'Spades', 'Diamonds']
    ranks = ['A', 'K', 'Q', 'J', '9', '8', '7', '6', '5', '4', '3', '2']
    values = {'A': 11, 'K': 10, 'Q': 10, 'J': 10, '9': 9, '8': 8, '7': 7, '6': 6,\
     '5': 5, '4': 4, '3': 3, '2': 2}

    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def showCard(self):
        print(f'{self.rank} of {self.suit}')

# deck class
class DeckOfCards():
    
    def __init__(self):
        self.deck = []
        self.build()

    def build(self):
        for suit in Card.suits:
            for rank in Card.ranks:
                self.deck.append(Card(suit, rank, Card.values[rank]))
        self.shuffle()


    def shuffle(self):
        random.shuffle(self.deck)

    def isEmpty(self):
        if len(self.deck) == 0:
            self.build()
            self.shuffle()

    def deal(self, *args):
        for x in args:
            self.isEmpty()
            x.addCard(self.deck.pop())
            self.isEmpty()
            x.addCard(self.deck.pop())

    def hit(self, player):
        self.isEmpty()
        player.addCard(self.deck.pop())

# player hand class
class Hand():
    def __init__(self, name, money = 100):
        self.hand = []
        self.money = money
        self.bet = 0
        self.name = name
        self.value = 0

    def addCard(self, card):
        self.hand.append(card)
        self.value += card.value

    def placeBet(self, amount):
        self.bet += amount

    def winHand(self):
        self.money += self.bet * 2
        self.bet = 0
        self.hand = []
        self.value = 0

    def loseHand(self):
        self.money -= self.bet
        self.bet = 0
        self.hand = []
        self.value = 0

    def showHand(self):
        print(f"{self.name}'s hand:")
        for card in self.hand:
            card.showCard()
        print(self.value)

    def clearHand(self):
        self.hand = []

class Dealer(Hand):
    def showDealerCard(self):
        print("Dealer's Card: ")
        self.hand[0].showCard()

#show player and dealer hands
def showHands(*args):
    for x in args:
        print(f"{x.name}'s hand: ")
        x.showHand()
        print('\n')

#show dealer card        


def main():
    
    #create the deck and shuffle it
    deck = DeckOfCards()
    deck.shuffle()

    #initialize player hand and dealer hand
    player1 = Hand('Player 1')
    dealer = Dealer('Dealer')

    #deal intial 2 cards per player
    deck.deal(player1, dealer)

    while True:
        
        player1.showHand()
        dealer.showDealerCard()

        while True:
            hit = input('Would you like to hit? (y/n) ')
            if hit == 'y':
                deck.hit(player1)
                player1.showHand()
                if player1.value > 21:
                    print('You busted!')
                    player1.loseHand()
                    break
            else:
                player1.showHand()
                dealer.showDealerCard()
                
                #keep dealing cards to dealer till value above 16
                while dealer.value <= 16:
                    deck.hit(dealer)
                
                print(dealer.value)

                #if dealer value is between 16 - 21, check to see who won
                if dealer.value < 21 and dealer.value > 16:
                    if dealer.value < player1.value:
                        dealer.showHand()
                        print('Player 1 wins!')
                        player1.winHand()
                        dealer.clearHand()
                    else:
                        dealer.showHand()
                        print('Dealer wins!')
                        player1.loseHand()
                        dealer.clearHand()
                
                #check to see if dealer is over 21 and has an Ace, then modify dealer Ace values till below 21 or no Aces left
                elif dealer.value > 21 and 'A' in [card.rank for card in dealer.hand]:
                    count = [card.rank for card in dealer.hand].count('A')
                    while dealer.value > 21 and count != 0:
                        dealer.value -= 10
                        count -= 1

                    #after modify dealer value for Aces, check to see who wins
                    if player1.value > dealer.value:
                        print('Player 1 wins!')
                        dealer.showHand()
                        player1.winHand()
                        dealer.clearHand()
                    else:
                        print('Dealer wins!')
                        dealer.showHand()
                        player1.loseHand()
                        dealer.clearHand()

                #finally if dealer is over 21 with no Aces, he busted
                elif dealer.value > 21:
                    print('Dealer busted')
                    dealer.showHand()
                    player1.winHand()
                    dealer.clearHand()
                    break

                break
        
        break




main()

# deal

# ask for number of playersjj
