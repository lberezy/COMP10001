# Project 3 - COMP10001
# Author: Lucas Berezy
#
#   Hearts card game 'AI'.
# I've never played Hearts before this, and it's still a little confusing to me
# which means you get to laugh extra hard at some of the plays the AI may make.


import itertools 

# construct some card set constants, might come in handy and set gymnastics is
# fun.
__SUITS__   = set(['H','D','C','S']) # hearts, diamonds, clubs, spades
__NUMBERS__ = set([str(i) for i in range(2, 10)]).union(set(['0']))
__ROYALS__  = set(['J','Q','K','A'])
__RANKS__   = __NUMBERS__.union(__ROYALS__)
__RANK_ORDER__ = \
    ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
__ALLCARDS__ = map(''.join, itertools.product(__RANKS__,__SUITS__))


# filter functions, to make life easier... maybe. I wrote these before thinking
# what i'd actually use them for.

def f_suit(suit):
    ''' returns an appropriate filter function based on the suit. For use
    in filter()., otherwise returns None '''

    if suit in __SUITS__:
        return lambda card: card[1] == suit

def cards_to_suit(cards, sorted = True):
    ''' takes a list of cards, returns an optionally sorted dict of lists of
    each suit of cards (in rank order) '''

    suits = {}
    # create dictionary with 
    for suit in __SUITS__:
        suits[suit] = [card for card in cards if f_suit(suit)(card)]
    if sorted:
        for suit in output:
            output[suit].sort(key = lambda x: __RANK_ORDER__.index(x[0]))
    return output

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
    if len(filter(f_hearts, hand)):
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
    if stop_rank not in __RANKS__ or suit not in __SUITS__: # invalid end point
        return
    cards = map(''.join, itertools.product(__RANKS__,suit)) # generator source
    cards.sort(key = lambda x: __RANK_ORDER__.index(x[0])) # sorted (2..ace)
    count = 0
    card = cards[0] # first card in source
    while True:
        yield card
        card = cards[count]
        count += 1
        if card == (stop_card): # include the stop card in generator
            yield stop_card
            break


#playing QS breaks hearts, QS treated like a heart

# filter functions for H,D,C,S etc
# have_suit() function
# ducking function (highest card that doesn't win, but isn't 0D)


def pass_cards(hand):
    ''' Pases a 3, hopefully advantageous cards at the beginning of the round.
    Prioritises passing QKA of Spades, then the QS or 0D then if possible,
    voiding in a suit.'''

    def pick(card):
        ''' removes card from hand and places it in picked list '''
        to_pass.append(hand[card[1]].pop(hand[card[1]].index(card)))


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
    # don't really need to filter, but those functions were just sitting around
    if 'AS' in filter(f_spades, hand) and len(to_pass) < 3:
        # pop the card from the hand into the to_pass list
        pick('AS')
    if 'KS' in filter(f_spades, hand) and len(to_pass) < 3:
        pick('KS')
    if 'QS' in filter(f_spades, hand) and len(to_pass) < 3:
        pick('QS')

    # it's hard to capture this card when in hand, so give away unless you 
    # don't have a card to capture it with (A,K,Q,J of Diamonds)
    if '0D' in filter(f_diamonds, hand) \
        and have_any_cards(['AD','KD','QD']) and len(to_pass) < 3:
        pick('0D')
        # set a flag so we know not to give these away later
        keep_high_diamonds = True

    # sort remaining suits by size
### BUG HERE
    sorted_suits = sorted([(len(x),x) for x in cards_to_suit(hand)])
    print sorted_suits
    sorted_suits = [x[1] for x in sorted_suits]
    print sorted_suits
    # pick off smallest suits that will fit entirely

    #WARNING: infinite loop
    #FIXME
    for suit in sorted_suits:
        # if the whole suit will fit in remaining pick
        if len(suit) <= (3 - len(to_pass)):
                print suit
                [pick(card) for card in suit]

        # don't forget to check len(to_pass) == pass_size
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
# can lead anything 
    if played == []:
        # trying to lead penalty card when not broken and not forced to break
        if not broken and (play[1] == 'H' or play == 'QS') and \
         (have_suit(hand, 'D') or have_suit(hand, 'D')
         or (filter(f_spades, hand) != ['QS'])):
            return False
        return True

    lead_card = played[0]


#NOT FINISHED
#"         # must follow suit if card of that suit held" doesn't work
#is_valid_play(['KH'], ['0D', '9S', '3S', '3D', '3H', '5D', 'AD', '6C', '7D', '6H', 'JH'],'JH',True)""",True
    # not following suit when following is possible
    if have_suit(hand, lead_card[1]) and play[1] != lead_card[1]:
        return False
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

    def shot_moon(tricks):
        ''' returns a boolean True if the player has captured every penalty
        card including the QS. '''

        tricks = list(itertools.chain(tricks))  # flatten list of lists
        if len(filter(f_suit('H'),tricks)) == len(__RANK_ORDER__) \
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
        # if so, make them win. This score is a mutually exclusive outcome, so
        # there can now be only one winner.
        # probably not the 'right' way to calculate it
            
            # score == 16 if captured 0D as well (26 - 10)
        if score == 16 and shot_moon(tricks):
            # set the new score
            score = -36 # wew, magic numbers (-26 moon shoot + -10 for 0D)
        if score == 26 and shot_moon(tricks): 
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

    def can_follow():
        ''' returns a boolean status of the player being able 
        to follow suit'''
        if not len(filter(f_suit(lead_suit), get_valid_plays())):
            return False
        return True

    round_no = get_round_no()
    lead_suit = played[0][1] # suit that is currently leading
    #mylead = # some truth value

    valid_plays = get_valid_plays() # if there is only one move, make it
    if len(valid_plays) == 1:
        return valid_plays

    if '0D' in played: # if the 0D has been played, try to capture it
        # try each card in Diamonds above 0D, highest first
        for card in [x for x in card_gen('AD')][:-5:-1]:
            if card in valid_plays:
                return card

    if 'QS' in played: # panic!
        # try to play highest card under queen
        for card in [x for x in card_gen('JS')][::-1]:
            if card in valid_plays:
                return card

    # try play the highest card that's valid if it's not dangerous (can't follow
    #    or hearts not broken)
    if can_follow() or not hearts:
        # 
    # try play the 'shortest' suit that is a valid play if it's 'dangerous'

    #if round_no == 0:
        #play highest spade if possible, else play any damned card
        #valid_plays[]
    return