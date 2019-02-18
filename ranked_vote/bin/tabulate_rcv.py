import argparse
from json import dumps

from ranked_vote.format import read_ballots
from ranked_vote.methods import METHODS


def run_tabulation(rcv_file, method):
    ballots = read_ballots(rcv_file)
    tabulation = METHODS[method](ballots)
    print('Winner:', tabulation.winner)
    print('Rounds:')
    print(dumps([r.to_dict() for r in tabulation.rounds], indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('rcv_file')
    parser.add_argument('--method', default='irv')
    run_tabulation(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
