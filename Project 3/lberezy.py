'''
    Project 3 - COMP10001
    Author: Lucas Berezy

    A Hearts card game 'AI' and score prediction.

I've never played Hearts before this, and it's still a little confusing to me
which means you get to laugh extra hard at some of the plays the AI may make.
enjoy.

Also thanks for being an awesome tutor! 10/10, did recommend highly on
subject experience survey.
'''


import itertools
from random import choice, gauss
from math import floor

# construct some card set constants, might come in handy and set gymnastics is
# fun.
SUITS = set(['H', 'D', 'C', 'S'])  # hearts, diamonds, clubs, spades
NUMBERS = set([str(i) for i in range(2, 10)]).union(set(['0']))
ROYALS = set(['J', 'Q', 'K', 'A'])
RANKS = NUMBERS.union(ROYALS)
RANK_ORDER = \
    ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
ALL_CARDS = map(''.join, itertools.product(RANKS, SUITS))


def f_suit(suit):
    ''' returns an appropriate filter function based on the suit. For use
    in filter()., otherwise returns None '''

    if suit in SUITS:
        return lambda card: card[1] == suit


def cards_to_suit(cards, sort=True):
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

    assert isinstance(cards, list)
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
    ''' determines if a card is a penalty card '''
    if card == 'QS' or card[1] == 'H':
        return True
    return False


def card_gen(stop_card):
    ''' Just learnt what yield does, so here's a generator function to
    generate cards from the bottom of a suit up until a stop card.
    useful when generating runs of cards in a list:
    [card for card in card_gen(stop_card)]
    kinda messy though.
    '''

    suit = stop_card[1]
    stop_rank = stop_card[0]
    if stop_rank not in RANKS or suit not in SUITS:  # invalid end point
        return
    cards = map(''.join, itertools.product(RANKS, suit))  # generator source
    # can't use card_sort() as this isn't a list
    cards.sort(key=lambda x: RANK_ORDER.index(x[0]))  # sorted (2..ace)
    count = 0
    while True:
        card = cards[count]
        yield card
        count += 1
        if card == (stop_card):
            break


def pass_cards(hand):
    ''' Pases a 3, hopefully advantageous cards at the beginning of the round.
    Prioritises passing QKA of Spades, then the QS or 0D then if possible,
    voiding in a suit.'''

    def pick(card):
        ''' removes card from hand and places it in picked list '''
        to_pass.append(hand.pop(hand.index(card)))

    to_pass = []  # 3 cards to pass
    high_diamonds = ['AD', 'KD', 'QD', 'JD']
    keep_high_diamonds = False

    # Remove A,K,Q of Spades first
    for card in ['AS', 'KS', 'QS']:
        if card in filter(f_suit('S'), hand) and len(to_pass) < 3:
            pick(card)

    # it's hard to capture this card when in hand, so give away unless you
    # don't have a card to capture it with (A,K,Q,J of Diamonds)
    if '0D' in filter(f_suit('D'), hand) \
            and have_any_cards(high_diamonds, hand) and (len(to_pass) < 3):
        pick('0D')
        # set a flag so we know not to give these away later
        keep_high_diamonds = True

    # sort remaining suits by size
    # dictionary of {suit: [cards]}
    suit_dict = cards_to_suit(hand)
    # form a list of suits in order of how many cards each contains
    sorted_suits = sorted(suit_dict.keys(), key=lambda x: len(suit_dict[x]))

    # attempt to go void, from shortest suit to longest suit
    for suit in sorted_suits:    # dictionary of {suit: [cards]}
        # try and take highest cards first
        for card in card_sort(suit_dict[suit], rev=True):
            if len(to_pass) < 3:
                if keep_high_diamonds and card in high_diamonds:
                    continue
                else:
                    pick(card)
            else:
                return to_pass

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

        # flatten list of lists
        tricks = list(itertools.chain.from_iterable(tricklist))
        # have all the penalty cards?
        if len(filter(f_suit('H'), tricks)) == len(RANK_ORDER) \
                and ('QS' in tricks):
            return True
        return False

    scores = []
    # construct a list of final scores for each player
    for tricklist in tricks_won:
        score = 0
        for trick in tricklist:
            score += score_trick(trick)

        # did the player 'shoot the moon' (score = 26 or 16 (from 0D))?
        # if so, make them win.
        # and the award for worst player goes to...
        if score == 16 and shot_moon():  # (shot moon + 0D == 16)
            # set the new score
            score = -36  # wew, magic numbers (-26 moon shoot + -10 for 0D)
        if score == 26 and shot_moon():
            score *= -1  # turn that frown upside down!
        scores.append(score)

    # decorate the list so that each element is now a tuple of (score, Bool)
    # where Boolean True represents _a_ winning player (i.e. is equal to the
    # minumum score. (can be multiple winners)
    return [(score, (lambda x: x == min(scores))(score)) for score in scores]


