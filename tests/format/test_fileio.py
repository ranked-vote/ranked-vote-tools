import unittest
from os import path
from tempfile import TemporaryDirectory

from ranked_vote.ballot import Ballot, Candidate, UNDERVOTE, OVERVOTE, WRITE_IN
from ranked_vote.format import read_ballots, write_ballots


class TestRoundTrip(unittest.TestCase):
    def test_round_trip_csv(self):
        ballots = [
            Ballot('1', [Candidate('A'), UNDERVOTE, Candidate('C')]),
            Ballot('2', [Candidate('D'), WRITE_IN, OVERVOTE]),
        ]

        with TemporaryDirectory() as td:
            filename = path.join(td, 'ballots.csv')
            write_ballots(filename, ballots)

            rt_ballots = list(read_ballots(filename))

        self.assertEqual(ballots, rt_ballots)

    def test_round_trip_gz(self):
        ballots = [
            Ballot('1', [Candidate('A'), UNDERVOTE, Candidate('C')]),
            Ballot('2', [Candidate('D'), WRITE_IN, OVERVOTE]),
        ]

        with TemporaryDirectory() as td:
            filename = path.join(td, 'ballots.csv.gz')
            write_ballots(filename, ballots)

            rt_ballots = list(read_ballots(filename))

        self.assertEqual(ballots, rt_ballots)
