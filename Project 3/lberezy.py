# Project 3 - COMP10001
# Author: Lucas Berezy


import itertools 

# construct some card set constants
__SUITS__     = set(['H','D','C','S']) # hearts, diamonds, clubs, spades
__NUMBERS__ = set(str(i) for i in range(2, 10),0)
__ROYALS__    = set(['J','Q','K','A'])
__RANKS__     = __NUMBERS__.union(__ROYALS__)
__RANK_ORDER__ = \
    ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
__ALLCARDS__ = map(''.join, itertools.product(__RANKS__,__SUITS__))



def f_hearts(hand):
    return [card[1] for card in hand if card[1] == 'H']
def f_diamonds(hand):
    return [card[1] for card in hand if card[1] == 'D']
def f_clubs(hand):
    return [card[1] for card in hand if card[1] == 'C']
def f_spades(hand):
    return [card[1] for card in hand if card[1] == 'S']

def have_suit(hand, suit):
    ''' checks to see if suit is in hand '''
    if len([card[1] for card in hand if card[1] == suit]):
        return True
    return False


#playing QS breaks hearts, QS treated like a heart

# filter functions for H,D,C,S etc
# have_suit() function
# ducking function (highest card that doesn't win, but isn't 0D)
def pass_cards(hand, pass_size = 3):
    ''' Pases a 3, hopefully advantageous cards at the beginning of the round.
    Prioritises passing QKA of Spades, then the QS or 0D then if possible,
    voiding in a suit.'''
    def pick(card, hand, picked):
        ''' removes card from hand and places it in picked list '''
        to_pass.append(hand[card[1]].pop(hand[card[1]].index(card)))


    # Passes a hopefully advantageous list of 3 cards
    # from the dealt hand of cards
    #
    # Priorities:
    # check if QS is in hand
    #    Go void in a suit iff possible
    #    

    # seriously avoid passing low spades

    # QKA of Spades first, then go void

    to_pass = [] # 3 cards to pass
    pass_count = 0 # number of cards chosen so far
    hand_list = hand[::] # store backup of flat hand list
    hand = cards_to_suit(hand) # sort into list of suits

    # check for 'interesting' cards
    if 'QS' in filter(f_spades, hand): # not really necessary to filter
        # pop the card from the hand into the to_pass list
        to_pass.append(hand['S'].pop(hand['S'].index('QS')))

    if '0D' in filter(f_diamonds, hand):
        # pop the card from the hand into the to_pass list
        to_pass.append(hand['D'].pop(hand['D'].index('0D')))

    # check if there are any suits to go void in and try to do so
    for suit in __SUITS__:
        suit = filter(filter_)
        if len(suit) <= (pass_size - pass_count):
            [to_pass.append(card) for card in suit]

    # don't forget to check len(to_pass) == pass_size
    return to_pass

def cards_to_suit(cards, sorted = True):
    ''' takes a list of cards, returns an optionally sorted dict of lists of
    each suit of cards '''
    hearts        = [x for x in cards if x[1] == 'H']
    diamonds     = [x for x in cards if x[1] == 'D']
    clubs         = [x for x in cards if x[1] == 'C']
    spades         = [x for x in cards if x[1] == 'S']
    output = {'H': hearts, 'D': diamonds, 'C': clubs, 'S': spades}
    if sorted:
        for suit in output:
            output[suit].sort(key = lambda x: __RANK_ORDER__.index(x[0]))
    return output

def is_valid_play(played, hand, play, broken):
    ''' sosjfgodijg '''
     output = False
     if play not in hand:    # no fun allowed
         return False

     if played == []:    # your lead
         if not broken and (play[1] == 'H' or play == 'QS') and \
         ( filter(have_suit(), )
             return False
         return True

