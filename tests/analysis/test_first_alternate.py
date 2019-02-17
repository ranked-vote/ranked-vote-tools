import unittest
from collections import Counter

from ranked_vote.analysis.first_alternate import FirstAlternates
from ranked_vote.analysis.pairwise_stat import PairwiseStat
from ranked_vote.ballot import Ballot, Candidate, UNDERVOTE, OVERVOTE

CANDIDATE_A = Candidate('A')
CANDIDATE_B = Candidate('B')
CANDIDATE_C = Candidate('C')

CANDIDATES = [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]


class TestFirstAlternate(unittest.TestCase):
    def test_simple_case(self):
        ballots = [
            Ballot('1', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('2', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('3', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('4', [CANDIDATE_B, CANDIDATE_A, CANDIDATE_C]),
            Ballot('5', [CANDIDATE_B, CANDIDATE_A, CANDIDATE_C]),
            Ballot('6', [CANDIDATE_B, CANDIDATE_A, CANDIDATE_C]),
            Ballot('7', [CANDIDATE_A, CANDIDATE_C, CANDIDATE_B]),
            Ballot('8', [CANDIDATE_A, CANDIDATE_C, CANDIDATE_B]),
            Ballot('9', [CANDIDATE_A, CANDIDATE_C, CANDIDATE_B]),
        ]

        first_alternates = FirstAlternates(CANDIDATES, ballots)

        expected = Counter({
            (CANDIDATE_A, CANDIDATE_B): 3,
            (CANDIDATE_A, CANDIDATE_C): 3,
            (CANDIDATE_B, CANDIDATE_A): 3
        })

        self.assertEqual(expected, first_alternates._counts)

        expected_ps = [
            PairwiseStat(CANDIDATE_A, CANDIDATE_B, 3, 6),
            PairwiseStat(CANDIDATE_A, CANDIDATE_C, 3, 6),
            PairwiseStat(CANDIDATE_B, CANDIDATE_A, 3, 3),
            PairwiseStat(CANDIDATE_B, CANDIDATE_C, 0, 3),
            PairwiseStat(CANDIDATE_C, CANDIDATE_A, 0, 0),
            PairwiseStat(CANDIDATE_C, CANDIDATE_B, 0, 0),
        ]

        self.assertEqual(expected_ps, first_alternates.pairwise)

    def test_undervote(self):
        ballots = [
            Ballot('1', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('2', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('3', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('4', [CANDIDATE_B, CANDIDATE_A, CANDIDATE_C]),
            Ballot('5', [CANDIDATE_B, UNDERVOTE]),
        ]

        first_alternates = FirstAlternates(CANDIDATES, ballots)

        expected = Counter({
            (CANDIDATE_A, CANDIDATE_B): 3,
            (CANDIDATE_B, CANDIDATE_A): 1,
            (CANDIDATE_B, UNDERVOTE): 1,
        })

        self.assertEqual(expected, first_alternates._counts)

    def test_implicit_undervote(self):
        ballots = [
            Ballot('1', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('2', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('3', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('4', [CANDIDATE_B, CANDIDATE_A, CANDIDATE_C]),
            Ballot('5', [CANDIDATE_B]),
        ]

        first_alternates = FirstAlternates(CANDIDATES, ballots)

        expected = Counter({
            (CANDIDATE_A, CANDIDATE_B): 3,
            (CANDIDATE_B, CANDIDATE_A): 1,
            (CANDIDATE_B, UNDERVOTE): 1,
        })

        self.assertEqual(expected, first_alternates._counts)

    def test_overvote(self):
        ballots = [
            Ballot('1', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('2', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('3', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('4', [CANDIDATE_B, CANDIDATE_A, CANDIDATE_C]),
            Ballot('5', [CANDIDATE_B, OVERVOTE]),
        ]

        first_alternates = FirstAlternates(CANDIDATES, ballots)

        expected = Counter({
            (CANDIDATE_A, CANDIDATE_B): 3,
            (CANDIDATE_B, CANDIDATE_A): 1,
            (CANDIDATE_B, UNDERVOTE): 1,
        })

        self.assertEqual(expected, first_alternates._counts)
