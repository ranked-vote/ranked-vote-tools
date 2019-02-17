from abc import ABC, abstractmethod
from typing import Iterator, Dict, Any

from ranked_vote.ballot import Ballot, Candidate


class BaseMethod(ABC):
    winner: Candidate
    metadata: Dict[str, Any]

    def __init__(self, ballots: Iterator[Ballot]):
        self.ballots = list(ballots)
        self.winner = self.tabulate()

    @abstractmethod
    def tabulate(self) -> Candidate:
        pass
