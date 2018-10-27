"""
    helps with retrieving card encodings
"""
import itertools

number_coding = {
    'A': [0 + 13 * i for i in range(4)],
    'K': [1 + 13 * i for i in range(4)],
    'Q': [2 + 13 * i for i in range(4)],
    'J': [3 + 13 * i for i in range(4)],
    'T': [4 + 13 * i for i in range(4)],
    '9': [5 + 13 * i for i in range(4)],
    '8': [6 + 13 * i for i in range(4)],
    '7': [7 + 13 * i for i in range(4)],
    '6': [8 + 13 * i for i in range(4)],
    '5': [9 + 13 * i for i in range(4)],
    '4': [10 + 13 * i for i in range(4)],
    '3': [11 + 13 * i for i in range(4)],
    '2': [12 + 13 * i for i in range(4)],
}

colour_coding = {
    'Spades': list(range(13)),
    'Hearts': list(range(13, 26)),
    'Diamonds': list(range(26, 39)),
    'Clubs': list(range(39, 52)),
}

numbers = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
colours = ['Spades', 'Hearts', 'Diamonds', 'Clubs']


coding_dic = {code_i: card for code_i, card in zip(range(52), itertools.product(colours, numbers))}
