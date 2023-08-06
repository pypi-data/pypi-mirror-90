import io
import json
import logging
import os
from pathlib import Path
import sys
from typing import Any, Callable, Dict

from . import Engine
from minionize.types import Param

LOGGER = logging.getLogger(__name__)

ENV_FILE_PATH = "FILE_PATH"
ENV_DECODER = "FILE_DECODER"
DEFAULT_DECODER = "identity"
# default = stdin


def identity_decoder(raw: str) -> str:
    return raw


def json_decoder(raw: str) -> Dict:
    return json.loads(raw)


def create_decoder_from_env():
    decoder = os.environ.get(ENV_DECODER, DEFAULT_DECODER)
    if decoder == "json":
        decoder = json_decoder
    else:
        decoder = identity_decoder
    return decoder


class File(Engine):
    """Process each line of a file.

    This is equivalent to "| xargs".
    No ack mecanism.
    """

    def __init__(
        self, myio: io.IOBase, decoder: Callable[[str], Any] = identity_decoder
    ):
        self.myio = myio
        self.decoder = decoder

    def next(self) -> Param:
        try:
            # strip work also on bytes
            return self.decoder(next(self.myio).strip())
        except StopIteration:
            return None

    def ack(self, param: Param):
        pass

    def nack(self, param: Param):
        pass

    @classmethod
    def from_env(cls):
        path = os.environ.get(ENV_FILE_PATH)
        if path is None:
            file = sys.stdin
            LOGGER.debug("Reading from stdin")
        else:
            file = Path(path).open("r")
            LOGGER.debug(f"reading from {path}")
        decoder = create_decoder_from_env()
        return cls(file, decoder=decoder)
