from typing import List, Dict


class Choice:
    pass


class SpecialChoice:
    def __init__(self, choice_id):
        self.choice_id = choice_id

    def __repr__(self):
        return 'Choice: {}'.format(self.choice_id)

    def __eq__(self, other):
        return self is other


UNDERVOTE = SpecialChoice('$UNDERVOTE')
OVERVOTE = SpecialChoice('$OVERVOTE')
WRITE_IN = SpecialChoice('$WRITE_IN')

_choice_registry = {
    '$UNDERVOTE': UNDERVOTE,
    '$OVERVOTE': OVERVOTE,
    '$WRITE_IN': WRITE_IN
} # type: Dict[str, Choice]


def parse_choice(choice_str: str):
    if choice_str not in _choice_registry:
        _choice_registry[choice_str] = Candidate(choice_str)
    return _choice_registry[choice_str]


class Candidate(Choice):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id

    def __repr__(self):
        return 'Candidate {}'.format(self.candidate_id)

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
