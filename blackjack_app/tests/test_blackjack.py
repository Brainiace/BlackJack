import pytest
from blackjack_app.models import Card, Hand
from blackjack_app.engine import BasicStrategy
from blackjack_app.counter import CardCounter

def test_card_values():
    assert Card('A').value == 11
    assert Card('K').value == 10
    assert Card('10').value == 10
    assert Card('5').value == 5

def test_hand_total():
    hand = Hand([Card('A'), Card('9')])
    assert hand.total == 20
    assert hand.is_soft == True

    hand.add_card(Card('5'))
    assert hand.total == 15
    assert hand.is_soft == False

def test_basic_strategy_hard():
    strategy = BasicStrategy(h17=True)
    # 11 vs 10
    hand = Hand([Card('6'), Card('5')])
    dealer = Card('10')
    assert strategy.get_recommendation(hand, dealer) == 'Double'

    # 16 vs 7
    hand = Hand([Card('10'), Card('6')])
    dealer = Card('7')
    assert strategy.get_recommendation(hand, dealer) == 'Hit'

    # 16 vs 6
    dealer = Card('6')
    assert strategy.get_recommendation(hand, dealer) == 'Stand'

def test_basic_strategy_soft():
    strategy = BasicStrategy(h17=True)
    # A,7 (18) vs 2 (H17)
    hand = Hand([Card('A'), Card('7')])
    dealer = Card('2')
    assert strategy.get_recommendation(hand, dealer) == 'Double'

    # A,7 (18) vs 9
    dealer = Card('9')
    assert strategy.get_recommendation(hand, dealer) == 'Hit'

def test_basic_strategy_pairs():
    strategy = BasicStrategy()
    # 8,8 vs Ace
    hand = Hand([Card('8'), Card('8')])
    dealer = Card('A')
    assert strategy.get_recommendation(hand, dealer) == 'Split'

    # 10,10 vs 6
    hand = Hand([Card('10'), Card('10')])
    dealer = Card('6')
    assert strategy.get_recommendation(hand, dealer) == 'Stand'

def test_card_counter():
    counter = CardCounter(num_decks=1)
    # Deal some low cards
    for _ in range(5):
        counter.update_count(Card('2'))

    assert counter.running_count == 5
    # 52 - 5 = 47 cards left. 47/52 = 0.90 decks
    # TC = 5 / 0.90 = 5.55
    assert counter.true_count == 5.53 # 5 / (47/52) = 5.5319...
    assert counter.get_bet_multiplier() == 12
