from typing import Iterator, TextIO
from csv import DictReader, DictWriter
from itertools import groupby

from ranked_vote_tools.ballot import Ballot, parse_choice, UNDERVOTE


def read_ballots_fh(fh: TextIO) -> Iterator[Ballot]:
    reader = DictReader(fh)

    for ballot_id, rows in groupby(reader, lambda x: x['ballot_id']):
        choices = list()
        last_rank = 1
        for row in rows:
            rank = int(row['rank'])
            while last_rank + 1 < rank:
                choices.append(UNDERVOTE)
                last_rank += 1
            choices.append(parse_choice(row['choice']))
            last_rank = rank
        yield Ballot(ballot_id, choices)


def read_ballots(filename: str) -> Iterator[Ballot]:
    pass


def write_ballots(filename: str, ballots: Iterator[Ballot]):
    pass