def score_trick(trick):
    ''' scores a trick based on the rules set out in the spec.
            Hearts: +1 point
            Q of S: +13 points
            0 of D: -10 points
    '''
    score = 0
    score += len(filter(f_suit('H'), trick))    # number of hearts in trick
    score += 13 * ('QS' in trick)   # Queen of Spades
    score += -10 * ('0D' in trick)   # 10 of Diamonds
    return score


def play(tricks_won, played, hand, broken, is_valid=is_valid_play,
         valid_plays=get_valid_plays, score=score_game):
    ''' plays a valid card in a round of hearts according, and quite badly.
    apologies for the large amount of return branching.
    '''

    def get_round_no():
        ''' returns the current round of play based on tricks won '''
        return sum([len(tricklist) for tricklist in tricks_won])

    def must_follow():
        ''' returns a boolean status of the player being required
        to follow suit'''
        # if any lead_suit cards in valid_plays, then player must follow
        if not len(played):  # no following if it's your lead
            return False
        lead_suit = played[0][1]  # leading suit
        if len(filter(f_suit(lead_suit),
                      get_valid_plays(played, hand, broken, is_valid))):
            return True
        return False

    def get_danger():
        ''' returns a somewhat arbitrary danger level '''
        past_cards = list(itertools.chain.from_iterable(tricks_won))
        danger = 0
        danger += (13 - len(filter(f_suit('H'), played)))  # hearts remaining
        if 'QS' in played:
            danger += 5
        if 'QS' in past_cards:
            danger -= 2
        return danger

    # state-ish variables
    round_no = get_round_no()
    danger = get_danger()
    if len(played):
        lead_suit = played[0][1]  # suit that is currently leading
    else:
        lead_suit = ''
    valid_plays = get_valid_plays(played, hand, broken, is_valid)

    # play 'logic'
    # if there is only one move, make it
    if len(valid_plays) == 1:
        return valid_plays[0]   # return string not list

    # discard highest possible on opening
    if round_no == 0:
        try:
            # grab highest value valid card and get rid of it
            return card_sort(valid_plays, rev=True)[0]
        except:
            pass

    # if the 0D has been played, try to capture it
    if '0D' in played:
        # try each card in Diamonds above 0D, highest first
        # probably would be better to do: in ['JD','QD','KD','AD']
        for card in [x for x in card_gen('AD')][:-5:-1]:
            if card in valid_plays:
                return card  # return string, not list

    # if QS played, try not to win the trick
    if 'QS' in played:  # panic!
        # if don't have to follow, discard a high card safely
        if not must_follow():
            exclude = set(filter(f_suit(lead_suit), valid_plays))
            to_play = [card for card in valid_plays if card not in exclude]
            return card_sort(to_play, rev=True)[0]
        # otherwise, try card in Spades < QS, highest to lowest
        for card in reversed([x for x in card_gen('JS')]):
            if card in valid_plays:
                return card  # return string, not list

    if must_follow():  # if you must follow, play the smallest card
        if danger <= 1 or len(played) < 3:
            # note: this isn't always a good strategy
            return card_sort(valid_plays)[0]
        else:   # play biggest
            return card_sort(valid_plays, rev=True)[0]

    # attempt to throw away an off-suit high card if safe to do so
    if not must_follow():
        # grab highest value valid card and get rid of it
        exclude = set(filter(f_suit(lead_suit), valid_plays))
        to_play = [card for card in valid_plays if card not in exclude]
        if len(to_play):
            return card_sort(to_play, rev=True)[0]

    # if it's a safe-ish suit or not too dangerous and near the end of the
    # trick, make a high play.
    if lead_suit in ['S', 'C', 'D'] and danger <= 4 or \
            (len(filter(f_suit('H'), played)) == 0 and (len(played) >= 3)):
        return card_sort(valid_plays, rev=True)[0]

    # when dangerous, play smallest card
    if danger >= 4:
        return card_sort(valid_plays)[0]

    # 0/10 move
    # if all else fails, return random valid card
    # BELIEVE IN THE HEART OF THE CARDS!
    return choice(valid_plays)


