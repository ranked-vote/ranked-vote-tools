from typing import Dict, Type

from ranked_vote.methods.eager_instant_runoff import EagerInstantRunoff
from ranked_vote.methods.instant_runoff import InstantRunoff

METHODS = {
    'irv': InstantRunoff,
    'eager_irv': EagerInstantRunoff,
}  # type: Dict[str, Type[InstantRunoff]]
