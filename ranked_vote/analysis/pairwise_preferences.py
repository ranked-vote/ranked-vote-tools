from collections import Counter
from typing import Iterator, List, Tuple, Counter as CounterType, Optional, Dict, Set

from ranked_vote.ballot import Ballot, Candidate


class PreferenceMatrix:
    _candidates: List[Candidate]
    _preferences: CounterType[Tuple[Candidate, Candidate]]

    def __init__(self, candidates: List[Candidate], ballots: Iterator[Ballot]):
        self._candidates = candidates
        self._preferences = Counter()

        for ballot in ballots:
            preferred = set()

            for c in ballot.candidate_rank:
                for p in preferred:
                    self._preferences[(p, c)] += 1

                preferred.add(c)

            for p in preferred:
                for c in set(candidates) - preferred:
                    self._preferences[(p, c)] += 1

    def preferred(self, c1, c2):
        return self._preferences[(c1, c2)] > self._preferences[(c2, c1)]

    @property
    def graph(self) -> Dict[Candidate, Set[Candidate]]:
        graph = dict()
        for c1 in self._candidates:
            graph[c1] = set()
            for c2 in self._candidates:
                if self.preferred(c2, c1):
                    graph[c1].add(c2)
        return graph

    @property
    def smith_set(self) -> Set[Candidate]:
        g = self.graph
        last_set = set(g)
        while True:
            this_set = set.union(*(g[a] for a in last_set))
            if this_set == set() or this_set == last_set:
                break
            last_set = this_set

        return last_set

    @property
    def condorcet_winner(self) -> Optional[Candidate]:
        ss = self.smith_set
        if len(ss) == 1:
            return ss.pop()

    @property
    def preferences(self) -> CounterType[Tuple[Candidate, Candidate]]:
        return self._preferences

    @property
    def candidates(self) -> List[Candidate]:
        return self._candidates
