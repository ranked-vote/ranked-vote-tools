import unittest

from ranked_vote.ballot import Ballot, Candidate, UNDERVOTE, OVERVOTE, WRITE_IN, parse_choice


class TestCandidateParse(unittest.TestCase):
    def test_parse_special_choices(self):
        self.assertIs(UNDERVOTE, parse_choice('$UNDERVOTE'))
        self.assertIs(OVERVOTE, parse_choice('$OVERVOTE'))
        self.assertIs(WRITE_IN, parse_choice('$WRITE_IN'))

    def test_parse_same_object(self):
        self.assertIs(Candidate.get('Jane'), parse_choice('Jane'))
