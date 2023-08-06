from typing import Dict

from ..logger import Loggable


class Action(Loggable):
    def get_message_types(self) -> Dict[str, callable]:
        return {}

    def passive(self) -> None:
        pass

    def cleanup(self) -> None:
        pass
