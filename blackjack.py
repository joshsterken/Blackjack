import random
import os

#card class
class Card():
    suits = ('Clubs', 'Hearts', 'Spades', 'Diamonds')
    ranks = ('A', 'K', 'Q', 'J', '9', '8', '7', '6', '5', '4', '3', '2')
    values = {'A': 11, 'K': 10, 'Q': 10, 'J': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def showCard(self):
        print(f'{self.rank} of {self.suit}')

# deck class
class DeckOfCards():
    
    def __init__(self):
        self.deck = []#Card('Clubs', '4', 4), Card('Clubs', '3', 3), Card('Clubs', '2', 2), Card('Clubs', 'A', 11), Card('Clubs', 'K', 10), Card('Clubs', 'Q', 10), Card('Clubs', 'A', 11),Card('Clubs', '7', 7)]
        self.build()

    def build(self):
        for suit in Card.suits:
            for rank in Card.ranks:
                self.deck.append(Card(suit, rank, Card.values[rank]))
        #self.shuffle()


    def shuffle(self):
        random.shuffle(self.deck)

    def isEmpty(self):
        if len(self.deck) == 0:
            self.build()
            self.shuffle()

    def deal(self, *args):
        for x in args:
            self.isEmpty()
            x.addCard(self.deck.pop(0))
            self.isEmpty()
            x.addCard(self.deck.pop(0))

    def hit(self, player):
        self.isEmpty()
        player.addCard(self.deck.pop(0))

# player hand class
class Hand():
    def __init__(self, name, money = 100):
        self.hand = []
        self.money = money
        self.bet = 0
        self.name = name
        self.value = 0
        self.tempValue = 0

    def addCard(self, card):
        self.hand.append(card)
        self.value += card.value

    def placeBet(self):
        while True:
            try:
                amount = int(input('How much to bet? $'))
                if self.money < amount:
                    print('**Insufficient funds**')
                else:
                    break
            except ValueError:
                print('Amount must be an integer')

        self.bet += amount

    def winHand(self):
        self.money += self.bet
        self.bet = 0
        self.hand = []
        self.value = 0

    def loseHand(self):
        self.money -= self.bet
        self.bet = 0
        self.hand = []
        self.value = 0

    def pushHand(self):
        self.bet = 0
        self.hand = []
        self.value = 0

    def showHand(self):
        print(f"-----{self.name}'s hand-----")
        print(f'-----${self.money}----------')
        print(f'*****Current value: {self.value}')
        for card in self.hand:
            card.showCard()
        print('\n')

    def clearHand(self):
        self.hand = []
        self.value = 0

class Dealer(Hand):
    def showDealerCard(self):
        print("Dealer's Card: ")
        self.hand[0].showCard()
        print('\n')

    def showHand(self):
        print(f"{self.name}'s hand:")
        print(f'*****Current value: {self.value}')
        for card in self.hand:
            card.showCard()
        print('\n')

#show player and dealer hands
def showHands(*args):
    for x in args:
        print(f"{x.name}'s hand: ")
        x.showHand()
        print('\n')

def playAgain(deck, dealer, player1):
    ans = input('Would you like to play another round (y/n)? ')
    if ans == 'y':
        round(deck, dealer, player1)


def round(deck, dealer, player1):
    while True:
        
        #deal intial 2 cards per player
        deck.deal(player1, dealer)

        player1.showHand()
        dealer.showDealerCard()

        
        player1.placeBet()
        hit = input('Would you like to hit? (y/n) ')
        while hit == 'y':
            deck.hit(player1)
            player1.showHand()
            dealer.showDealerCard()
            
            tempValue = player1.value

            if player1.value > 21 and 'A' in [card.rank for card in player1.hand]:
                count = [card.rank for card in player1.hand].count('A')
                while tempValue > 21 and count != 0:
                    tempValue -= 10
                    count -= 1
                if tempValue > 21:
                    print('You busted!')
                    player1.loseHand()
                    dealer.clearHand()
                    playAgain(deck, dealer, player1)
                    break                    

            hit = input('Would you like to hit? (y/n) ')


        player1.showHand()
        
        #keep dealing cards to dealer till value above 16
        while dealer.value <= 16:
            deck.hit(dealer)

        #if player hasn't busted, set player value to value not over 21
        if player1.value > 21:
            player1.value = tempValue

        #if dealer value is between 16 - 21, check to see who won
        if dealer.value > 16 and dealer.value < 21 :
            if dealer.value < player1.value:
                dealer.showHand()
                player1.winHand()
                dealer.clearHand()
                print('Player 1 wins!')
                playAgain(deck, dealer, player1)
            elif dealer.value > player1.value and dealer.value <= 21:
                dealer.showHand()
                player1.loseHand()
                dealer.clearHand()
                print('Dealer wins!')
                playAgain(deck, dealer, player1)
            elif dealer.value == player1.value and dealer.value <= 21:
                dealer.showHand()
                player1.pushHand()
                dealer.clearHand()
                print('Push Round!')
                playAgain(deck, dealer, player1)
        
        #check to see if dealer is over 21 and has an Ace, then modify dealer Ace values till below 21 or no Aces left
        elif dealer.value > 21 and 'A' in [card.rank for card in dealer.hand]:
            count = [card.rank for card in dealer.hand].count('A')
            while dealer.value > 21 and count != 0:
                dealer.value -= 10
                count -= 1
            while dealer.value <= 16:
                if deck.deck[0].rank == 'A' and dealer.value >= 11:
                    deck.isEmpty()
                    dealer.hand.append(deck.deck.pop(0))
                    dealer.value += 1
                else:
                    deck.hit(dealer)

            #after modify dealer value for Aces, check to see who wins
            if dealer.value > 21:
                dealer.showHand()
                player1.winHand()
                dealer.clearHand()
                print('Dealer busted!')
                playAgain(deck, dealer, player1)

            elif player1.value > dealer.value:                
                dealer.showHand()
                player1.winHand()
                dealer.clearHand()
                print('Player 1 wins!')
                playAgain(deck, dealer, player1)

            elif player1.value == dealer.value:
                dealer.showHand()
                player1.pushHand()
                dealer.clearHand()
                print('Push Round!')
                playAgain(deck, dealer, player1)
            
            else:                
                dealer.showHand()
                player1.loseHand()
                dealer.clearHand()
                print('Dealer wins!')
                playAgain(deck, dealer, player1)

        #finally if dealer is over 21 with no Aces, he busted
        elif dealer.value > 21:
            
            dealer.showHand()
            player1.winHand()
            dealer.clearHand()
            print('Dealer busted!')
            playAgain(deck, dealer, player1)

        break


def main():
    
    #create the deck and shuffle it
    deck = DeckOfCards()
    #deck.shuffle()

    #initialize player hand and dealer hand
    player1 = Hand('Player 1')
    dealer = Dealer('Dealer')

    round(deck, dealer, player1)


main()

# deal

# ask for number of playersjj
