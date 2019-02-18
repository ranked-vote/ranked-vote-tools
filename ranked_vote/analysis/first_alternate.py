from collections import Counter
from typing import Iterator, Tuple, Counter as CounterType, Dict, List

from ranked_vote.analysis.pairwise_stat import PairwiseStat
from ranked_vote.ballot import Ballot, Candidate, Choice, EXHAUSTED


class FirstAlternates:
    _counts: CounterType[Tuple[Candidate, Choice]]
    _first_counts: CounterType[Candidate]
    _candidates: List[Candidate]

    def __init__(self, candidates: List[Candidate], ballots: Iterator[Ballot]):
        self._candidates = candidates

        self._counts = Counter()
        self._first_counts = Counter()

        for ballot in ballots:
            first_choice = ballot.choices[0]
            if len(ballot.choices) > 1 and isinstance(ballot.choices[1], Candidate):
                second_choice = ballot.choices[1]
            else:
                second_choice = EXHAUSTED

            if isinstance(first_choice, Candidate):
                self._first_counts[first_choice] += 1
                self._counts[(first_choice, second_choice)] += 1

    def _pairwise_iter(self):
        for c1 in self._candidates:
            for c2 in self._candidates + [EXHAUSTED]:
                if c1 == c2:
                    continue

                num = self._counts[(c1, c2)]
                denom = self._first_counts[c1]
                yield PairwiseStat(c1, c2, num, denom)

    @property
    def pairwise(self):
        return list(self._pairwise_iter())

    def to_dict_list(self) -> List[Dict]:
        return [ps.to_dict() for ps in self.pairwise]
