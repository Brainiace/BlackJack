from typing import List

class Card:
    """Represents a playing card."""
    def __init__(self, rank: str):
        self.rank = rank.upper()
        self.value = self._set_value()
        self.is_ace = self.rank == 'A'

    def _set_value(self) -> int:
        if self.rank in ['J', 'Q', 'K', '10']:
            return 10
        if self.rank == 'A':
            return 11
        try:
            return int(self.rank)
        except ValueError:
            raise ValueError(f"Invalid card rank: {self.rank}")

    def __repr__(self):
        return self.rank

class Hand:
    """Represents a blackjack hand."""
    def __init__(self, cards: List[Card] = None):
        self.cards = cards or []

    def add_card(self, card: Card):
        self.cards.append(card)

    @property
    def values(self) -> List[int]:
        return [c.value for c in self.cards]

    @property
    def total(self) -> int:
        """Calculates the best possible total for the hand."""
        total = sum(c.value for c in self.cards)
        aces = sum(1 for c in self.cards if c.is_ace)
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    @property
    def is_soft(self) -> bool:
        """A hand is soft if it contains an Ace valued at 11 without busting."""
        total = sum(c.value for c in self.cards)
        aces = sum(1 for c in self.cards if c.is_ace)
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        # If we have at least one ace, and the total with one ace as 11 is still <= 21
        # Hard total is sum where all aces are 1.
        hard_total = sum(c.value if not c.is_ace else 1 for c in self.cards)
        return any(c.is_ace for c in self.cards) and (hard_total + 10 <= 21)

    @property
    def is_pair(self) -> bool:
        """Checks if the hand is a pair (two cards of the same value)."""
        return len(self.cards) == 2 and self.cards[0].value == self.cards[1].value

    def __repr__(self):
        return f"{[c.rank for c in self.cards]} (Total: {self.total}{' Soft' if self.is_soft else ''})"
