from .models import Hand, Card

class BasicStrategy:
    """
    Implements Blackjack Basic Strategy for H17 and S17 rules.
    Recommendations: 'H' (Hit), 'S' (Stand), 'D' (Double), 'P' (Split).
    """

    # Tables for Hard Totals (rows: player total 8-17, columns: dealer upcard 2-A)
    # dealer_upcards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
    HARD_TOTALS = {
        8:  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        9:  ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
        10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
        11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],
        12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
        17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], # 17+ is always stand
    }

    # Tables for Soft Totals (rows: player A+2 to A+9, columns: dealer upcard 2-A)
    SOFT_TOTALS = {
        13: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A,2
        14: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A,3
        15: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A,4
        16: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A,5
        17: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'], # A,6
        18: ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'], # A,7 (S17)
        19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], # A,8
        20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'], # A,9
    }

    # Tables for Pairs (rows: 2,2 to A,A, columns: dealer upcard 2-A)
    PAIRS = {
        '2': ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
        '3': ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
        '4': ['H', 'H', 'H', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
        '5': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
        '6': ['P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
        '7': ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
        '8': ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        '9': ['P', 'P', 'P', 'P', 'P', 'S', 'P', 'P', 'S', 'S'],
        '10':['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        'A': ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    }

    def __init__(self, h17: bool = True):
        self.h17 = h17
        self.dealer_map = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, '10':8, 'J':8, 'Q':8, 'K':8, 'A':9}

    def get_recommendation(self, player_hand: Hand, dealer_upcard: Card) -> str:
        d_idx = self.dealer_map.get(dealer_upcard.rank)
        if d_idx is None:
             d_idx = 8 if dealer_upcard.value == 10 else 9

        # 1. Splitting
        if player_hand.is_pair and len(player_hand.cards) == 2:
            card_rank = player_hand.cards[0].rank
            if card_rank in ['J', 'Q', 'K']: card_rank = '10'
            rec = self.PAIRS[card_rank][d_idx]
            if rec == 'P': return 'Split'

        # 2. Soft Totals
        if player_hand.is_soft:
            total = player_hand.total
            if total >= 20: return 'Stand'
            if total == 19:
                # A,8 vs 6 is Double in H17
                if self.h17 and dealer_upcard.rank == '6' and len(player_hand.cards) == 2:
                    return 'Double'
                return 'Stand'

            rec = self.SOFT_TOTALS.get(total, ['H']*10)[d_idx]

            # H17 adjustments
            if self.h17:
                if total == 18:
                    if dealer_upcard.rank == '2': return 'Double' if len(player_hand.cards) == 2 else 'Stand'
                    if dealer_upcard.is_ace: return 'Hit'
                if total == 17 and dealer_upcard.rank == '2': return 'Double' if len(player_hand.cards) == 2 else 'Hit'
                if total == 13 and dealer_upcard.rank == '4': return 'Double' if len(player_hand.cards) == 2 else 'Hit'

            if rec == 'D': return 'Double' if len(player_hand.cards) == 2 else 'Hit'
            if rec == 'S': return 'Stand'
            return 'Hit'

        # 3. Hard Totals
        total = player_hand.total
        if total >= 17: return 'Stand'
        if total <= 8: return 'Hit'

        # H17 adjustment for Hard 11 vs Ace
        if total == 11 and self.h17 and dealer_upcard.is_ace and len(player_hand.cards) == 2:
            return 'Double'

        rec = self.HARD_TOTALS[total][d_idx]
        if rec == 'D': return 'Double' if len(player_hand.cards) == 2 else 'Hit'
        if rec == 'S': return 'Stand'
        return 'Hit'
