import unittest
from io import StringIO
from ranked_vote_tools.ballot import Ballot, Candidate, UNDERVOTE, OVERVOTE, WRITE_IN
from ranked_vote_tools.files import write_ballots_fh
from typing import List


def fh_to_lines(fh: StringIO) -> List[str]:
    return fh.getvalue().split('\n')[:-1]


class TestReadBallots(unittest.TestCase):
    def test_simple_ballots(self):
        ballots = [
            Ballot('1', [Candidate('A'), Candidate('B'), Candidate('C')]),
            Ballot('2', [Candidate('D'), Candidate('E'), Candidate('F')]),
        ]

        buffer = StringIO()
        write_ballots_fh(buffer, ballots)

        self.assertEqual([
            'ballot_id,rank,choice',
            '1,1,A',
            '1,2,B',
            '1,3,C',
            '2,1,D',
            '2,2,E',
            '2,3,F',
        ], fh_to_lines(buffer))

    def test_special_choices(self):
        ballots = [
            Ballot('1', [Candidate('A'), UNDERVOTE, Candidate('C')]),
            Ballot('2', [Candidate('D'), WRITE_IN, OVERVOTE]),
        ]

        buffer = StringIO()
        write_ballots_fh(buffer, ballots)

        self.assertEqual([
            'ballot_id,rank,choice',
            '1,1,A',
            '1,2,$UNDERVOTE',
            '1,3,C',
            '2,1,D',
            '2,2,$WRITE_IN',
            '2,3,$OVERVOTE',
        ], fh_to_lines(buffer))


if __name__ == '__main__':
    unittest.main()
