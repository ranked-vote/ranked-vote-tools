from typing import List, Dict


class Choice:
    pass


class SpecialChoice:
    def __init__(self, choice_id):
        self.choice_id = choice_id

    def __repr__(self):
        return 'Choice: {}'.format(self.choice_id)

    def __str__(self):
        return self.choice_id

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(self.choice_id)


UNDERVOTE = SpecialChoice('$UNDERVOTE')
OVERVOTE = SpecialChoice('$OVERVOTE')
WRITE_IN = SpecialChoice('$WRITE_IN')

NON_COUNTED_VOTES = {UNDERVOTE, OVERVOTE}

_special_choices = {
    '$UNDERVOTE': UNDERVOTE,
    '$OVERVOTE': OVERVOTE,
    '$WRITE_IN': WRITE_IN
}  # type: Dict[str, Choice]

_candidate_registry = dict()  # type: Dict[str, Candidate]


def parse_choice(choice_str: str):
    if choice_str in _special_choices:
        return _special_choices[choice_str]
    else:
        return Candidate.get(choice_str)


class Candidate(Choice):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id

    @staticmethod
    def get(name: str) -> 'Candidate':
        if name not in _candidate_registry:
            _candidate_registry[name] = Candidate(name)
        return _candidate_registry[name]

    def __hash__(self):
        return hash(self.candidate_id)

    def __repr__(self):
        return 'Candidate {}'.format(self.candidate_id)

    def __str__(self):
        return self.candidate_id

    def __eq__(self, other):
        if not isinstance(other, Candidate):
            return False
        return self.candidate_id == other.candidate_id


class Ballot:
    def __init__(self, ballot_id: str, choices: List[Choice]):
        self.ballot_id = ballot_id
        self.choices = choices

    def __repr__(self):
        return 'Ballot {} with choices {}'.format(self.ballot_id, self.choices)

    def __eq__(self, other):
        if not isinstance(other, Ballot):
            return False
        return (self.ballot_id, self.choices) == (other.ballot_id, other.choices)

    @property
    def candidate_rank(self) -> List[Candidate]:
        return [c for c in self.choices if isinstance(c, Candidate)]
