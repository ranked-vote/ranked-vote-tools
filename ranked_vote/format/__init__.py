import gzip
from csv import DictReader, DictWriter
from itertools import groupby
from typing import Iterator, TextIO

from ranked_vote.ballot import Ballot, parse_choice


def read_ballots_fh(fh: TextIO) -> Iterator[Ballot]:
    reader = DictReader(fh)

    for ballot_id, rows in groupby(reader, lambda x: x['ballot_id']):
        choices = [parse_choice(row['choice']) for row in rows]
        yield Ballot(ballot_id, choices)


def write_ballots_fh(fh: TextIO, ballots: Iterator[Ballot]):
    writer = DictWriter(fh, ['ballot_id', 'rank', 'choice'], lineterminator='\n')
    writer.writeheader()

    for ballot in ballots:
        for rank, choice in enumerate(ballot.choices, 1):
            writer.writerow({
                'ballot_id': ballot.ballot_id,
                'rank': rank,
                'choice': str(choice)
            })


def read_ballots(filename: str) -> Iterator[Ballot]:
    if filename.endswith('.gz'):
        fh = gzip.open(filename, 'rt')
    else:
        fh = open(filename, 'r')

    yield from read_ballots_fh(fh)

    fh.close()


def write_ballots(filename: str, ballots: Iterator[Ballot]):
    if filename.endswith('.gz'):
        fh = gzip.open(filename, 'wt', encoding='UTF-8')
    else:
        fh = open(filename, 'w')

    write_ballots_fh(fh, ballots)

    fh.close()
