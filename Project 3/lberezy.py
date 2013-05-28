# Project 3 - COMP10001
# Author: Lucas Berezy
#
#   Hearts card game 'AI'.
# I've never played Hearts before this, and it's still a little confusing to me
# which means you get to laugh extra hard at some of the plays the AI may make.


import itertools 

# construct some card set constants, might come in handy and set gymnastics is
# fun.
SUITS   = set(['H','D','C','S']) # hearts, diamonds, clubs, spades
NUMBERS = set([str(i) for i in range(2, 10)]).union(set(['0']))
ROYALS  = set(['J','Q','K','A'])
RANKS   = NUMBERS.union(ROYALS)
RANK_ORDER = \
    ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
ALL_CARDS = map(''.join, itertools.product(RANKS,SUITS))


# filter functions, to make life easier... maybe. I wrote these before thinking
# what i'd actually use them for.

def f_suit(suit):
    ''' returns an appropriate filter function based on the suit. For use
    in filter()., otherwise returns None '''

    if suit in SUITS:
        return lambda card: card[1] == suit

def cards_to_suit(cards, sort = True):
    ''' takes a list of cards, returns an optionally sorted dict of lists of
    each suit of cards (in rank order) '''

    suits = {}
    # create dictionary with {suit: [cards]}
    for suit in SUITS:
        suits[suit] = [card for card in cards if f_suit(suit)(card)]
        if sort:
            card_sort(suits[suit])
    return suits

def card_sort(cards, rev=False):
    '''sorts a list of cards in rank order'''
    return sorted(cards, key=lambda x: RANK_ORDER.index(x[0]), reverse=rev)

def have_suit(hand, suit):
    ''' checks to see if suit is in hand '''

    if len([card[1] for card in hand if card[1] == suit]):
        return True
    return False

def have_any_cards(cards, hand):
    ''' Returns true if any card in list of cards is in hand '''

    assert type(cards)==list
    for card in cards:
        if card in hand:
            return True
    return False

def have_penalty(hand):
    ''' Returns true iff there is a Heart or QS in hand '''
    
    if 'QS' in hand:
        return True
    if len(filter(f_suit('H', hand))):
        return True
    return False

def is_penalty(card):
    if card == 'QS' or card[1] == 'H':
        return True
    return false

def card_gen(stop_card):
    ''' Just learnt what yield does, so here's a generator function to
    generate cards from the bottom of a suit up until a stop card. 
    useful when generating runs of cards in a list:
    [card for card in card_gen(stop_card)]
    it's super messy.
    '''
    
    suit = stop_card[1]
    stop_rank = stop_card[0]
    if stop_rank not in RANKS or suit not in SUITS: # invalid end point
        return
    cards = map(''.join, itertools.product(RANKS,suit)) # generator source
    # can't use card_sort() as sort needs to be in-place and lazy
    cards.sort(key = lambda x: RANK_ORDER.index(x[0])) # sorted (2..ace)
    print cards
    count = 0
    while True:
        card = cards[count]
        yield card
        count += 1
        if card == (stop_card): # include the stop card in generator
            break

###############################################################################

def pass_cards(hand):
    ''' Pases a 3, hopefully advantageous cards at the beginning of the round.
    Prioritises passing QKA of Spades, then the QS or 0D then if possible,
    voiding in a suit.'''

    def pick(card):
        ''' removes card from hand and places it in picked list '''
        to_pass.append(hand.pop(hand.index(card)))


    # Passes a hopefully advantageous list of 3 cards
    # from the dealt hand of cards
    #
    # Priorities:
    #   Rid self of A,K,Q of Spades
    #   If have 0D, discard only if have A,K,Q of Diamonds
    #   Try and go void in a suit, if it fits entirely into remaining pass
    #   Try and go void in the shortest suit that's not hearts, starting with
    #   the highest cards (that aren't A,K,Q of Diamonds if 0D was passed)
    #   Avoid passing low spades

    # seriously avoid passing low spades

    to_pass = [] # 3 cards to pass
    ##hand = cards_to_suit(hand) # sort into list of suits

    # Remove A,K,Q of Spades first
    for card in ['AS','KS','QS']:
        if card in filter(f_suit('S'), hand) and len(to_pass) < 3:
            pick(card)

    # it's hard to capture this card when in hand, so give away unless you 
    # don't have a card to capture it with (A,K,Q,J of Diamonds)
    if '0D' in filter(f_suit('D'), hand) \
        and have_any_cards(['AD','KD','QD'], hand) and len(to_pass) < 3:
        pick('0D')
        # set a flag so we know not to give these away later
        keep_high_diamonds = True

    # sort remaining suits by size
    # dictionary of {suit: [cards]}
    suit_dict = cards_to_suit(hand)
    # form a list of suits in order of how many cards each contains
    sorted_suits = sorted(suit_dict.keys(), key = lambda  x: len(suit_dict[x]))

    # attempt to go void, from shortest suit to longest suit
    for suit in sorted_suits:    # dictionary of {suit: [cards]}
            # try and take highest cards first
            for card in card_sort(suit_dict[suit], rev = True):
                if len(to_pass) < 3:
                    pick(card)
                else:
                    return to_pass

    #assert(len(to_pass) == 3)
    return to_pass



