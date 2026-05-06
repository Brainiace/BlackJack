import pytest
from blackjack_app.models import Card, Hand
from blackjack_app.engine import BasicStrategy, CardCounter, Bankroll

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

def test_surrender_logic():
    # S17 16 vs 10
    strategy_s17 = BasicStrategy(h17=False)
    hand = Hand([Card('10'), Card('6')])
    dealer = Card('10')
    assert strategy_s17.get_recommendation(hand, dealer) == 'Surrender'

    # H17 15 vs Ace
    strategy_h17 = BasicStrategy(h17=True)
    hand = Hand([Card('10'), Card('5')])
    dealer = Card('A')
    assert strategy_h17.get_recommendation(hand, dealer) == 'Surrender'

    # Surrender only on first two cards (simulated in engine by checking len(cards)==2)
    hand.add_card(Card('2')) # total 17, but 3 cards
    assert strategy_h17.get_recommendation(hand, dealer) == 'Stand' # Table says R for 17 vs A in H17, but len > 2 means Stand (since 17)

def test_card_counter():
    counter = CardCounter(num_decks=1)
    # Deal some low cards
    for _ in range(5):
        counter.update_count(Card('2'))

    assert counter.running_count == 5
    # 52 - 5 = 47 cards left. 47/52 = 0.9038 decks
    # TC = 5 / 0.9038 = 5.532...
    assert counter.true_count == 5.53
    assert counter.get_bet_multiplier() == 12

def test_kelly_criterion_lite():
    counter = CardCounter(num_decks=6)
    # TC 0: 1 unit
    assert counter.get_bet_multiplier() == 1

    # TC 2: 4 units (based on my implementation)
    # We need TC to be around 2.
    # 6 decks = 312 cards.
    # If we deal 52 cards, 5 decks left. RC 10 -> TC 2.
    for _ in range(10):
        counter.update_count(Card('2')) # RC 10
    for _ in range(42):
        counter.update_count(Card('7')) # RC 10, 52 cards dealt

    assert counter.true_count == 2.0
    assert counter.get_bet_multiplier() == 4

def test_bankroll():
    bankroll = Bankroll(1000)
    bankroll.add_win(100)
    assert bankroll.balance == 1100
    assert bankroll.profit_loss == 100

    bankroll.subtract_loss(50)
    assert bankroll.balance == 1050
    assert bankroll.profit_loss == 50
