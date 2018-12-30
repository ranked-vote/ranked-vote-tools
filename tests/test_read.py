import unittest
from io import StringIO
from ranked_vote_tools.ballot import Ballot, Candidate, UNDERVOTE, OVERVOTE, WRITE_IN
from ranked_vote_tools.files import read_ballots_fh


def lines_to_fh(*lines: str) -> StringIO:
    return StringIO('\n'.join(lines))


class TestReadBallots(unittest.TestCase):
    def test_simple_ballots(self):
        csv_fh = lines_to_fh('ballot_id,rank,choice',
                             '1,1,A',
                             '1,2,B',
                             '1,3,C',
                             '2,1,D',
                             '2,2,E',
                             '2,3,F')
        ballots = read_ballots_fh(csv_fh)

        self.assertEqual(Ballot('1', [
            Candidate('A'),
            Candidate('B'),
            Candidate('C')
        ]), next(ballots))

        self.assertEqual(Ballot('2', [
            Candidate('D'),
            Candidate('E'),
            Candidate('F')
        ]), next(ballots))

        with self.assertRaises(StopIteration):
            next(ballots)

    def test_special_choices(self):
        csv_fh = lines_to_fh('ballot_id,rank,choice',
                             '1,1,$WRITE_IN',
                             '1,2,B',
                             '1,3,$UNDERVOTE',
                             '2,1,D',
                             '2,2,$OVERVOTE',
                             '2,3,F')
        ballots = read_ballots_fh(csv_fh)

        self.assertEqual(Ballot('1', [
            WRITE_IN,
            Candidate('B'),
            UNDERVOTE
        ]), next(ballots))

        self.assertEqual(Ballot('2', [
            Candidate('D'),
            OVERVOTE,
            Candidate('F')
        ]), next(ballots))

        with self.assertRaises(StopIteration):
            next(ballots)

    def test_implicit_undervote(self):
        csv_fh = lines_to_fh('ballot_id,rank,choice',
                             '1,1,A',
                             '1,3,C',
                             '2,1,D',
                             '2,5,F')
        ballots = read_ballots_fh(csv_fh)

        self.assertEqual(Ballot('1', [
            Candidate('A'),
            UNDERVOTE,
            Candidate('C')
        ]), next(ballots))

        self.assertEqual(Ballot('2', [
            Candidate('D'),
            UNDERVOTE,
            UNDERVOTE,
            UNDERVOTE,
            Candidate('F')
        ]), next(ballots))

        with self.assertRaises(StopIteration):
            next(ballots)


if __name__ == '__main__':
    unittest.main()
