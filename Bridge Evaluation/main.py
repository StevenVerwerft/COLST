from Bridge import Bridge
import matplotlib.pyplot as plt

def main():

    bridgegame = Bridge()
    bridgegame.deal()
    bridgegame.show_hands()
    bridgegame.show_hands_cards()
    bridgegame.show_hands_values()
    bridgegame.show_hands_distributions()
    bridgegame.read_rules()

    return


if __name__ == '__main__':
    main()
