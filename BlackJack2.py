import random

class Card(object):

    suitList = ["Hearts", "Diamonds", "Clubs", "Spades"]
    rankList = ["Invalid", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    scoreList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def __init__ (self, suit=0, rank=1):
        if suit >= 0 and suit <= 3:
            self.suit = suit
        else:
            self.suit = 0
        if rank >= 1 and rank <= 13:
            self.rank = rank
        else:
            self.rank = 1
        self.score = self.scoreList[self.rank]
        self.cname = self.rankList[self.rank]
        self.sname = self.suitList[self.suit]

    def __str__(self):
        return self.rankList[self.rank] + " of " + self.suitList[self.suit]

    def __repr__(self):
        return self.rankList[self.rank] + " of " + self.suitList[self.suit]

    def __cmp__(self, other):
        i = cmp(self.rank, other.rank)
        if i == 0:
            return cmp(self.suit, other.suit)
        return i

class Deck(object):
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                self.cards.append(Card(suit, rank))

    def __getitem__(self, i):
        return self.cards[i]

    def __iter__(self):
        for card in self.cards:
            yield card

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return '\n'.join([str(c) for c in self])

    def __repr__(self):
        return str(self.cards)

class BJ(object):

    dealer_hit_threshold = 15

    def __init__(self):
        '''
        Designed for 2 players. Player 2 is the dealer. Dealer wins a tie.
        Results are appended to self.results:
        [[winner, playerhand, dealerhand], [winner, playerhand, dealerhand]]
        Results are formatted for output.
        '''
        self.results = []
        self.deck = Deck()

    def deal_hand(self, n, deck):
        '''
        Randomly deal and remove n cards from a Deck object.
        '''
        hand = []
        if len(deck) >= n:
            for i in range(n):
                hand.append(deck.cards.pop(random.choice(range(len(deck)))))
        else:
            print ("There are not enough cards in the deck to deal any cards.")
        return hand

    def hit_hand(self, hand, deck):
        if len(deck):
            hand.append(deck.cards.pop(random.choice(range(len(deck)))))
            return True
        else: return False

    def score_hand_BJ(self, hand):
        score = sum([card.score for card in hand])
        if 'Ace' in [card.cname for card in hand]:
            if score <= 11:
                score += 10
        return score

    def play(self):
        playing = False
        print
        while True:
            option = raw_input("(D)eal, (H)it Me, (S)tand, (Q)uit")
            if option.upper() == "D":
                if playing:
                    print ("You are already playing a hand!")
                else:
                    playing = True
                    hand1 = self.deal_hand(2, self.deck)
                    hand2 = self.deal_hand(2, self.deck)
                    print ("Player 1 Hand: %s\nPlayer 2 Hand: %s" % (hand1, hand2)
                    print ("Player 1 Score: %s\nPlayer 2 Score: %s" % (self.score_hand_BJ(hand1), self.score_hand_BJ(hand2))
                    while self.score_hand_BJ(hand2) <= BJ.dealer_hit_threshold:
                        if not self.deck:
                            print ("The deck is empty. Start over.")
                            self.play_over()
                            return
                        else:
                            self.hit_hand(hand2, self.deck)
                            print ("Dealer took a HIT. Current HAND: %s Score: %s" % (hand2, self.score_hand_BJ(hand2))
                            if self.score_hand_BJ(hand2) > 21:
                                print "Dealer BUSTS. Player wins."
                                self.results.append(["Player", hand1, hand2])
                                playing = False
                                print

            elif option.upper() == "H":
                if playing:
                    if not self.deck:
                        print ("The deck is empty. Start over.")
                        self.play_over()
                        return
                    else:
                        self.hit_hand(hand1, self.deck)
                        print ("Player took a HIT. Current HAND: %s Score: %s" % (hand1, self.score_hand_BJ(hand1))
                        if self.score_hand_BJ(hand1) > 21:
                            print ("Player BUSTS. Dealer wins.")
                            self.results.append(["Dealer", hand1, hand2])
                            playing = False
                            print
                else:
                    print ("You must DEAL before taking a HIT")

            elif option.upper() == "S":
                if playing:
                    if self.score_hand_BJ(hand1) > self.score_hand_BJ(hand2):
                        print ("PLAYER wins this hand. Score: %s to %s" % (self.score_hand_BJ(hand1), self.score_hand_BJ(hand2))
                        self.results.append(["Player", hand1, hand2])
                    else:
                        print ("DEALER wins this hand. Score: %s to %s" % (self.score_hand_BJ(hand1), self.score_hand_BJ(hand2))
                        self.results.append(["Dealer", hand1, hand2])
                else:
                    print ("You must DEAL before selecting option to STAND.")
                playing = False
                print

            elif option.upper() == "Q":
                self.play_over()
                return

    def play_over(self):
        dd = dict.fromkeys(["Player", "Dealer"], 0)
        for hand in self.results:
            dd[hand[0]] += 1
        playerwins = dd["Player"]
        dealerwins = dd["Dealer"]
        if playerwins > dealerwins:
            resultList = ["", "Player won %d hand%s to %d." % (playerwins, ["", "s"][playerwins>1 or 0], dealerwins)]
        elif playerwins == dealerwins:
            resultList = ["There was a tie %d hand%s to %d." % (playerwins, ["", "s"][playerwins>1 or 0], dealerwins)]
        else:
            resultList = ["Dealer won %d hand%s to %d." % (dealerwins, ["", "s"][dealerwins>1 or 0], playerwins)]
        resultList.append("Hands Played:")
        if self.results:
            for hand in self.results:
                resultList.append("  Player: %s   Dealer: %s" % (", ".join([str(c) for c in hand[1]]), ", ".join([str(c) for c in hand[2]])))
        else:
            resultList.append("No hands were played")
        print '\n'.join(resultList)

if __name__ == "__main__":
    g = BJ()
    g.play()
