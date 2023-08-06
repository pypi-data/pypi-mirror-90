import json
import random
import tempfile

from pathlib import Path

from .base import Handler


class SelectionHandler(Handler):
    """
    When multiple URLs are sent back to allow the user to choose which one.
    """

    SCRATCH = tempfile.NamedTemporaryFile(prefix="majel-", suffix=".html")
    TEMPLATE = Path(__file__).parent.parent / "template.html"

    def __init__(self, driver, payload) -> None:
        super().__init__(driver, payload)
        self.pages = json.loads(payload)

    @classmethod
    def can_handle(cls, payload: str) -> bool:
        """
        When the payload isn't a URL at all, but a JSON blob
        """
        return payload.startswith("[")

    def get_prepared_url(self) -> str:
        return f"file://{self.SCRATCH.name}"

    def pre_fetch(self):

        with open(self.TEMPLATE) as f:
            template = f.read()

        links = ""
        for page in self.pages:
            links += '<a class="{}" href="{}">{}</a>'.format(
                self._get_button_colour(), page["url"], page["title"]
            )

        with open(self.SCRATCH.name, "w") as f:
            f.write(
                template.replace("{{ links }}", links).replace(
                    "{{ columns }}", str(self._get_columns())
                )
            )

    def _get_columns(self):
        page_count = len(self.pages)
        if page_count < 4:
            return page_count
        if page_count < 10:
            return 3
        if page_count < 17:
            return 4
        return 5

    def _get_button_colour(self):
        return "lc2375{:02d}".format(random.randint(1, 8))
