from abc import ABC, abstractmethod
from typing import Iterator

from ranked_vote.ballot import Ballot, Candidate


class BaseMethod(ABC):
    winner: Candidate

    def __init__(self, ballots: Iterator[Ballot]):
        self.ballots = list(ballots)
        self.winner = self._tabulate()

    @abstractmethod
    def _tabulate(self) -> Candidate:
        pass
