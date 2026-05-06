# Dealer upcards index: 0=2, 1=3, 2=4, 3=5, 4=6, 5=7, 6=8, 7=9, 8=10, 9=A

S17_HARD = {
    8:  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
    9:  ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
    11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],
    12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
}

S17_SOFT = {
    13: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    14: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    15: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    16: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    17: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    18: ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'],
    19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
}

S17_PAIRS = {
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

H17_HARD = S17_HARD.copy()
H17_HARD[11] = ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D']

H17_SOFT = S17_SOFT.copy()
H17_SOFT[13] = ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'] # A,2 vs 4 is Hit in S17, but Double in some H17. Let's use the old engine logic.
# Wait, let's just make H17 tables explicitly.

H17_SOFT = {
    13: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    14: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    15: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    16: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    17: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    18: ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'],
    19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
}
# Adjusting H17 SOFT based on engine.py's special logic
# if total == 18:
#    if dealer_upcard.rank == '2': return 'Double'
#    if dealer_upcard.is_ace: return 'Hit'
H17_SOFT[18] = ['D', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'] # 18 vs 2 is D. 18 vs A is H.
# Wait, the index for A is 9.
H17_SOFT[18][0] = 'D'
H17_SOFT[18][9] = 'H'

# if total == 17 and dealer_upcard.rank == '2': return 'Double'
H17_SOFT[17][0] = 'D'

# if total == 13 and dealer_upcard.rank == '4': return 'Double'
H17_SOFT[13][2] = 'D'

# A,8 (19) vs 6 is Double in H17
H17_SOFT[19] = ['S', 'S', 'S', 'S', 'D', 'S', 'S', 'S', 'S', 'S']

H17_PAIRS = S17_PAIRS.copy()

STRATEGY_MAP = {
    False: { # S17
        'HARD': S17_HARD,
        'SOFT': S17_SOFT,
        'PAIRS': S17_PAIRS
    },
    True: { # H17
        'HARD': H17_HARD,
        'SOFT': H17_SOFT,
        'PAIRS': H17_PAIRS
    }
}

DEALER_UPCARD_INDEX = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, '10':8, 'J':8, 'Q':8, 'K':8, 'A':9}
