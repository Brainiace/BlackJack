from .models import Card

class CardCounter:
    """
    Implements Hi-Lo card counting logic.
    2-6 = +1
    7-9 = 0
    10-Ace = -1
    """
    def __init__(self, num_decks: int = 6):
        self.num_decks = num_decks
        self.running_count = 0
        self.cards_dealt = 0

    def update_count(self, card: Card):
        """Updates the running count based on the card dealt."""
        val = card.value
        if 2 <= val <= 6:
            self.running_count += 1
        elif val >= 10 or card.is_ace:
            self.running_count -= 1
        # 7, 8, 9 are 0
        self.cards_dealt += 1

    @property
    def true_count(self) -> float:
        """Calculates the True Count based on remaining decks."""
        total_cards = self.num_decks * 52
        cards_remaining = total_cards - self.cards_dealt
        decks_remaining = cards_remaining / 52

        # Avoid division by zero and return 0 if no cards remain (though unlikely in practice)
        if decks_remaining <= 0:
            return float(self.running_count)

        # Rounding to nearest half deck is common, but here we'll use exact for precision
        # or round to 1 decimal place.
        return round(self.running_count / decks_remaining, 2)

    def get_bet_multiplier(self) -> int:
        """
        Suggests a bet multiplier based on the True Count.
        TC < 1: 1 unit
        TC 1-2: 2 units
        TC 2-3: 4 units
        TC 3-4: 8 units
        TC > 4: 12 units (or max)
        """
        tc = self.true_count
        if tc < 1:
            return 1
        if 1 <= tc < 2:
            return 2
        if 2 <= tc < 3:
            return 4
        if 3 <= tc < 4:
            return 8
        return 12

    @property
    def player_edge(self) -> float:
        """
        Estimates player edge based on True Count.
        Basic Strategy House Edge is ~-0.5%.
        Each point of True Count adds ~0.5% to player edge.
        """
        return round(-0.5 + (0.5 * self.true_count), 2)

    def reset(self):
        self.running_count = 0
        self.cards_dealt = 0
