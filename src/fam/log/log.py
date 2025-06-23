from loguru import logger
from fam.state import State
from fam.utils import fprint


def log_verbose(message):

    if State.verbose:
        fprint(message=message)
