import sys
from blackjack_app.models import Card, Hand
from blackjack_app.engine import BasicStrategy, CardCounter, Bankroll

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

def display_recommendation(rec: str, tc: float, edge: float):
    print("\n" + "-"*30)
    print(f"RECOMMENDATION: >>> {rec.upper()} <<<")
    print(f"Current True Count: {tc}")
    print(f"Player Edge: {edge}%")
    print("-"*30)

def handle_hand(strategy, counter, bankroll):
    print("\n--- NEW HAND ---")

    # Get unit size
    try:
        unit_size = float(input("Enter base unit size (default 10): ") or 10)
    except ValueError:
        unit_size = 10.0

    multiplier = counter.get_bet_multiplier()
    current_bet = unit_size * multiplier

    print(f"\nSuggested Bet: {multiplier} units (${current_bet})")
    if counter.true_count >= 3:
        print("*** ADVISORY: True Count is >= 3. TAKE INSURANCE if Dealer shows Ace. ***")

    d_up = get_card_input("Dealer's upcard: ")
    counter.update_count(d_up)

    p_card1 = get_card_input("Player's 1st card: ")
    counter.update_count(p_card1)
    p_card2 = get_card_input("Player's 2nd card: ")
    counter.update_count(p_card2)

    p_hand = Hand([p_card1, p_card2])

    is_split = False

    while p_hand.total < 21:
        rec = strategy.get_recommendation(p_hand, d_up)
        print(f"\nHand: {p_hand}")
        print(f"Dealer: {d_up}")
        display_recommendation(rec, counter.true_count, counter.player_edge)

        if rec == 'Stand':
            break
        if rec == 'Surrender':
            confirm = input("Surrender? (y/n): ").lower()
            if confirm == 'y':
                bankroll.subtract_loss(current_bet / 2)
                print(f"Surrendered. Lost ${current_bet / 2}")
                return
            else:
                rec = 'Hit' # Fallback if they don't surrender

        if rec == 'Split':
            print("Action: SPLIT the cards and play two hands.")
            print("For the purpose of this tracker, please continue with the FIRST hand.")
            is_split = True
            # In a real app we'd track both, but let's keep it simple and just track cards.
            # We'll just continue as if it's one hand for simplicity of the CLI flow.

        move = input("\nEnter next card (rank), 'S' to Stand, or 'D' for Double: ").strip().upper()
        if move == 'S':
            break

        if move == 'D':
            new_card = get_card_input("Enter Double Down card: ")
            counter.update_count(new_card)
            p_hand.add_card(new_card)
            current_bet *= 2
            print(f"Hand: {p_hand} (Final)")
            break

        if move in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
            new_card = Card(move)
            counter.update_count(new_card)
            p_hand.add_card(new_card)
        else:
            print("Invalid input. Continuing...")

    # Hand outcome for bankroll
    print(f"\nFinal Hand: {p_hand}")
    if p_hand.total > 21:
        print("RESULT: BUST")
        bankroll.subtract_loss(current_bet)
    else:
        outcome = input("Result? (W)in, (L)oss, (P)ush, (B)lackjack: ").strip().upper()
        if outcome == 'W':
            bankroll.add_win(current_bet)
        elif outcome == 'L':
            bankroll.subtract_loss(current_bet)
        elif outcome == 'B':
            bankroll.add_win(current_bet * 1.5)
        elif outcome == 'P':
            print("Push. No change to bankroll.")

def main():
    print_header()

    try:
        num_decks = int(input("Enter number of decks (default 6): ") or 6)
        rules = input("Dealer hits Soft 17? (y/n, default y): ").lower() != 'n'
        initial_bankroll = float(input("Enter initial bankroll (default 1000): ") or 1000)
    except ValueError:
        num_decks = 6
        rules = True
        initial_bankroll = 1000.0

    strategy = BasicStrategy(h17=rules)
    counter = CardCounter(num_decks=num_decks)
    bankroll = Bankroll(initial_balance=initial_bankroll)

    while True:
        print_header()
        print(f"BANKROLL: ${bankroll.balance:.2f} (Profit/Loss: ${bankroll.profit_loss:.2f})")
        print(f"RC: {counter.running_count} | TC: {counter.true_count} | Edge: {counter.player_edge}%")
        print(f"Recommended Bet: {counter.get_bet_multiplier()} units")
        print("-" * 50)

        print("Actions: [H] New Hand, [C] Add Other Cards, [R] Reset Count, [Q] Quit")
        action = input("Select action: ").strip().upper()

        if action == 'Q':
            break
        elif action == 'R':
            counter.reset()
            print("Count reset.")
        elif action == 'C':
            cards_str = input("Enter cards seen (comma separated, e.g. 2,A,10,5): ").split(',')
            for c in cards_str:
                c = c.strip().upper()
                if c in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                    counter.update_count(Card(c))
            print("Counts updated.")
        elif action == 'H':
            handle_hand(strategy, counter, bankroll)

if __name__ == "__main__":
    main()
