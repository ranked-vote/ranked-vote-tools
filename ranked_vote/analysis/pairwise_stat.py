from typing import Dict

from ranked_vote.ballot import Candidate


class PairwiseStat:
    def __init__(self, candidate1: Candidate, candidate2: Candidate, numerator: int, denominator: int):
        self.candidate1 = candidate1
        self.candidate2 = candidate2
        self.numerator = numerator
        self.denominator = denominator

    def to_dict(self) -> Dict:
        return {
            'first_candidate': str(self.candidate1),
            'second_candidate': str(self.candidate2),
            'numerator': self.numerator,
            'denominator': self.denominator
        }

    def __repr__(self):
        return 'PairwiseStat({}, {}, {}, {})'.format(self.candidate1, self.candidate2, self.numerator, self.denominator)

    @property
    def _t(self):
        return self.candidate1, self.candidate2, self.numerator, self.denominator

    def __eq__(self, other):
        if not isinstance(other, PairwiseStat):
            return False
        return self._t == other._t
