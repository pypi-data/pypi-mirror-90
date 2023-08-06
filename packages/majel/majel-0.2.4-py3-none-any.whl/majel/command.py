#!/usr/bin/env python3

import sys
import time

from mycroft_bus_client import MessageBusClient

from .actions.base import Action
from .config import ConfigurationError
from .logger import Loggable


class Majel(Loggable):
    def __init__(self) -> None:
        self.client = MessageBusClient()
        self.actions = [a() for a in Action.__subclasses__()]

    def __call__(self, *args, **kwargs):

        for action in self.actions:
            for type_, fn in action.get_message_types().items():
                self.logger.info(
                    "Registering %s to %s.%s",
                    type_,
                    action.__class__.__name__,
                    fn.__name__,
                )
                self.client.on(type_, fn)

        self.client.run_forever()

        try:
            while True:
                for action in self.actions:
                    action.passive()
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.logger.info("Exiting")

    @classmethod
    def run(cls):
        """
        I wish I knew a cleaner way to do this, but this appears to be required
        to play nice with the syntax in pyproject.toml.
        """
        cls()()


if __name__ == "__main__":
    try:
        Majel()()
    except ConfigurationError as e:
        sys.stderr.write(str(e))
