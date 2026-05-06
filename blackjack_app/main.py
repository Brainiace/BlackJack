import sys
from blackjack_app.models import Card, Hand
from blackjack_app.engine import BasicStrategy
from blackjack_app.counter import CardCounter

def print_header():
    print("\n" + "="*50)
    print("      BLACKJACK STRATEGY & CARD COUNTER")
    print("="*50)

def get_card_input(prompt: str) -> Card:
    while True:
        rank = input(prompt).strip().upper()
        if rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
            return Card(rank)
        print("Invalid card rank. Use 2-10, J, Q, K, or A.")

def main():
    print_header()

    try:
        num_decks = int(input("Enter number of decks in shoe (default 6): ") or 6)
        rules = input("Dealer hits Soft 17? (y/n, default y): ").lower() != 'n'
    except ValueError:
        num_decks = 6
        rules = True

    strategy = BasicStrategy(h17=rules)
    counter = CardCounter(num_decks=num_decks)

    while True:
        print_header()
        print(f"Running Count: {counter.running_count}")
        print(f"True Count:    {counter.true_count}")
        print(f"Player Edge:   {counter.player_edge}%")
        print(f"Suggested Bet: {counter.get_bet_multiplier()} units")
        print("-" * 50)

        print("Actions: [C] Add Card, [H] New Hand, [R] Reset Count, [Q] Quit")
        action = input("Select action: ").strip().upper()

        if action == 'Q':
            break
        elif action == 'R':
            counter.reset()
            print("Count reset.")
            continue
        elif action == 'C':
            card = get_card_input("Enter card rank: ")
            counter.update_count(card)
        elif action == 'H':
            # Basic Strategy Recommendation for a new hand
            print("\n--- NEW HAND ---")
            d_up = get_card_input("Dealer's upcard: ")
            counter.update_count(d_up)

            p_card1 = get_card_input("Player's first card: ")
            counter.update_count(p_card1)
            p_card2 = get_card_input("Player's second card: ")
            counter.update_count(p_card2)

            p_hand = Hand([p_card1, p_card2])

            while p_hand.total < 21:
                rec = strategy.get_recommendation(p_hand, d_up)
                print(f"\nHand: {p_hand}")
                print(f"Dealer: {d_up}")
                print(f"RECOMMENDATION: >>> {rec} <<<")

                if rec == 'Stand':
                    break

                move = input("\nEnter next card dealt to player (or 'S' to Stand, 'D' for Double card, 'rank' for Hit): ").strip().upper()
                if move == 'S':
                    break

                if move == 'D':
                    new_card = get_card_input("Enter the double down card: ")
                elif move in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                    new_card = Card(move)
                else:
                    print("Invalid input. Use card rank or S/D.")
                    continue

                if new_card:
                    counter.update_count(new_card)
                    p_hand.add_card(new_card)

                if move == 'D' or rec == 'Double':
                    print(f"Final Hand: {p_hand}")
                    break

            if p_hand.total > 21:
                print(f"Hand: {p_hand} - BUSTED")
            elif p_hand.total == 21:
                print(f"Hand: {p_hand} - BLACKJACK/21")

            input("\nPress Enter to continue tracking other cards...")

if __name__ == "__main__":
    main()
