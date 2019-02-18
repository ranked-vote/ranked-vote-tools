from collections import Counter
from typing import Tuple, Counter as CounterType, Dict, List

from ranked_vote.analysis.pairwise_stat import PairwiseStat
from ranked_vote.ballot import Candidate, EXHAUSTED
from ranked_vote.methods.instant_runoff import InstantRunoff


class FinalByFirst:
    _first_vote_counts: CounterType[Candidate]
    _pair_counts: CounterType[Tuple[Candidate, Candidate]]
    _eliminated_candidates: List[Candidate]
    _final_candidates: List[Candidate]

    def __init__(self, tabulator: InstantRunoff):
        self._final_candidates = tabulator.rounds[-1].candidates + [EXHAUSTED]
        self._eliminated_candidates = [c for c in tabulator.candidates if c not in self._final_candidates]

        self._first_vote_counts = Counter()
        self._pair_counts = Counter()

        for ballot in tabulator.ballots:
            first_choice = ballot.choices[0]
            if first_choice not in self._final_candidates:
                self._first_vote_counts[first_choice] += 1

                second_choice = next((c for c in ballot.choices[1:] if c in self._final_candidates), EXHAUSTED)

                self._pair_counts[(first_choice, second_choice)] += 1

    def _pairwise_iter(self):
        for c1 in self._eliminated_candidates:
            for c2 in self._final_candidates:
                num = self._pair_counts[(c1, c2)]
                denom = self._first_vote_counts[c1]
                yield PairwiseStat(c1, c2, num, denom)

    @property
    def pairwise(self):
        return list(self._pairwise_iter())

    def to_dict(self) -> Dict:
        return {
            'finalists': [str(c) for c in self._final_candidates],
            'eliminated': [str(c) for c in self._eliminated_candidates],
            'pairs': [ps.to_dict() for ps in self.pairwise]
        }
