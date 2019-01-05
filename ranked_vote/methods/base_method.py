from abc import ABC, abstractmethod

from ranked_vote.ballot import Ballot, Candidate
from typing import Iterator, Dict, Any


class BaseMethod(ABC):
    winner: Candidate
    metadata: Dict[str, Any]

    def __init__(self, ballots: Iterator[Ballot]):
        self.ballots = list(ballots)
        self.winner = self.tabulate()

    @abstractmethod
    def tabulate(self) -> Candidate:
        pass
