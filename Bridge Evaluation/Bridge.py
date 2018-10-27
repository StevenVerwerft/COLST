import itertools
import random
from math import ceil
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from tkinter import filedialog


class Bridge(object):

    __n_cards = 52
    __cards = list(range(__n_cards))

    # card encodings
    numbers = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    colours = ['S', 'H', 'D', 'C']

    card_coding_dic = {code_i: card for code_i, card in zip(range(52),
                                                            itertools.product(colours, numbers))}

    def __init__(self, players=4):

        self.players = players

        # each player has an empty hand at the beginning of the game
        self.current_hands = [[] for i in range(players)]
        self.adx = []
        self.distributions = self.get_distributions()

        dic = self.purpose_1and2()

        self.HP = dic['hp']
        self.dis = dic['dis']
        self.AHP = dic['ahp']

    @classmethod
    def get_card_from_encoding(cls, card_code: int):
        return cls.card_coding_dic[card_code]

    @classmethod
    def get_cardset(cls):
        return cls.__cards

    def deal(self):

        # assert that every player has an empty hand
        for player in range(self.players):
            try:
                assert not self.current_hands[player], 'player {}: hand not empty'.format(player)
            except AssertionError:
                print('Cannot deal\nHands not empty!')

                answer = input('Empty hands and deal again? (y/n?)\n>> ').lower()
                if answer == 'y':
                    self.clear_hands()
                    continue
                else:
                    print('Quitting...')
                    exit()

        # get a book of cards
        cardset = self.get_book_of_cards()

        # deal the book of cards to the players
        current_player = 0
        while cardset:

            card = random.choice(cardset)
            cardset.remove(card)
            if len(self.current_hands[current_player]) < 13:
                self.current_hands[current_player].append(card)
            else:
                current_player += 1
                if current_player > 3:
                    break
                else:
                    self.current_hands[current_player].append(card)

    def show_hands(self):

        for player in range(self.players):
            print('Hand player {}: {}'.format(player, self.current_hands[player]))

        return self.current_hands

    def show_hands_cards(self):
        """shows the actual cards instead of the encodings"""
        for player in range(self.players):
            print('Hand player {}:\n {}\n'.format(player,
                                              [self.card_coding_dic[card] for card in self.current_hands[player]]))
        return

    def show_hands_values(self):

        for player in range(self.players):
            print('Hand player {}: value = {}'.format(player, self.calculate_hand_value(self.current_hands[player])))
        return

    def show_hands_distributions(self):
        for player in range(self.players):
            print('Hand player {}: distribution = {}'.format(player,
                                                             self.get_hand_distribution(self.current_hands[player])))
        return

    def clear_hands(self):
        self.current_hands = [[] for player in range(self.players)]
        return

    def get_hand_distribution(self, hand):

        s, h, d, c = 0, 0, 0, 0
        for card in hand:
            if card < 13:
                s += 1
            elif card < 26:
                h += 1
            elif card < 39:
                d += 1
            else:
                c += 1
        return sorted([s, h, d, c], reverse=True)

    def calculate_hand_value(self, hand):

        HP = 0
        for card in hand:
            HP += max(0, 4 - (card % 13))
        return HP

    def purpose_1(self):
        """
            calculate as efficiently as possible the amount of Honour Points for each hand j (0-4)
            for each deal i (0-2499)
        """
        try:
            assert not any(self.current_hands), 'not all hands are empty!'
        except AssertionError:
            print('clearing hands')
            self.clear_hands()

        ndeals = 2500
        HP = []

        for deal in range(ndeals):
            HP.append([])
            self.deal()
            for player in range(self.players):
                HP[deal].append(self.calculate_hand_value(self.current_hands[player]))

            self.clear_hands()
        return HP

    def purpose_2(self):

        """
            indicate as efficiently as possible the distribution number for each of the hands j (0-3)
            for each deal i (0-2499)
        """
        try:
            assert not any(self.current_hands), 'not all hands empty'
        except AssertionError:
            print('Clearing hands')
            self.clear_hands()

        ndeals = 2500
        dis = []

        for deal in range(ndeals):
            dis.append([])
            self.deal()
            for player in range(self.players):
                dis[deal].append(self.distributions.index(self.get_hand_distribution(self.current_hands[player])))
            self.clear_hands()
        self.DIS = dis
        return dis

    def purpose_1and2(self):

        try:
            assert not any(self.current_hands), 'not all hands empty'
        except AssertionError:
            print('clearing hands')
            self.clear_hands()

        ndeals = 2500
        dis = []
        hp = []
        ahp = []
        for deal in range(ndeals):
            dis.append([])
            hp.append([])
            ahp.append([])

            self.deal()
            for player in range(self.players):

                hand_dis = self.distributions.index(self.get_hand_distribution(self.current_hands[player]))
                hand_hp = self.calculate_hand_value(self.current_hands[player])

                dis[deal].append(hand_dis)
                hp[deal].append(hand_hp)
                ahp[deal].append(hand_hp + self.adx[hand_dis])

            self.clear_hands()

        return {'dis': dis, 'hp': hp, 'ahp': ahp}

    def calculate_ahp(self):
        return

    @staticmethod
    def get_book_of_cards():
        return list(range(52))

    def get_distributions(self):

        distributions = list()
        self.adx = []  # used for calculating adjusted HP

        for i1 in range(ceil(13 / 4), 14):
            to_dist1 = 13 - i1
            for i2 in range(ceil(to_dist1 / 3), to_dist1+1):
                if i2 > i1:
                    break
                to_dist2 = to_dist1 - i2
                for i3 in range(ceil(to_dist2 / 2), to_dist2+1):
                    if i3 > i2:
                        break

                    to_dist3 = to_dist2 - i3
                    self.adx.append(i1 + i2 - 8)
                    distributions.append([i1, i2, i3, to_dist3])

        return distributions

    def visualize(self, option="p1", size=(16, 9)):

        fig = plt.figure(figsize=size)

        if option.lower() == 'p1':

            data = pd.DataFrame(np.asarray(self.purpose_1()), columns=['player1', 'player 2',
                                                                       'player 3', 'player 4'])
            data = data.melt(value_name='hand value', var_name='player')
            sns.countplot(x='hand value', data=data, hue='player')

        if option.lower() == 'p2':

            data = pd.DataFrame(np.asarray(self.purpose_2()), columns=['player 1', 'player 2',
                                                                       'player 3', 'player 4'])
            data = data.melt(value_name='hand distribution', var_name='player')  # go to long format
            sns.countplot(x='hand distribution', data=data, hue='player')

        plt.show()

    def read_rules(self, path='rules.txt'):

        if os.path.exists(path):
            file = open(path, 'r')
        else:
            path = filedialog.askopenfilename(initialdir='./')
            file = open(path, 'r')

        rules = file.readlines()
        file.close()
        rules = [rule.split()[:-1] for rule in rules]  # fix this because it omits the last line
        for rule in rules:
            print(rule)