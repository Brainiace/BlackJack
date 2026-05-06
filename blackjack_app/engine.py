from .models import Hand, Card
from .strategy_tables import STRATEGY_MAP, DEALER_UPCARD_INDEX

class CardCounter:
    """
    Implements Hi-Lo card counting logic and True Count calculation.
    """
    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks
        self.running_count = 0
        self.cards_dealt = 0

    def update_count(self, card: Card):
        """Updates the running count based on the card dealt."""
        val = card.value
        # 2-6 = +1, 10-A = -1, 7-9 = 0
        if 2 <= val <= 6:
            self.running_count += 1
        elif val >= 10 or card.is_ace:
            self.running_count -= 1
        self.cards_dealt += 1

    @property
    def true_count(self) -> float:
        """Calculates the True Count: Running Count / Decks Remaining."""
        total_cards = self.num_decks * 52
        cards_remaining = total_cards - self.cards_dealt
        decks_remaining = max(cards_remaining / 52, 0.01) # Avoid division by zero
        return round(self.running_count / decks_remaining, 2)

    @property
    def player_edge(self) -> float:
        """
        Estimates player edge based on True Count.
        Basic Strategy House Edge is ~-0.5%.
        Each point of True Count adds ~0.5% to player edge.
        """
        return round(-0.5 + (0.5 * self.true_count), 2)

    def get_bet_multiplier(self) -> int:
        """
        Kelly Criterion-lite formula:
        Bet units = (Player Edge * 100) rounded to nearest whole number, min 1.
        Example: 1% edge -> 2 units (conservative Kelly) or directly use edge.
        Let's follow a simple progressive scale based on edge.
        """
        edge = self.player_edge
        if edge <= 0:
            return 1
        # Simple Kelly-lite: multiplier = 1 + edge * 10
        # If edge is 0.5%, multiplier = 1 + 5 = 6? No, let's use the requirement from counter.py as base or similar.
        # But Agent.md says "Kelly Criterion-lite formula".
        # Standard simple Kelly: Bet % = Edge / Variance. Blackjack variance is ~1.15.
        # So Bet % approx = Edge.
        # If edge is 1%, bet 1% of bankroll.
        # In units, if 1 unit is 0.25% of bankroll, then 1% edge = 4 units.

        # Let's use a scale:
        # TC 1 (0% edge): 1 unit
        # TC 2 (0.5% edge): 2 units
        # TC 3 (1.0% edge): 4 units
        # TC 4 (1.5% edge): 8 units
        # TC 5+ (2.0%+ edge): 12 units
        tc = self.true_count
        if tc < 1: return 1
        if tc < 2: return 2
        if tc < 3: return 4
        if tc < 4: return 8
        return 12

    def reset(self):
        self.running_count = 0
        self.cards_dealt = 0

class Bankroll:
    """Manages the player's virtual bankroll."""
    def __init__(self, initial_balance: float = 1000.0):
        self.balance = initial_balance
        self.initial_balance = initial_balance

    def add_win(self, amount: float):
        self.balance += amount

    def subtract_loss(self, amount: float):
        self.balance -= amount

    @property
    def profit_loss(self) -> float:
        return self.balance - self.initial_balance

class BasicStrategy:
    """
    Implements Blackjack Basic Strategy using optimized lookup tables.
    """
    def __init__(self, h17: bool = True):
        self.h17 = h17
        self.tables = STRATEGY_MAP[h17]

    def get_recommendation(self, player_hand: Hand, dealer_upcard: Card) -> str:
        d_idx = DEALER_UPCARD_INDEX.get(dealer_upcard.rank)

        # 1. Splitting
        if player_hand.is_pair and len(player_hand.cards) == 2:
            card_rank = player_hand.cards[0].rank
            if card_rank in ['J', 'Q', 'K']: card_rank = '10'
            rec = self.tables['PAIRS'][card_rank][d_idx]
            if rec == 'P': return 'Split'

        # 2. Soft Totals
        if player_hand.is_soft:
            total = player_hand.total
            if total >= 21: return 'Stand'
            rec = self.tables['SOFT'].get(total, 'H')[d_idx]
            if rec == 'D': return 'Double' if len(player_hand.cards) == 2 else 'Hit'
            if rec == 'S': return 'Stand'
            return 'Hit'

        # 3. Hard Totals
        total = player_hand.total
        if total <= 8: return 'Hit'

        if total in self.tables['HARD']:
            rec = self.tables['HARD'][total][d_idx]
            if rec == 'R': return 'Surrender' if len(player_hand.cards) == 2 else ('Hit' if total <= 16 else 'Stand')
            if rec == 'D': return 'Double' if len(player_hand.cards) == 2 else 'Hit'
            if rec == 'S': return 'Stand'
            if rec == 'H': return 'Hit'

        if total >= 17: return 'Stand'
        return 'Hit'
