import logging
import rptk.__meta__
from rptk.api import Rptk as RptkAPI

logging.getLogger(__name__).addHandler(
    logging.NullHandler()
)
__all__ = [RptkAPI.__name__]
