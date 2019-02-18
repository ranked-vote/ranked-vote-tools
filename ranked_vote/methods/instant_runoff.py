from collections import defaultdict, Counter
from typing import List, Dict, Counter as CounterType, Tuple

from ranked_vote.ballot import Candidate, NON_COUNTED_VOTES, UNDERVOTE, OVERVOTE, EXHAUSTED
from ranked_vote.methods.base_method import BaseMethod


class RoundResults:
    round: int
    candidates: List[Candidate]
    results: CounterType[Candidate]
    candidate_results: Dict[Candidate, int]
    eliminated: List[Candidate]
    total_ballots: int
    continuing_ballots: int

    def top_candidate(self) -> Candidate:
        return max(self.candidate_results, key=self.candidate_results.get)

    def bottom_candidate(self) -> Candidate:
        return min(self.candidate_results, key=self.candidate_results.get)

    def __init__(self, rnd: int, counts: CounterType[Candidate], eliminated=None,
                 transfers: CounterType[Tuple[Candidate, Candidate]] = None):
        self.round = rnd
        self.results = counts
        self.candidate_results = {k: v for k, v in counts.items() if k not in NON_COUNTED_VOTES}
        self.total_ballots = sum(counts.values())
        self.continuing_ballots = sum(self.candidate_results.values())
        self.candidates = [c for c, _ in Counter(self.candidate_results).most_common()]
        self.eliminated = eliminated
        self.transfers = transfers

    def to_dict(self):
        results = [{
                'name': str(c),
                'votes': v
            } for c, v in self.results.most_common() if isinstance(c, Candidate)]

        results.append({
            'name': str(EXHAUSTED),
            'votes': self.results[UNDERVOTE] + self.results[OVERVOTE]
        })

        return {
            'round': self.round,
            'candidates': [str(c) for c in self.candidates],
            'results': results,
            'undervote': self.results[UNDERVOTE],
            'overvote': self.results[OVERVOTE],
            'continuing_ballots': self.continuing_ballots,
            'eliminated': [str(c) for c in self.eliminated],
            'transfers': [{
                'from': str(fr),
                'to': str(to),
                'count': c
            } for ((fr, to), c) in self.transfers.items()]
        }


class InstantRunoff(BaseMethod):
    rounds: List[RoundResults]
    candidates: List[Candidate]

    def _eliminate(self, round_results: RoundResults) -> List[Candidate]:
        return [round_results.bottom_candidate()]

    def _tabulate(self) -> Candidate:
        self.rounds = list()
        self.candidates = list()

        top_choice_to_choices = defaultdict(list)
        for ballot in self.ballots:
            top_choice_to_choices[ballot.choices[0]].append(ballot.choices)

        last_eliminated = list()
        all_eliminated_candidates = set()
        last_transfer_counts = dict()

        for rnd in range(1, len(self.ballots) + 1):
            # Count first choices
            counts = Counter({candidate: len(ballots) for candidate, ballots in
                              top_choice_to_choices.items()})  # type: CounterType[Candidate, int]

            self.candidates.extend([
                c for c, _ in counts.most_common() if c not in self.candidates
                                                      and isinstance(c, Candidate)
            ])

            round_results = RoundResults(rnd, counts, last_eliminated, last_transfer_counts)
            self.rounds.append(round_results)

            # Check for majority winner
            if max(round_results.candidate_results.values()) >= ((round_results.continuing_ballots + 1) / 2):
                winner = round_results.top_candidate()
                return winner

            # Eliminate bottom choice and redistribute ballots
            last_eliminated = self._eliminate(round_results)
            all_eliminated_candidates.update(last_eliminated)

            last_transfer_counts = Counter()

            for candidate in self.candidates:
                if candidate in last_eliminated:
                    ballots_to_reallocate = top_choice_to_choices.pop(candidate)
                    for ballot in ballots_to_reallocate:
                        while ballot[0] in all_eliminated_candidates:
                            ballot = ballot[1:]
                            if not ballot:
                                ballot.append(UNDERVOTE)
                        top_choice_to_choices[ballot[0]].append(ballot)

                        new_choice = ballot[0]
                        if not isinstance(new_choice, Candidate):
                            new_choice = EXHAUSTED
                        last_transfer_counts[(candidate, new_choice)] += 1
                elif candidate not in all_eliminated_candidates:
                    last_transfer_counts[(candidate, candidate)] += counts[candidate]
            last_transfer_counts[(EXHAUSTED, EXHAUSTED)] = counts[UNDERVOTE] + counts[OVERVOTE]