def is_valid_play(played, hand, play, broken):
    ''' Determines if a given play is valid, based on current hand, played
    cards in current trick and if hearts are broken according to the rules
    in the spec. '''

    if play not in hand:    # no fun allowed
        return False
    if not play:    # must play something
        return False

    # leading 
    if played == []:
        # trying to lead penalty card when not broken and not forced to break
        if not broken and (play[1] == 'H' or play == 'QS') and \
         (have_suit(hand, 'D') or have_suit(hand, 'D')
         or (filter(f_suit('S'), hand) != ['QS'])):
            return False
        return True

    # otherwise...

    lead_card = played[0]
    # not following suit when following is possible
    # if you are trying to play off suit, but can follow suit, don't allow it
    if have_suit(hand, lead_card[1]) and play[1] != lead_card[1]:
        return False
    # at this point, anything else is a valid move (I hope)
    return True


def get_valid_plays(played, hand, broken, is_valid=is_valid_play):
    ''' returns a list of all valid plays that can be made from a hand given
    some play state variables. '''

    output = []
    for card in hand:
        if (is_valid(played, hand, card, broken)):
            output.append(card)
    return output


def score_game(tricks_won):
    ''' scores each players list of tricks won and returns a tuple of players
    scores and a boolean regarding their winning status in a list, in order
    of the original ordering of lists in tricks_won. players may draw. '''

    def shot_moon():
        ''' returns a boolean True if the player has captured every penalty
        card including the QS. '''

        tricks = list(itertools.chain.from_iterable(tricklist))  # flatten list of lists
        if len(filter(f_suit('H'),tricks)) == len(RANK_ORDER) \
            and ('QS' in tricks):
            return True
        return False

    scores = []
    # construct a list of final scores for each player
    for tricklist in tricks_won:
        score = 0
        for trick in tricklist:
            score += score_trick(trick)

        # did the player 'shoot the moon' (score = 26 or 36 (from 0D))?
        # if so, make them win.

        if score == 16 and shot_moon(): # (shot moon + 0D)
            # set the new score
            score = -36 # wew, magic numbers (-26 moon shoot + -10 for 0D)
        if score == 26 and shot_moon(): 
            score *= -1 # turn that frown upside down!
        scores.append(score)

    # modify the list so that each element is now a tuple of (score, Bool)
    # where Boolean True represents _a_ winning player (i.e. is equal to the
    # minumum score.
    return [(score,(lambda x: x == min(scores))(score)) for score in scores]


def score_trick(trick):
    ''' scores a trick based on the rules set out in the spec.
            Hearts: +1 point
            Q of S: +13 points
            0 of D: -10 points
    '''
    score = 0 # should init to 0 on first increment, but be explicit
    score += len(filter(f_suit('H'),trick))     # number of hearts in trick
    score +=  13 * ('QS' in trick)   # Queen of Spades
    score += -10 * ('0D' in trick)   # 10 of Diamonds
    return score


def play(tricks_won, played, hand, broken, is_valid=is_valid_play, \
    valid_plays=get_valid_plays, score=score_game):

    def get_round_no():
        ''' returns the current round of play based on tricks won '''
        return sum([len(tricklist) for tricklist in tricks_won])

    def must_follow():
        ''' returns a boolean status of the player being required 
        to follow suit'''
        if not len(filter(f_suit(lead_suit), get_valid_plays())):
            return False
        return True

    round_no = get_round_no()
    print round_no
    if len(played):
        print played
        lead_suit = played[0][1] # suit that is currently leading
    #mylead = # some truth value

    valid_plays = get_valid_plays(played, hand, broken, is_valid)

    # if there is only one move, make it
    if len(valid_plays) == 1:
        return valid_plays[0]   # return string not list

    if '0D' in played: # if the 0D has been played, try to capture it
        # try each card in Diamonds above 0D, highest first
        for card in [x for x in card_gen('AD')][:-5:-1]:
            if card in valid_plays:
                return card  # return string, not list

    if 'QS' in played: # panic!
        # try to play highest card under queen
        for card in [x for x in card_gen('JS')][::-1]:
            if card in valid_plays:
                return card  # return string, not list

    # try play the highest card that's valid if it's not dangerous (can't follow
    #    or hearts not broken)
    #if not must_follow() or not hearts:
        # 
    # try play the 'shortest' suit that is a valid play if it's 'dangerous'

    #if round_no == 0:
        #play highest spade if possible, else play any damned card
        #valid_plays[]

    ### 0/10 move ###
    return valid_plays[0] # if all else fails, return the first viable card