from collections import Counter
from typing import List

from ranked_vote.ballot import Ballot, Candidate


class ApprovalEntry:
    def __init__(self, candidate, other_candidate, candidate_votes, other_candidate_votes):
        self.candidate = candidate
        self.other_candidate = other_candidate
        self.candidate_votes = candidate_votes
        self.other_candidate_votes = other_candidate_votes

    def to_dict(self):
        return {
            'candidate': str(self.candidate),
            'other_candidate': str(self.other_candidate),
            'candidate_votes': self.candidate_votes,
            'other_candidate_votes': self.other_candidate_votes,
        }


class ApprovalResult:
    def __init__(self, approval_set: List[ApprovalEntry], approval_set_compliment: List[ApprovalEntry]):
        self.approval_set = approval_set
        self.approval_set_compliment = approval_set_compliment

    def to_dict(self):
        return {
            'approval_set': [d.to_dict() for d in self.approval_set],
            'approval_set_compliment': [d.to_dict() for d in self.approval_set_compliment],
        }


def honest_approval_set(ballots: List[Ballot], candidates: List[Candidate]) -> ApprovalResult:
    approval_set = list()
    approval_set_compliment = list()
    for candidate in candidates:
        votes = Counter()
        for ballot in ballots:
            if candidate in ballot.choices:
                for c in ballot.choices:
                    votes[c] += 1
                    if c == candidate:
                        break
            else:
                votes[ballot.choices[0]] += 1

        candidate_votes = votes.pop(candidate)
        [(other_candidate, other_candidate_votes)] = votes.most_common(1)

        approval_entry = ApprovalEntry(candidate, other_candidate, candidate_votes, other_candidate_votes)

        if candidate_votes > other_candidate_votes:
            approval_set.append(approval_entry)
        else:
            approval_set_compliment.append(approval_entry)

    return ApprovalResult(approval_set, approval_set_compliment)
