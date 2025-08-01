from datetime import date
from typing import Annotated

from pydantic import StringConstraints, validate_call


class Find:
    __slots__ = "query"
    DOMAIN_PATTERN: str = Annotated[
        str,
        StringConstraints(
            pattern=r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
                    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
                    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
                    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
        )
    ]

    def __init__(self, query: str):
        self.query = query

    @validate_call
    def on_site(self, site: DOMAIN_PATTERN):
        self.query += f" site:{site}"
        return self

    @validate_call
    def include(self, *args: str):
        self.query = ' +'.join([self.query, *args])
        return self

    @validate_call
    def exclude(self, *args: str):
        self.query = ' -'.join([self.query, *args])
        return self

    @validate_call
    def exact_phrase(self, *args: str):
        self.query = ' '.join([self.query, *map(lambda item: f'"{item}"', args)])
        return self

    def now(self):
        self.query += f" {date.today()}"
        return self

    def build(self):
        return self.query

    def __str__(self):
        return self.build()
