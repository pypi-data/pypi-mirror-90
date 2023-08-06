"""Module for custom Graph."""
from typing import (
    Dict,
    List,
)


class Graph:  # pylint:disable=too-few-public-methods
    """Custom structure for encoding and decoding pythonflow graph."""

    def __init__(self, operations: Dict, dependencies: List):
        self.operations = operations
        self.dependencies = dependencies
