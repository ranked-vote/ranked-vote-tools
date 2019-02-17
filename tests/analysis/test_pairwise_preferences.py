import unittest
from collections import Counter

from ranked_vote.analysis.pairwise_preferences import PreferenceMatrix
from ranked_vote.ballot import Ballot, Candidate, UNDERVOTE, OVERVOTE

CANDIDATE_A = Candidate('A')
CANDIDATE_B = Candidate('B')
CANDIDATE_C = Candidate('C')
CANDIDATE_D = Candidate('D')

CANDIDATES_ABC = [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]
CANDIDATES_ABCD = [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C, CANDIDATE_D]


class TestPairwisePreferences(unittest.TestCase):
    def test_simple_pairwise(self):
        ballots = [
            Ballot('1', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
            Ballot('2', [CANDIDATE_B, CANDIDATE_A, CANDIDATE_C]),
            Ballot('3', [CANDIDATE_C, CANDIDATE_B, CANDIDATE_A]),
            Ballot('4', [CANDIDATE_B, CANDIDATE_A, CANDIDATE_C]),
            Ballot('5', [CANDIDATE_C, CANDIDATE_B, CANDIDATE_A]),
            Ballot('6', [CANDIDATE_A, CANDIDATE_B, CANDIDATE_C]),
        ]

        matrix = PreferenceMatrix(CANDIDATES_ABC, ballots)

        self.assertEqual(CANDIDATES_ABC, matrix.candidates)

        expected_counts = Counter({
            (CANDIDATE_A, CANDIDATE_B): 2,
            (CANDIDATE_A, CANDIDATE_C): 4,
            (CANDIDATE_B, CANDIDATE_A): 4,
            (CANDIDATE_B, CANDIDATE_C): 4,
            (CANDIDATE_C, CANDIDATE_A): 2,
            (CANDIDATE_C, CANDIDATE_B): 2,
        })

        self.assertEqual(expected_counts, matrix.preferences)

        expected_graph = {
            CANDIDATE_A: {CANDIDATE_B},
            CANDIDATE_B: set(),
            CANDIDATE_C: {CANDIDATE_A, CANDIDATE_B}
        }

        self.assertEqual(expected_graph, matrix.graph)

        expected_smith = {CANDIDATE_B}
        self.assertEqual(expected_smith, matrix.smith_set)

        self.assertEqual(CANDIDATE_B, matrix.condorcet_winner)

    def test_omitted(self):
        ballots = [
            Ballot('1', [CANDIDATE_A, CANDIDATE_B]),
            Ballot('2', [CANDIDATE_B, CANDIDATE_A]),
            Ballot('3', [CANDIDATE_C, CANDIDATE_B]),
            Ballot('4', [CANDIDATE_B, CANDIDATE_A]),
            Ballot('5', [CANDIDATE_C, CANDIDATE_B]),
            Ballot('6', [CANDIDATE_A, CANDIDATE_B]),
        ]

        matrix = PreferenceMatrix(CANDIDATES_ABC, ballots)

        self.assertEqual(CANDIDATES_ABC, matrix.candidates)

        expected_counts = Counter({
            (CANDIDATE_A, CANDIDATE_B): 2,
            (CANDIDATE_A, CANDIDATE_C): 4,
            (CANDIDATE_B, CANDIDATE_A): 4,
            (CANDIDATE_B, CANDIDATE_C): 4,
            (CANDIDATE_C, CANDIDATE_A): 2,
            (CANDIDATE_C, CANDIDATE_B): 2,
        })

        self.assertEqual(expected_counts, matrix.preferences)

        expected_graph = {
            CANDIDATE_A: {CANDIDATE_B},
            CANDIDATE_B: set(),
            CANDIDATE_C: {CANDIDATE_A, CANDIDATE_B}
        }

        self.assertEqual(expected_graph, matrix.graph)

        expected_smith = {CANDIDATE_B}
        self.assertEqual(expected_smith, matrix.smith_set)

        self.assertEqual(CANDIDATE_B, matrix.condorcet_winner)

    def test_undervote_overvote(self):
        ballots = [
            Ballot('1', [CANDIDATE_A, CANDIDATE_B, UNDERVOTE]),
            Ballot('2', [CANDIDATE_B, CANDIDATE_A, OVERVOTE]),
            Ballot('3', [CANDIDATE_C, CANDIDATE_B, UNDERVOTE]),
            Ballot('4', [CANDIDATE_B, CANDIDATE_A, OVERVOTE]),
            Ballot('5', [CANDIDATE_C, CANDIDATE_B, UNDERVOTE]),
            Ballot('6', [CANDIDATE_A, CANDIDATE_B, OVERVOTE]),
        ]

        matrix = PreferenceMatrix(CANDIDATES_ABC, ballots)

        self.assertEqual(CANDIDATES_ABC, matrix.candidates)

        expected_counts = Counter({
            (CANDIDATE_A, CANDIDATE_B): 2,
            (CANDIDATE_A, CANDIDATE_C): 4,
            (CANDIDATE_B, CANDIDATE_A): 4,
            (CANDIDATE_B, CANDIDATE_C): 4,
            (CANDIDATE_C, CANDIDATE_A): 2,
            (CANDIDATE_C, CANDIDATE_B): 2,
        })

        self.assertEqual(expected_counts, matrix.preferences)

        expected_graph = {
            CANDIDATE_A: {CANDIDATE_B},
            CANDIDATE_B: set(),
            CANDIDATE_C: {CANDIDATE_A, CANDIDATE_B}
        }

        self.assertEqual(expected_graph, matrix.graph)

        expected_smith = {CANDIDATE_B}
        self.assertEqual(expected_smith, matrix.smith_set)

        self.assertEqual(CANDIDATE_B, matrix.condorcet_winner)

    def test_non_condorcet(self):
        ballots = [
            Ballot('1', [CANDIDATE_B, CANDIDATE_D, CANDIDATE_A]),
            Ballot('2', [CANDIDATE_B, CANDIDATE_D, CANDIDATE_C]),
            Ballot('3', [CANDIDATE_D, CANDIDATE_C, CANDIDATE_A]),
            Ballot('4', [CANDIDATE_D, CANDIDATE_C, CANDIDATE_B]),
            Ballot('5', [CANDIDATE_C, CANDIDATE_B, CANDIDATE_D]),
            Ballot('6', [CANDIDATE_C, CANDIDATE_B, CANDIDATE_A]),
        ]

        matrix = PreferenceMatrix(CANDIDATES_ABCD, ballots)

        expected_counts = Counter({
            (CANDIDATE_A, CANDIDATE_B): 1,
            (CANDIDATE_A, CANDIDATE_C): 1,
            (CANDIDATE_A, CANDIDATE_D): 1,
            (CANDIDATE_B, CANDIDATE_A): 5,
            (CANDIDATE_B, CANDIDATE_C): 2,
            (CANDIDATE_B, CANDIDATE_D): 4,
            (CANDIDATE_C, CANDIDATE_A): 5,
            (CANDIDATE_C, CANDIDATE_B): 4,
            (CANDIDATE_C, CANDIDATE_D): 2,
            (CANDIDATE_D, CANDIDATE_A): 5,
            (CANDIDATE_D, CANDIDATE_B): 2,
            (CANDIDATE_D, CANDIDATE_C): 4
        })

        self.assertEqual(expected_counts, matrix.preferences)

        expected_graph = {
            CANDIDATE_A: {CANDIDATE_B, CANDIDATE_C, CANDIDATE_D},
            CANDIDATE_B: {CANDIDATE_C},
            CANDIDATE_C: {CANDIDATE_D},
            CANDIDATE_D: {CANDIDATE_B},
        }

        self.assertEqual(expected_graph, matrix.graph)

        self.assertEqual(None, matrix.condorcet_winner)