def predict_score(hand):
    ''' takes a playing hand at the start of the game (after passing) and
    attempts to predict the final score based on this information alone via
    the (poor) construction of a Gaussian distribution.

    Ideally it would be nice to gather some statistical data on how this
    'player' (among others) scores based on different hands, then map the
    likeness of a given hand onto this distribution. It would be wrong to
    cause excessive load scraping the online test playground however.

    Assumptions: If holding QS, then median score is likely to be higher.
    The closer the player is to holding a full-hand of hearts (idk, but it
    sounds like a dangerous position to be in), the higher the score. Score is
    also likely to be higher if player holds 0D and no higher
    diamonds to capture with. If the player does have higher diamonds, the
    median score will be shifted toward 0 by the number of these cards.
    Score is likely to be toward 0 if starting with a hand that is void in
    1 or more suits as it offers more opportunity for safe disposals.
    If the average card in the hand has a low rank, then the score is likely
    to be lower.'''

    def clamp(score, s_min=-10, s_max=26):
        if score >= s_max:     # max score
            return s_max
        elif score <= s_min:
            return s_min
        else:
            return score

    # warning: the following section is filled with made up pseudo-statistical
    # numbers. I really wish they were magic in the 'helpful wizard' sense
    # of the word, but they're more of the 'uh...sure...okay' kind. Sorry.

    # Stand back, I'm going to try STATISTICS!
    # ... and by statistics I mean fiddling with parameters arbitrarily.

    # some (un)educated guesses at possible initial score distributions
    mu = 4  # mean initial score
    sigma = 2.5  # standard deviation in score

    hearts_count = len(filter(f_suit('H'), hand))
    mu += 0.4 * hearts_count / len(hand)
    sigma += hearts_count / 2

    # compute average card rank of hand
    hand_score = 0
    for card in hand:
        if card[0] in ROYALS:
            hand_score += 12
            mu += 1  # kind does something
        else:
            hand_score += int(card[0])
    hand_score = float(hand_score) / len(hand)  # average
    # adjust mu accordingly
    mu += (hand_score - 10)    # yep, another made up number

    # consider void suits
    void_suits = 0
    for suit in SUITS:
        if (len(filter(f_suit(suit), hand)) == 0):
            void_suits += 1

    mu -= void_suits * 3  # more likely to have a score closer to zero

    # consider Queen of Spades
    if 'QS' in hand:
        mu += (13 - mu)  # a guess at what the mean score might be closer to
        sigma -= 0.5    # more likely to occur

    # consider 10 of Diamonds, others are likely to win a trick here
    # on second thought, this kind of doesn't make sense
    if '0D' in hand:
        higher_diamonds = len([x for x in filter(f_suit('D'), hand)
                               if x in ['JD', 'QD', 'KD', 'AD']])
        mu -= 2 * (0.4 * higher_diamonds)
                   # makes it more unlikely to capture
        sigma += 0.8

    prediction = int(floor(gauss(mu, sigma)))    # compute integer score
    prediction = clamp(prediction)  # clamp to [-10..26] range
    if prediction in [26, 16]:  # may have possibly shot the moon
        if prediction == 16:
            if choice([0, 0, 1]):  # 1/3 chance of moon shoot
                return -36
            else:
                return 16
        else:
            return -26
    else:
        return int(prediction)
