from collections import defaultdict, Counter
from typing import List, Dict

from ranked_vote.ballot import Candidate, NON_COUNTED_VOTES, UNDERVOTE
from ranked_vote.methods import BaseMethod


class RoundResults:
    round: int
    candidates: List[Candidate]
    results: Dict[Candidate, int]
    candidate_results: Dict[Candidate, int]
    last_eliminated: List[Candidate]
    total_ballots: int
    total_votes: int

    def top_candidate(self) -> Candidate:
        return max(self.candidate_results, key=self.candidate_results.get)

    def bottom_candidate(self) -> Candidate:
        return min(self.candidate_results, key=self.candidate_results.get)

    def __init__(self, round, counts, last_eliminated=None):
        self.round = round
        self.results = counts
        self.candidate_results = {k: v for k, v in counts.items() if k not in NON_COUNTED_VOTES}
        self.total_ballots = sum(counts.values())
        self.total_votes = sum(self.candidate_results.values())
        self.candidates = Counter(self.candidate_results).most_common()
        self.last_eliminated = last_eliminated


def round_generator():
    i = 1
    while True:
        yield i
        i += 1


class InstantRunoff(BaseMethod):
    rounds: List[RoundResults]

    def tabulate(self) -> Candidate:
        self.rounds = list()

        top_choice_to_choices = defaultdict(list)
        for ballot in self.ballots:
            top_choice_to_choices[ballot.choices[0]].append(ballot.choices)

        last_eliminated = list()

        for rnd in round_generator():
            # Count first choices
            counts = {candidate: len(ballots) for candidate, ballots in
                      top_choice_to_choices.items()}  # type: Dict[Candidate, int]
            round_results = RoundResults(rnd, counts, last_eliminated)
            self.rounds.append(round_results)

            # Check for majority winner
            if max(round_results.candidate_results.values()) >= ((round_results.total_votes + 1) / 2):
                winner = round_results.top_candidate()
                return winner

            # Eliminate bottom choice and redistribute ballots
            bottom_candidate = round_results.bottom_candidate()

            choices = top_choice_to_choices.pop(bottom_candidate)
            for ballot in choices:
                ballot = ballot[1:]
                if ballot == []:
                    ballot.append(UNDERVOTE)
                top_choice_to_choices[ballot[0]].append(ballot)

            last_eliminated = [bottom_candidate]
