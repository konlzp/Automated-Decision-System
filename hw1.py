'''
Created on Sep 17, 2015

@author: luozhipei
'''
# Mini-project #6 - Blackjack

#import simplegui
import random
import csv

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
#card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
#card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
global in_play
global outcome
global num_play
global genFlag
global sim_mat
global testFlag
genFlag = 0
in_play = False
num_play = 0
outcome = " start game"
score = 0
sim_mat = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank


       
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = "Hand contains "
        for i in range(len(self.cards)):
            ans += str(self.cards[i]) + " "
        return ans
        # return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)
        # add a card object to a hand
    
    def have_ace(self):
        for c in self.cards:
            if c.get_rank() == 'A':
                return True
        return False
    
    def get_house(self):
        value = 0
        aces = False
        c = self.cards[1]
        rank = c.get_rank()
        v = VALUES[rank]
        if rank == 'A':
            aces = True
        value += v
        if aces and value < 12: value += 10
        return value

    def get_value(self):
        value = 0
        aces = False
        for c in self.cards:
            rank = c.get_rank()
            v = VALUES[rank]
            if rank == 'A': aces = True
            value += v
        if aces and value < 12: value += 10
        return value
        
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        # create a Deck object

    def shuffle(self):
        random.shuffle(self.deck)
        # shuffle the deck 

    def deal_card(self):
        return self.deck.pop()
        # deal a card object from the deck
    
    def __str__(self):
        ans = "The deck: "
        for c in self.deck:
            ans += str(c) + " "
        return ans
        # return a string representing the deck


#define event handlers for buttons
def deal():
    global outcome, in_play, theDeck, playerhand, househand, score, sim_mat, genFlag
    if in_play:
        outcome = "House wins by default!"
        score -= 1
    else:
        outcome = "Hit or stand?"
    in_play = True
    theDeck = Deck()
    theDeck.shuffle()
    #print theDeck
    playerhand = Hand()
    househand = Hand()
    playerhand.add_card(theDeck.deal_card())
    playerhand.add_card(theDeck.deal_card())
    househand.add_card(theDeck.deal_card())
    househand.add_card(theDeck.deal_card())

    """
    Self defined code.
    """
    if genFlag == 0:
        while in_play == True:
            if not testFlag or input('continue?'):
                playerIndex = playerhand.get_value()
                if playerhand.have_ace():
                    playerIndex += 10
                houseIndex = househand.get_house()
                if hitme(playerIndex, houseIndex):
                    hit()
                else:
                    stand()\
#             if playerhand.get_value() < 17:
#                 hit()
#             else:
#                 stand()
    elif genFlag == 1:
        index = playerhand.get_value() - 1 + (househand.get_house() - 1) * 31
        if playerhand.have_ace():
            index = index + 10
        sim_mat[index][1] += 1
        hit()
        if in_play == True:
            if not playerhand.have_ace():
                sim_mat[index][0] += 1
        stand()
    elif genFlag == 2:
        prevScore = score
        index = playerhand.get_value() - 1 + (househand.get_house() - 1) * 31
        if playerhand.have_ace():
            index = index + 10
        sim_mat[index][3] += 1
        stand()
        if score - prevScore > -1:
            sim_mat[index][2] += 1
        
    #print theDeck

def hit():
    global in_play, score, outcome
    if in_play:
        playerhand.add_card(theDeck.deal_card())
        val = playerhand.get_value()
        # print "Player", playerhand, "Value:", val
        if val > 21: 
            outcome = "You are busted! House wins!"
            in_play = False
            score -= 1
            #print outcome, "Score:", score
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global score, in_play, outcome
    if playerhand.get_value() > 21:
        outcome = "You are busted."
        return None
    if not in_play:
        outcome = "Game is over."
        return None
    val = househand.get_value()
    while(val < 17):
        househand.add_card(theDeck.deal_card())
        val = househand.get_value()  
        #print "House:", househand, "Value:", val
    if (val > 21):
        #print "House is busted!"
        if playerhand.get_value() > 21:
            outcome = "House is busted, but House wins tie game!"
            score -= 1
        else: 
            outcome = "House is busted! Player wins!"
            score += 1
    else:
        if (val == playerhand.get_value()):
            outcome = "House wins ties!"
            score -= 1
        elif (val > playerhand.get_value()):
            outcome = "House wins!"
            score -= 1
        else:
            outcome = "Player wins!"
            score += 1
    in_play = False


def hitme(playerhand, househand):
    global sim_mat
    index = playerhand - 1 + (househand - 1) * 31
    if sim_mat == [] :
        with open('transcript', 'r') as simMatFile:
            reader = csv.reader(simMatFile)
            for line in reader:
                tempLine = []
                for probElement in line:
                    tempLine.append(int(probElement))
                sim_mat.append(tempLine)
    if sim_mat[index][0]:
        return True
    else:
        return False

def sim(trials):
    global genFlag
    global sim_mat
    genFlag = 1
    sim_mat = []
    for i in range(0, 31 * 11):
        sim_mat.append([0, 0, 0, 0])
    for i in range(0, trials):
        deal()
    genFlag = 2
    for i in range(0, trials):
        deal()
    i = 0
    for simTuple in sim_mat:
        sim_mat[i] = [(float(simTuple[0]) / simTuple[1]) if simTuple[1] != 0 else 0, (float(simTuple[2]) / simTuple[3]) if simTuple[3] != 0 else 0]
        if i % 31 == 20 or i % 31 == 30:
            sim_mat[i][0] = 0
            sim_mat[i][1] = 1
        if sim_mat[i][0] > sim_mat[i][1]:
            sim_mat[i] = 1
        else:
            if sim_mat[i][1] > 0.28:
                sim_mat[i] = 0
            else:
                sim_mat[i] = 1
        i += 1
    
    with open('transcript','w') as simMatFile:
        writer = csv.writer(simMatFile)
        [writer.writerow(str(r)) for r in sim_mat]
    
def play(trials):
    global genFlag
    global score
    global sim_mat
    genFlag = 0
    score = 0
    sim_mat = []
    with open('transcript', 'r') as simMatFile:
        reader = csv.reader(simMatFile)
        for line in reader:
            tempLine = []
            for probElement in line:
                tempLine.append(int(probElement))
            sim_mat.append(tempLine)
    while not isinstance(trials, int):
        trials = input("Please enter a Int")
    global testFlag
    testFlag = 0
    #testFlag = input('test?')
    for i in range(0, trials):
        deal()
    return float(trials + score) / (2 * trials)

# get things rolling


"""
To run test script, comment following code
"""
if input("Generate Simulation Table?"):
    sim(100000)
num_play = input('The number of experiment?')
print play(num_play)


"""
To generate the summary file, uncomment following code.
"""
# with open('Summary', 'w') as sumFile:
#     for i in range(0, 10):
#         if i < 5:
#             num_play = 10000
#         else:
#             num_play = 100000
#         sumFile.write(str(i) + ". num_play: " + str(num_play) + "  winning rate: " + str(play(num_play)))
"""
End of code.
BTW, the test script is really bad. 
More freedom should be given on how we write our code.
"""