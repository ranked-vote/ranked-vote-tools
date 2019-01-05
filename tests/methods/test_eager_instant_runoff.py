from unittest import TestCase

from ranked_vote.ballot import Ballot, Candidate
from ranked_vote.methods.eager_instant_runoff import EagerInstantRunoff

CANDIDATE_A = Candidate('A')
CANDIDATE_B = Candidate('B')
CANDIDATE_C = Candidate('C')
CANDIDATE_D = Candidate('D')
CANDIDATE_E = Candidate('E')
CANDIDATE_F = Candidate('F')


class TestEagerInstantRunoff(TestCase):
    def test_multiple_runoff_rounds(self):
        ballots = [
            Ballot('1', [CANDIDATE_A]),
            Ballot('2', [CANDIDATE_A]),
            Ballot('3', [CANDIDATE_A]),
            Ballot('4', [CANDIDATE_A]),
            Ballot('5', [CANDIDATE_B]),
            Ballot('6', [CANDIDATE_B]),
            Ballot('7', [CANDIDATE_B]),
            Ballot('8', [CANDIDATE_C]),
            Ballot('9', [CANDIDATE_C]),
            Ballot('10', [CANDIDATE_D]),
        ]

        irv = EagerInstantRunoff(ballots)
        self.assertEqual(CANDIDATE_A, irv.winner)
        self.assertEqual(3, len(irv.rounds))

        self.assertEqual(10, irv.rounds[0].total_votes)
        self.assertEqual(10, irv.rounds[0].total_ballots)
        self.assertEqual(1, irv.rounds[0].round)
        self.assertEqual([], irv.rounds[0].last_eliminated)

        self.assertEqual(9, irv.rounds[1].total_votes)
        self.assertEqual(10, irv.rounds[1].total_ballots)
        self.assertEqual(2, irv.rounds[1].round)
        self.assertEqual([CANDIDATE_D], irv.rounds[1].last_eliminated)

        self.assertEqual(7, irv.rounds[2].total_votes)
        self.assertEqual(10, irv.rounds[2].total_ballots)
        self.assertEqual(3, irv.rounds[2].round)
        self.assertEqual([CANDIDATE_C], irv.rounds[2].last_eliminated)

    def test_simple_eager_runoff(self):
        ballots = [
            Ballot('1', [CANDIDATE_A]),
            Ballot('2', [CANDIDATE_A]),
            Ballot('3', [CANDIDATE_A]),
            Ballot('4', [CANDIDATE_A]),
            Ballot('5', [CANDIDATE_B]),
            Ballot('6', [CANDIDATE_B]),
            Ballot('7', [CANDIDATE_B]),
            Ballot('8', [CANDIDATE_B]),
            Ballot('9', [CANDIDATE_C, CANDIDATE_B]),
            Ballot('10', [CANDIDATE_D, CANDIDATE_B]),
        ]

        irv = EagerInstantRunoff(ballots)
        self.assertEqual(CANDIDATE_B, irv.winner)
        self.assertEqual(2, len(irv.rounds))

        self.assertEqual(10, irv.rounds[0].total_votes)
        self.assertEqual(10, irv.rounds[0].total_ballots)
        self.assertEqual(1, irv.rounds[0].round)
        self.assertEqual([], irv.rounds[0].last_eliminated)

        self.assertEqual(10, irv.rounds[1].total_votes)
        self.assertEqual(10, irv.rounds[1].total_ballots)
        self.assertEqual(2, irv.rounds[1].round)
        self.assertEqual([CANDIDATE_C, CANDIDATE_D], irv.rounds[1].last_eliminated)
