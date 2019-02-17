from collections import Counter
from typing import List

from ranked_vote.ballot import Candidate
from ranked_vote.methods.instant_runoff import InstantRunoff, RoundResults


class EagerInstantRunoff(InstantRunoff):
    def eliminate(self, round_results: RoundResults) -> List[Candidate]:
        candidates_ranked = iter(k for k, _ in Counter(round_results.candidate_results).most_common())

        last_votes = round_results.candidate_results[next(candidates_ranked)]
        votes_remaining = round_results.continuing_ballots - last_votes

        eliminated = list()

        for candidate in candidates_ranked:
            if votes_remaining < last_votes:
                eliminated.append(candidate)
            else:
                last_votes = round_results.candidate_results[candidate]
                votes_remaining -= last_votes

        return eliminated + list(candidates_ranked)
